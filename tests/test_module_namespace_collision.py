"""
QA finding, now fixed: cross-service Python module namespace collision.

Originally, three of the five FastAPI service packages -- nlp/teamB,
ml/teamA, and cv/teamB -- had no __init__.py at their own directory
level (only rag/teamC did), and cv/teamB and rag/teamC both reached
their own logic via a bare, unqualified `from src.X import Y` combined
with a manual `sys.path.append(...)`. In isolation (as run.py launches
each service, one per OS process) that's harmless. The moment more than
one of these services got imported into the *same* Python process --
which is exactly what a plain `pytest` run across the repo does -- the
generic name `src` collided: whichever service's `src` package loaded
first silently claimed that name for the rest of the process, breaking
the other service's import (or, in the namespace-package case, silently
merging two unrelated teams' code into one virtual package with no
error at all).

Fix applied:
  - Added __init__.py to nlp/teamB, ml/teamA, cv/teamB, cv/teamB/api,
    cv/teamB/src, rag/teamC/api, rag/teamC/src.
  - Replaced the bare `sys.path.append(...); from src.X import Y`
    pattern in cv/teamB/api/main.py and rag/teamC/api/main.py, and the
    bare `from teamB.src.X import Y` in nlp/teamB/api/main.py, with
    ordinary relative imports (`from ..src.X import Y`), which resolve
    against each module's own package identity instead of a shared
    global name.
  - Added pytest.ini (`--import-mode=importlib`) so pytest's own
    collection machinery doesn't reintroduce a similar sys.path
    mutation for test files.

This file now verifies the fix holds, and keeps a self-contained
(temp-directory-based) demonstration of *why* the bare-`src` pattern is
dangerous in general -- decoupled from the current repo state, so it
keeps documenting the underlying Python pitfall even if these specific
files change later.
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class TestFixIsInPlace:

    def test_every_service_package_has_init_files(self):
        required = [
            "nlp/teamB/__init__.py",
            "ml/teamA/__init__.py",
            "cv/teamB/__init__.py",
            "cv/teamB/api/__init__.py",
            "cv/teamB/src/__init__.py",
            "rag/teamC/api/__init__.py",
            "rag/teamC/src/__init__.py",
        ]
        missing = [p for p in required if not (REPO_ROOT / p).exists()]
        assert not missing, f"Missing __init__.py files: {missing}"

    def test_no_service_main_uses_bare_src_sys_path_hack(self):
        offenders = []
        for rel_path in [
            "cv/teamB/api/main.py",
            "rag/teamC/api/main.py",
            "nlp/teamB/api/main.py",
        ]:
            text = (REPO_ROOT / rel_path).read_text()
            if "sys.path.append" in text or "from src." in text or "from teamB.src" in text:
                offenders.append(rel_path)
        assert not offenders, (
            f"Expected these to use package-relative imports (`from ..src...`), "
            f"not a bare `src`/`teamB` name + manual sys.path mutation: {offenders}"
        )

    def test_full_repo_pytest_run_has_no_module_collision_errors(self):
        """
        End-to-end confirmation: running the whole suite together (the
        natural, default way to run "all the tests" in this repo) no
        longer produces any ModuleNotFoundError/collision fallout.
        """
        result = subprocess.run(
            [PYTHON, "-m", "pytest", "nlp", "ml", "cv", "rag", "backend", "agent", "-q"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=180,
        )
        combined = result.stdout + result.stderr
        assert "ModuleNotFoundError" not in combined, (
            f"Expected the full-suite run to be free of import collisions.\n"
            f"--- actual output (tail) ---\n{combined[-3000:]}"
        )


class TestBareSrcPackageNameIsAGeneralPythonPitfall:
    """
    Not about this repo's current state -- a timeless demonstration of
    *why* the pattern this repo used to have is dangerous, using
    freshly-created temp directories so it stays true regardless of any
    future changes to the actual service files.
    """

    def test_two_unrelated_bare_src_packages_collide_when_combined(self, tmp_path):
        service_a = tmp_path / "service_a"
        service_b = tmp_path / "service_b"
        (service_a / "src").mkdir(parents=True)
        (service_b / "src").mkdir(parents=True)
        (service_a / "src" / "__init__.py").write_text("")
        (service_a / "src" / "alpha.py").write_text("VALUE = 'from service_a'")
        # service_b/src has no __init__.py -- the more common "quick script"
        # shape, and the one this repo actually had.
        (service_b / "src" / "beta.py").write_text("VALUE = 'from service_b'")

        snippet = f"""
import sys
sys.path.insert(0, r"{service_a}")
import src  # binds bare 'src' to service_a's regular package, permanently

sys.path.append(r"{service_b}")
try:
    from src.beta import VALUE
    print("NO_COLLISION:" + VALUE)
except ModuleNotFoundError as e:
    print(f"COLLISION:{{e}}")
"""
        result = subprocess.run(
            [PYTHON, "-c", snippet],
            capture_output=True,
            text=True,
            timeout=30,
        )
        out = result.stdout.strip()
        assert out.startswith("COLLISION:"), (
            f"Expected service_a's regular-package `src` (imported first) to "
            f"permanently shadow service_b's same-named `src`, breaking "
            f"`from src.beta import VALUE` with ModuleNotFoundError. "
            f"Got: stdout={result.stdout!r} stderr={result.stderr!r}"
        )
