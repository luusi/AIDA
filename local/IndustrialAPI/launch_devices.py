import subprocess
import sys
import glob
from typing import List
import json


mode = "lmdp_ltlf"

if __name__ == "__main__":

    processes: List[subprocess.Popen] = []
    list_devices = glob.glob(f"actors_api_{mode}/descriptions/*.sdl")

    for configuration_path in list_devices:
        script = f"run_service_{mode}.py"
        process = subprocess.Popen([sys.executable, script, configuration_path])
        processes.append(process)

    for process in processes:
        process.wait()
