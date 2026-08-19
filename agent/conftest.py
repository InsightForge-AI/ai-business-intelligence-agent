import sys
from pathlib import Path

# Every module in this service (app.py, api/, services/, etc.) is
# imported with bare names like `from api.routes import router`, which
# only resolve if this service's own directory -- not the repo root --
# is on sys.path. run.py gets this for free by setting each service's
# directory as the subprocess cwd before launching uvicorn. pytest does
# not: collecting agent/tests/test_api.py from the repo root fails with
# `ModuleNotFoundError: No module named 'app'` without this, because
# agent/tests/ has no __init__.py, so pytest's own rootdir walk stops
# there instead of reaching agent/. This lets `pytest` work uniformly
# whether invoked from the repo root or from inside this directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
