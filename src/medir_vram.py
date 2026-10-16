import json
import re
import subprocess

import psutil


def get_vram_gb():
  pids = {
    p.pid
    for p in psutil.process_iter(["name", "cmdline"])
    if "--type=gpu-process" in (p.info["cmdline"] or [])
  }
  cmd = [
    "powershell", "-NoProfile", "-Command",
    ("Get-CimInstance Win32_PerfFormattedData_GPUPerformanceCounters_GPUProcessMemory"
    " | Select-Object Name,DedicatedUsage | ConvertTo-Json"),
  ]
  saida = subprocess.run(cmd, check=False, capture_output=True, text=True).stdout.strip()
  if not saida:
    return None

  dados = json.loads(saida)
  if isinstance(dados, dict):
    dados = [dados]

  total_bytes = 0
  for d in dados:
    m = re.match(r"pid_(\d+)_", d["Name"])
    if m and int(m[1]) in pids:
      pid = int(m[1])
      processo = psutil.Process(pid).name()

      print(f"PID: {pid} | Processo: {processo} - {d["DedicatedUsage"]}")
      total_bytes += d["DedicatedUsage"]

  return round(total_bytes / 1000**3, 6)

if __name__ == "__main__":
  vram_gb = get_vram_gb()
  print(f"Uso de VRAM: {vram_gb} GB" if vram_gb is not None else "Não foi possível coletar a VRAM.")