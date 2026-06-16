from config.models import AppArgs


def command_editor(marker_pos: int, config: AppArgs) -> None:
    command_data = config.command_file.read_bytes()
    exe_data = bytearray(config.command_client_exe.read_bytes())

    command_size = len(command_data)
    if command_size > config.command_size:
        print(
            f"Command file too large ({command_size} bytes), max size is {config.command_size}"
        )

    exe_data[marker_pos : marker_pos + config.command_size] = (
        b"\x00" * config.command_size
    )

    exe_data[marker_pos : marker_pos + command_size] = command_data

    config.output_file.write_bytes(exe_data)

    print(f"Patched executable written to {config.output_file}")
    print(f"JSON size: {command_size} bytes")
