import subprocess
import sys
import os
import time
import webbrowser

# Windows consoles often default to a legacy codepage (e.g. cp1252) that
# can't encode the emoji used in this script's own print()s below, which
# crashes the launcher before any service starts. Force UTF-8 on stdout/
# stderr so this works regardless of the host console's configured codepage.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.getcwd()
PYTHON = sys.executable  # 🔥 ensures correct environment

processes = []

def start_service(name, command, cwd):
    print(f"🚀 Starting {name}...")
    proc = subprocess.Popen(
        command,
        cwd=cwd
    )
    processes.append(proc)
    time.sleep(1)

try:
    # NLP
    start_service(
        "NLP",
        [PYTHON, "-m", "uvicorn", "teamB.api.main:app", "--port", "8001", "--reload"],
        os.path.join(BASE_DIR, "nlp")
    )

    # ML
    start_service(
        "ML",
        [PYTHON, "-m", "uvicorn", "teamA.api.main:app", "--port", "8002", "--reload"],
        os.path.join(BASE_DIR, "ml")
    )

    # RAG
    start_service(
        "RAG",
        [PYTHON, "-m", "uvicorn", "teamC.api.main:app", "--port", "8003", "--reload"],
        os.path.join(BASE_DIR, "rag")
    )

    # CV
    start_service(
        "CV",
        [PYTHON, "-m", "uvicorn", "teamB.api.main:app", "--port", "8004", "--reload"],
        os.path.join(BASE_DIR, "cv")
    )

    # AGENT
    start_service(
        "AGENT",
        [PYTHON, "-m", "uvicorn", "teamA.app:app", "--port", "8005", "--reload"],
        os.path.join(BASE_DIR, "agent")
    )

    # BACKEND
    start_service(
        "BACKEND",
        [PYTHON, "-m", "uvicorn", "main:app", "--port", "8000", "--reload"],
        os.path.join(BASE_DIR, "backend")
    )

    # FRONTEND SERVER
    start_service(
        "FRONTEND",
        [PYTHON, "-m", "http.server", "3000"],
        os.path.join(BASE_DIR, "frontend", "webpage")
    )

    # Give server time to start
    time.sleep(2)

    # Open browser (cross-platform)
    webbrowser.open("http://localhost:3000/landing")

    print("\n✅ ALL SERVICES STARTED\n")

    for p in processes:
        p.wait()

except KeyboardInterrupt:
    print("\n🛑 Stopping all services...")
    for p in processes:
        p.terminate()
    sys.exit(0)
