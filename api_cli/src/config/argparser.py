import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI client for Sandbox API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s upload malware.exe 60 --plugins procmon tlsmon
  %(prog)s list
  %(prog)s status task-uid
  %(prog)s files task-uid
  %(prog)s download task-uid dump.pcap --output task-uid.pcap
        """,
    )

    parser.set_defaults(plugins=None)

    parser.add_argument("--api-url", help="API URL")
    parser.add_argument("--token", help="Authentication token")
    parser.add_argument("--timeout", type=float, help="Timeout")
    parser.add_argument("--profile", help="Config profile")

    ### SUBPARSERS
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    ### UPLOAD
    p_upload = subparsers.add_parser("upload", help="Upload file & create sandbox task")
    p_upload.add_argument("file", help="Path to file to upload")
    p_upload.add_argument("duration", type=float, help="Task duration in seconds")
    p_upload.add_argument(
        "--plugins",
        nargs="*",
        help="List of plugin names (Defaults to profile default plugins)",
    )

    ### LIST
    subparsers.add_parser("list", help="List all task UIDs")

    ### STATUS
    p_status = subparsers.add_parser("status", help="Get task status")
    p_status.add_argument("task_uid", help="Task UID to check")

    ### FILES
    p_files = subparsers.add_parser("files", help="List files for a task")
    p_files.add_argument("task_uid", help="Task UID")

    ### DOWNLOAD
    p_download = subparsers.add_parser("download", help="Download a task file")
    p_download.add_argument("task_uid", help="Task UID")
    p_download.add_argument("filename", help="Exact filename to download")
    p_download.add_argument(
        "--output", help="Local output path (defaults to --filename)"
    )

    ### ANALYSIS
    p_analysis = subparsers.add_parser(name="analysis", help="Analysis result")
    p_analysis.add_argument("task_uid", help="Task UID")

    return parser
