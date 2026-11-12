import subprocess
import sys
from pathlib import Path

root = Path(r"C:\NewStartsNov\TheTechDocket")
pythonw_exe = root / ".venv" / "Scripts" / "pythonw.exe"
log_path = root / "bg_run.log"

date_arg = sys.argv[1] if len(sys.argv) > 1 else "2026-11-09"

cmd = [str(pythonw_exe), "-u", str(root / "run_date.py"), date_arg]
with open(log_path, "w", encoding="utf-8") as f:
    p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=str(root))
print(f"Launched pythonw PID: {p.pid} for {date_arg}")
