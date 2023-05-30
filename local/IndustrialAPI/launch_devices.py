import subprocess
import sys
import glob
from typing import List
import json


mode = "lmdp_ltlf"

if __name__ == "__main__":

    processes: List[subprocess.Popen] = []
    # TODO: modificare qui il path per fargli prendere quello "corrente"
    list_devices = glob.glob(f"IndustrialAPI/actors_api_{mode}/descriptions/*.sdl")
    print(list_devices)

    for configuration_path in list_devices:
        script = f"IndustrialAPI/run_service_{mode}.py"
        process = subprocess.Popen([sys.executable, script, configuration_path])
        processes.append(process)

    for process in processes:
        process.wait()
