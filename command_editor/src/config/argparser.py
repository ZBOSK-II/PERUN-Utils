import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Command Client Executable Editor")

    parser.add_argument("--exe", type=Path, help="Path to CommandClient executable")
    parser.add_argument(
        "command_file", type=Path, help="Path to .json file with Client command"
    )
    parser.add_argument("output_file", type=Path, help="Modified Client output path")
    parser.add_argument("--profile", help="Config profile")

    return parser
