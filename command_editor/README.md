# Command Editor

## Overview

Command Editor is a utility for modifying PERUN command client executables.

The tool allows users to insert or replace JSON-based command definitions within a precompiled PERUN command client executable, enabling customization of command behavior without rebuilding the executable.

## Features

Command Editor provides the following functionality:

- Embedding JSON command definitions into a command client executable
- Profile-based configuration
- Support for multiple command types

A reference command client executable and example command definitions are provided with the project.

## Configuration

Command Editor supports configuration through environment variables and profile-based configuration files.

### Environment Configuration

Create a `.env` file in the project directory.

Example:

```env
config_file=".config"
profile="default"
```

#### Available Variables

| Variable      | Description                  | Required |
| ------------- | ---------------------------- | -------- |
| `config_file` | Path to configuration file   | No       |
| `profile`     | Configuration profile to use | No       |

Default values:

| Variable      | Default   |
| ------------- | --------- |
| `config_file` | `.config` |
| `profile`     | `default` |

### Profile Configuration

Profiles are defined in a configuration file.

Example `.config`:

```ini
[default]
command_marker = COMMAND_START_MARKER
command_size = 4096
command_client_exe = command_client.exe
```

#### Configuration Options

| Option               | Description                                                          |
| -------------------- | -------------------------------------------------------------------- |
| `command_marker`     | Marker used to locate the command storage area inside the executable |
| `command_size`       | Maximum size allocated for the embedded command definition           |
| `command_client_exe` | Default command client executable used during editing                |

## Installation

### Using uv

Install project dependencies:

```bash
uv sync
```

### Using pip

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install .
```

## Running the Application

### Using uv

```bash
uv run python src/main.py
```

### Using pip

```bash
python3 src/main.py
```

## Command Definition Format

Embedded commands must follow the JSON structure shown below:

```json
{
    "command": "command_name",
    "args": {
        ... // command-specific arguments
    }
}
```

Example command definitions are available in the `examples` directory.

## Supported Command Definitions

The provided `command_client.exe` executable supports the following command definitions.

### credential_stealer

Performs credential extraction.

#### Required Arguments

None.

### port_scanner

Performs TCP port scanning against a specified target.

#### Required Arguments

| Argument  | Description                                       |
| --------- | ------------------------------------------------- |
| `address` | Target IPv4 address                               |
| `begin`   | First port in scan range                          |
| `end`     | Last port in scan range                           |
| `delay`   | Delay between connection attempts in milliseconds |

#### Example

```json
{
    "address": "127.0.0.1",
    "begin": 1,
    "end": 80,
    "delay": 200
}
```

### dos

Performs a denial-of-service simulation against a specified target.

#### Required Arguments

| Argument   | Description                               |
| ---------- | ----------------------------------------- |
| `address`  | Target IPv4 address                       |
| `port`     | Target port                               |
| `interval` | Interval between requests in milliseconds |
| `duration` | Duration in seconds                       |

#### Example

```json
{
    "address": "127.0.0.1",
    "port": 80,
    "interval": 100,
    "duration": 30
}
```

## Command-Line Interface

Command Editor uses `argparse` and provides built-in help for all options.

General syntax:

```text
main.py [-h] [--exe EXE] [--profile PROFILE] command_file output_file
```

### Positional Arguments

| Argument       | Description                             |
| -------------- | --------------------------------------- |
| `command_file` | Path to a JSON command definition       |
| `output_file`  | Output path for the modified executable |

### Options

| Option      | Description                           |
| ----------- | ------------------------------------- |
| `--exe`     | Path to the command client executable |
| `--profile` | Configuration profile                 |

Command-line arguments take precedence over values provided through `.env` files and profile configuration.

## Examples

Embed a command definition into the default command client executable:

```bash
python3 src/main.py examples/port_scanner.json modified_client.exe
```

Use a specific command client executable:

```bash
python3 src/main.py \
    --exe command_client.exe \
    examples/dos.json \
    modified_client.exe
```

Use a specific configuration profile:

```bash
python3 src/main.py \
    --profile default \
    examples/credential_stealer.json \
    modified_client.exe
```

## Project Structure

```text
command_editor/
├── README.md
├── command_client.exe
├── examples
│   ├── credential_stealer.json
│   ├── dos.json
│   └── port_scanner.json
├── pyproject.toml
├── .config
└── src
    ├── config
    │   ├── argparser.py
    │   ├── loader.py
    │   └── models.py
    ├── editor
    │   ├── command_editor.py
    │   └── find_marker.py
    └── main.py
```
