from config.loader import load_config, load_settings
from config.argparser import build_parser
from config.models import AppArgs

from editor.command_editor import command_editor
from editor.find_marker import find_marker


def main() -> None:
    settings = load_settings()
    parser = build_parser()
    args = parser.parse_args()

    profile = args.profile or settings.profile

    config = load_config(settings.config_file, profile)

    command_client_exe = args.exe or config.command_client_exe

    if not command_client_exe.exists():
        print("Client executable file does not exist")
        exit(1)

    app_args = AppArgs(
        config.command_marker,
        config.command_size,
        command_client_exe,
        args.command_file,
        args.output_file,
    )

    marker_pos = find_marker(app_args)
    command_editor(marker_pos, app_args)


if __name__ == "__main__":
    main()
