import inspect
import os
import subprocess
import sys
from pathlib import Path
from typing import List

CURRENT_DIRECTORY = Path(os.path.dirname(inspect.getfile(inspect.currentframe())))

DEVICES = [
    "stator_builder_service.json",
    "stator_warehouse_service.json",
    "rotor_builder1_service.json",
    "rotor_builder2_service.json",
    "rotor_warehouse_service.json",
    "inverter_warehouse_service.json",
    "assembler1_service.json",
    "assembler2_service.json",
    "painter1_service.json",
    "painter2_service.json",
    "smart_tester1_service.json",
    "smart_tester2_service.json",
    "mechanical_engineer_service.json",
]


if __name__ == "__main__":
    config_dir = Path("IndustrialAPI", "services")
    processes: List[subprocess.Popen] = []
    for configuration in DEVICES:
        configuration_path = config_dir / configuration
        script_name = "run-service.py"
        process = subprocess.Popen([sys.executable, script_name, "--spec", str(configuration_path)])
        processes.append(process)

    for process in processes:
        process.wait()