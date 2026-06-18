import json
import sys
from typing import Any
from tqdm import tqdm


class Console:
    def info(self, msg: str):
        print(f"Info: {msg}")

    def warning(self, msg: str):
        print(f"Warning: {msg}")

    def error(self, msg: str):
        print(f"Error: {msg}", file=sys.stderr)

    def json(self, data: dict):
        print(json.dumps(data, indent=2))

    def pretty_print_list(self, lst: list[Any]):
        for elem in lst:
            print(f"\t- {elem}")

    def progress_bar(self, desc: str, total: int, initial: int):
        return tqdm(
            desc=desc,
            total=total,
            initial=initial,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )
