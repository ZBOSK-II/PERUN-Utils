from config.models import AppArgs


def find_marker(config: AppArgs) -> int:
    data = bytearray(config.command_client_exe.read_bytes())

    marker_pos = data.find(config.command_marker.encode())

    if marker_pos == -1:
        print("Marker not found in executable")
        exit(1)

    return marker_pos
