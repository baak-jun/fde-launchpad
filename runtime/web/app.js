'use strict';
const token = document.querySelector('meta[name="fde-token"]').content;
const $ = (id) => document.getElementById(id);
let domains = [], domain = '', selected = null, jobs = [], busy = false;
const statuses = {needs_review:'검토 대기',approved:'승인됨',rejected:'거부됨',completed:'기록 완료'};
const modes = {rules:'규칙 기반',live_model:'실제 모델',rules_fallback:'규칙 대안 · 모델 오류'};
const events = {submitted:'요청 접수와 초안 생성',approved:'현재 초안 승인',rejected:'요청 거부',revised_approval_cleared:'입력 수정 · 기존 승인 해제',executed_local_sandbox:'로컬 결과 기록'};
function el(tag, text, cls) { const node=document.createElement(tag); if(text!==undefined)node.textContent=text;if(cls)node.className=cls;return node; }
function message(text, error=false){$('status').textContent=text;$('status').className=error?'error':'';}
async function api(path, method='GET', body) {
  const response=await fetch('/api'+path,{method,headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body)});
  const data=await response.json();
  if(!response.ok)throw new Error(typeof data.detail==='string'?data.detail:'입력 형식을 확인해 주세요.');
  return data;
}
async function guard(action){if(busy)return;busy=true;document.querySelectorAll('button').forEach(b=>b.disabled=true);try{await action();}catch(error){message(error.message,true);}finally{busy=false;renderDomains();renderJobs();renderDetail();$('submit').disabled=false;$('sample').disabled=false;$('refresh').disabled=false;}}
function renderDomains(){const root=$('domains');root.replaceChildren();domains.forEach((d,i)=>{const b=el('button',undefined,'domain'+(d.id===domain?' selected':''));b.setAttribute('aria-pressed',String(d.id===domain));const text=el('span');text.append(el('strong',d.name),el('small',d.description));b.append(text,el('span','0'+(i+1),'number'));b.onclick=()=>{domain=d.id;selected=null;renderDomains();renderJobs();renderDetail();$('request-text').value='';};root.append(b);});$('domain-description').textContent=domains.find(d=>d.id===domain)?.description||'';}
function renderJobs(){const root=$('jobs');root.replaceChildren();const filtered=jobs.filter(j=>j.domain===domain);$('count').textContent=filtered.length;if(!filtered.length)root.append(el('p','아직 요청이 없습니다. 예제로 시작해 보세요.','empty'));filtered.forEach(j=>{const b=el('button',undefined,'job'+(selected?.id===j.id?' active':''));const top=el('div',undefined,'job-top');top.append(el('span',j.result.proposal.title),el('small',statuses[j.status]));b.append(top,el('p',j.text));b.onclick=()=>guard(async()=>{selected=await api('/jobs/'+j.id);});root.append(b);});}
function button(text,fn,cls=''){const b=el('button',text,cls);b.onclick=()=>guard(fn);return b;}
async function reload(){jobs=await api('/jobs');if(selected)selected=await api('/jobs/'+selected.id);}
function renderDetail(){const root=$('detail');if(!selected){root.replaceChildren();const box=el('div',undefined,'empty-state');box.append(el('span','↗','empty-icon'),el('h3','요청을 선택해 주세요'),el('p','초안을 만든 뒤 분류와 근거를 검토하세요.','empty'));root.append(box);return;}root.replaceChildren();const j=selected,p=j.result.proposal,pack=domains.find(d=>d.id===j.domain);const head=el('div',undefined,'detail-head');head.append(el('h3',p.title),el('span',statuses[j.status],'badge '+j.status));root.append(head,el('p',modes[j.result.mode]+' · '+j.result.latency_ms+' ms · 버전 '+j.version,'meta'),el('p',p.summary,'summary'));
if(p.blocked_reason)root.append(el('p',p.blocked_reason,'blocked'));
const evidence=el('div',undefined,'evidence');evidence.append(el('h4','적용한 업무 기준'));p.policy_ids.forEach(id=>{const rule=pack.policies.find(r=>r.id===id);evidence.append(el('p',rule?rule.text:id));});if(!p.policy_ids.length)evidence.append(el('p','근거가 지정되지 않았습니다. 직접 확인하세요.'));root.append(evidence);
const actions=el('div',undefined,'actions');
if(j.status==='needs_review'){if(!p.blocked_reason)actions.append(button('승인',()=>decide('approve')));actions.append(button('거부',()=>decide('reject'),'danger'));}
if(j.status==='approved')actions.append(button('로컬 기록 생성',async()=>{await api('/jobs/'+j.id+'/execute','POST',{expected_version:j.version,proposal_hash:j.proposal_hash});await reload();message('승인한 초안을 이 기기에 기록했습니다. 외부 시스템에는 전송하지 않았습니다.');}));root.append(actions);
if(j.status!=='completed'){const label=el('label','요청을 수정하면 다시 검토합니다.');label.htmlFor='revision-text';const input=el('textarea');input.id='revision-text';input.value=j.text;input.maxLength=8000;input.rows=3;root.append(label,input,button('수정 후 초안 다시 만들기',async()=>{const text=$('revision-text').value;await api('/jobs/'+j.id,'PATCH',{text,expected_version:j.version});await reload();message('입력을 수정하고 기존 승인을 해제했습니다.');},'secondary'));}
if(j.action)root.append(el('div','로컬 기록 생성 완료 · '+j.action.id+'\n실제 발송·결제·예약은 수행하지 않았습니다.','action-result'));
const history=el('div',undefined,'history');history.append(el('h4','처리 이력'));const list=el('ul');(j.events||[]).forEach(e=>{const li=el('li',events[e.kind]||e.kind);li.append(el('time',new Date(e.at).toLocaleString('ko-KR')));list.append(li);});history.append(list);root.append(history);
}
async function decide(decision){await api('/jobs/'+selected.id+'/decision','POST',{expected_version:selected.version,decision});await reload();message(decision==='approve'?'승인했습니다. 로컬 기록을 생성할 수 있습니다.':'거부했습니다. 실행되지 않았습니다.');}
$('sample').onclick=()=>{$('request-text').value=domains.find(d=>d.id===domain).sample;};
$('submit-form').onsubmit=e=>{e.preventDefault();guard(async()=>{const data=await api('/jobs','POST',{domain,text:$('request-text').value,idempotency_key:crypto.randomUUID()});selected=await api('/jobs/'+data.id);await reload();message('초안을 만들었습니다. 근거와 내용을 검토해 주세요.');});};
$('refresh').onclick=()=>guard(reload);
(async()=>{try{const health=await api('/health');$('mode').textContent=modes[health.mode]+' · 로컬 기록';domains=await api('/domains');domain=domains[0].id;await reload();renderDomains();renderJobs();}catch(error){message(error.message,true);}})();
