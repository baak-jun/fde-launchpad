import hashlib
import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


def now():
    return datetime.now(timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


class StoreError(Exception):
    def __init__(self, status, message):
        self.status, self.message = status, message


class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.execute('PRAGMA journal_mode=WAL')
            db.executescript('''
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY, tenant TEXT NOT NULL, request_key TEXT NOT NULL,
                    request_hash TEXT NOT NULL, domain TEXT NOT NULL, text TEXT NOT NULL,
                    result TEXT NOT NULL, proposal_hash TEXT NOT NULL, status TEXT NOT NULL,
                    version INTEGER NOT NULL, approved_hash TEXT, approved_by TEXT,
                    created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
                    UNIQUE(tenant, request_key)
                );
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY, job_id TEXT NOT NULL, tenant TEXT NOT NULL,
                    actor TEXT NOT NULL, kind TEXT NOT NULL, at TEXT NOT NULL, detail TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS actions (
                    id TEXT PRIMARY KEY, job_id TEXT UNIQUE NOT NULL, tenant TEXT NOT NULL,
                    kind TEXT NOT NULL, payload TEXT NOT NULL, at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS budgets (
                    tenant TEXT NOT NULL, day TEXT NOT NULL, reserved_calls INTEGER NOT NULL,
                    PRIMARY KEY(tenant, day)
                );
            ''')

    @contextmanager
    def connection(self, write=False):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            if write:
                db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def event(self, db, principal, job_id, kind, detail=None):
        db.execute('INSERT INTO events(job_id,tenant,actor,kind,at,detail) VALUES(?,?,?,?,?,?)',
                   (job_id, principal.tenant, principal.actor, kind, now(), canonical(detail or {})))

    def row(self, db, principal, job_id):
        row = db.execute('SELECT * FROM jobs WHERE id=? AND tenant=?', (job_id, principal.tenant)).fetchone()
        if row is None:
            raise StoreError(404, '요청을 찾을 수 없습니다.')
        return row

    def public(self, row):
        result = dict(row)
        result.pop('request_hash')
        result['result'] = json.loads(result['result'])
        return result

    def get(self, principal, job_id):
        with self.connection() as db:
            result = self.public(self.row(db, principal, job_id))
            result['events'] = [dict(r) for r in db.execute('SELECT actor,kind,at,detail FROM events WHERE job_id=? AND tenant=? ORDER BY id', (job_id, principal.tenant))]
            action = db.execute('SELECT * FROM actions WHERE job_id=? AND tenant=?', (job_id, principal.tenant)).fetchone()
            result['action'] = dict(action) if action else None
            return result

    def list(self, principal):
        with self.connection() as db:
            return [self.public(r) for r in db.execute('SELECT * FROM jobs WHERE tenant=? ORDER BY created_at DESC LIMIT 100', (principal.tenant,))]

    def existing(self, principal, submission):
        with self.connection() as db:
            row = db.execute('SELECT * FROM jobs WHERE tenant=? AND request_key=?', (principal.tenant, submission.idempotency_key)).fetchone()
            if row:
                if row['request_hash'] != digest({'domain': submission.domain, 'text': submission.text}):
                    raise StoreError(409, '같은 요청 키에 다른 내용을 사용할 수 없습니다.')
                return self.public(row)

    def create(self, principal, submission, result):
        with self.connection(write=True) as db:
            row = db.execute('SELECT * FROM jobs WHERE tenant=? AND request_key=?', (principal.tenant, submission.idempotency_key)).fetchone()
            request_hash = digest({'domain': submission.domain, 'text': submission.text})
            if row:
                if row['request_hash'] != request_hash:
                    raise StoreError(409, '같은 요청 키에 다른 내용을 사용할 수 없습니다.')
                return self.public(row)
            job_id, stamp = uuid.uuid4().hex, now()
            db.execute('INSERT INTO jobs VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                (job_id, principal.tenant, submission.idempotency_key, request_hash, submission.domain, submission.text,
                 canonical(result), digest(result['proposal']), 'needs_review', 1, None, None, stamp, stamp))
            self.event(db, principal, job_id, 'submitted', {'mode': result['mode']})
            return self.public(self.row(db, principal, job_id))

    def revise(self, principal, job_id, text, expected_version, result):
        with self.connection(write=True) as db:
            row = self.row(db, principal, job_id)
            self.check_version(row, expected_version)
            if row['status'] == 'completed':
                raise StoreError(409, '완료된 요청은 변경할 수 없습니다. 새 요청을 만드세요.')
            db.execute('UPDATE jobs SET text=?,result=?,proposal_hash=?,status=?,version=version+1,approved_hash=NULL,approved_by=NULL,updated_at=? WHERE id=?',
                       (text, canonical(result), digest(result['proposal']), 'needs_review', now(), job_id))
            self.event(db, principal, job_id, 'revised_approval_cleared')
            return self.public(self.row(db, principal, job_id))

    def check_version(self, row, version):
        if row['version'] != version:
            raise StoreError(409, '다른 변경이 있습니다. 최신 상태를 다시 불러오세요.')

    def decide(self, principal, job_id, decision, version):
        with self.connection(write=True) as db:
            row = self.row(db, principal, job_id)
            self.check_version(row, version)
            if row['status'] != 'needs_review':
                raise StoreError(409, '검토 대기 상태에서만 결정할 수 있습니다.')
            if decision == 'approve' and json.loads(row['result'])['proposal']['blocked_reason']:
                raise StoreError(409, '차단된 요청은 승인할 수 없습니다.')
            approved = decision == 'approve'
            status = 'approved' if approved else 'rejected'
            db.execute('UPDATE jobs SET status=?,version=version+1,approved_hash=?,approved_by=?,updated_at=? WHERE id=?',
                       (status, row['proposal_hash'] if approved else None, principal.actor if approved else None, now(), job_id))
            self.event(db, principal, job_id, status)
            return self.public(self.row(db, principal, job_id))

    def execute(self, principal, job_id, version, proposal_hash):
        # Only a local sandbox connector. Action and completion share one transaction.
        # A remote connector MUST implement its own idempotency/reconciliation contract.
        with self.connection(write=True) as db:
            row = self.row(db, principal, job_id)
            if row['proposal_hash'] != proposal_hash:
                raise StoreError(409, '요청 내용이 변경되었습니다.')
            if row['status'] == 'completed':
                return self.public(row)
            self.check_version(row, version)
            if row['status'] != 'approved' or row['approved_hash'] != row['proposal_hash']:
                raise StoreError(409, '현재 내용에 대한 승인이 필요합니다.')
            db.execute('INSERT INTO actions VALUES(?,?,?,?,?,?)',
                       (uuid.uuid4().hex, job_id, principal.tenant, 'local_sandbox_record', canonical(json.loads(row['result'])['proposal']), now()))
            db.execute('UPDATE jobs SET status=?,version=version+1,updated_at=? WHERE id=?', ('completed', now(), job_id))
            self.event(db, principal, job_id, 'executed_local_sandbox')
            return self.public(self.row(db, principal, job_id))

    def reserve_calls(self, principal, limit, count=2):
        day = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        with self.connection(write=True) as db:
            row = db.execute('SELECT reserved_calls FROM budgets WHERE tenant=? AND day=?', (principal.tenant, day)).fetchone()
            used = row[0] if row else 0
            if used + count > limit:
                raise StoreError(429, '일일 모델 호출 한도에 도달했습니다.')
            db.execute('INSERT INTO budgets VALUES(?,?,?) ON CONFLICT(tenant,day) DO UPDATE SET reserved_calls=excluded.reserved_calls', (principal.tenant, day, used + count))

    def backup(self, destination):
        destination = Path(destination)
        if destination.exists():
            raise FileExistsError(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as source:
            target = sqlite3.connect(destination)
            try:
                source.backup(target)
                assert target.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
            finally:
                target.close()
