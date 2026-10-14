from config.loader import load_config, load_settings
from config.argparser import build_parser
from config.models import ApiArgs

from api.client import ApiClient
from api.exceptions import AppError
from tui import Console

from commands.upload import UploadCommand
from commands.list import ListCommand
from commands.status import StatusCommand
from commands.files import FilesCommand
from commands.download import DownloadCommand
from commands.analysis import AnalysisCommand


def main() -> int:
    settings = load_settings()
    parser = build_parser()
    args = parser.parse_args()

    profile = args.profile or settings.profile

    config = load_config(settings.config_file, profile)

    timeout = args.timeout or config.timeout

    api_url = args.api_url or settings.api_url
    token = args.token or settings.token

    if not api_url:
        parser.error("API URL is required. Provide it via `--token` or `.env` file")
    if not token:
        parser.error(
            "Authentication token is required. Provide it via `--api-url` or `.env` file"
        )
    if args.plugins is None:
        args.plugins = config.default_plugins

    api_args = ApiArgs(timeout, api_url, token)

    console = Console()
    api = ApiClient(api_args)

    commands = {
        "upload": UploadCommand,
        "list": ListCommand,
        "status": StatusCommand,
        "files": FilesCommand,
        "download": DownloadCommand,
        "analysis": AnalysisCommand,
    }

    try:
        command_class = commands[args.command]
        command = command_class(api, console)
        command.execute(args)
        return 0
    except AppError as e:
        console.error(str(e))
        return 1
    except Exception as e:
        console.error(str(e))
        return 1


if __name__ == "__main__":
    exit(main())
