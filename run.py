import subprocess
import sys
import os
import time

# Windows consoles often default to a legacy codepage (e.g. cp1252) that
# can't encode the emoji used in this script's own print()s below, which
# crashes the launcher before any service starts. Force UTF-8 on stdout/
# stderr so this works regardless of the host console's configured codepage.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.getcwd()
PYTHON = sys.executable

processes = []


def start_service(name, cwd, port):
    """
    Start a FastAPI service.
    """

    print(f"🚀 Starting {name}...")

    process = subprocess.Popen(

        [
            PYTHON,
            "-m",
            "uvicorn",
            "app:app",
            "--reload",
            "--port",
            str(port)
        ],

        cwd=cwd

    )

    processes.append(process)

    time.sleep(2)


try:

    # --------------------------------------------------
    # Agent
    # --------------------------------------------------

    start_service(

        "Agent",

        os.path.join(BASE_DIR, "agent"),

        8001

    )

    # --------------------------------------------------
    # ML
    # --------------------------------------------------

    start_service(

        "ML",

        os.path.join(BASE_DIR, "ml"),

        8002

    )

    # --------------------------------------------------
    # NLP
    # --------------------------------------------------

    start_service(

        "NLP",

        os.path.join(BASE_DIR, "nlp"),

        8003

    )

    # --------------------------------------------------
    # RAG
    # --------------------------------------------------

    start_service(

        "RAG",

        os.path.join(BASE_DIR, "rag"),

        8004

    )

    # --------------------------------------------------
    # CV
    # --------------------------------------------------

    start_service(

        "CV",

        os.path.join(BASE_DIR, "cv"),

        8005

    )

    # --------------------------------------------------
    # Backend
    # --------------------------------------------------

    start_service(

        "Backend",

        os.path.join(BASE_DIR, "backend"),

        8000

    )

    print("\n========================================")
    print("✅ All DocuMind services started.")
    print("========================================\n")

    print("Backend Docs : http://127.0.0.1:8000/docs")
    print("Agent Docs   : http://127.0.0.1:8001/docs")
    print("ML Docs      : http://127.0.0.1:8002/docs")
    print("NLP Docs     : http://127.0.0.1:8003/docs")
    print("RAG Docs     : http://127.0.0.1:8004/docs")
    print("CV Docs      : http://127.0.0.1:8005/docs")

    print("\nPress CTRL+C to stop all services.\n")

    for process in processes:

        process.wait()

except KeyboardInterrupt:

    print("\n🛑 Stopping all services...\n")

    for process in processes:

        process.terminate()

    print("✅ All services stopped.")