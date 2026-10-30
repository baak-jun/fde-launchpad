"""Start the local-only workbench. No network exposure or paid AI calls by default."""
import argparse
import uvicorn

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    uvicorn.run('runtime.app:configured_app', factory=True, host='127.0.0.1', port=args.port, log_level='info')
