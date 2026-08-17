import sys
from pathlib import Path

# See agent/conftest.py for the full explanation -- same fix, same
# reason, applied per service since each one's internal imports are
# bare and only resolve relative to that service's own directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
