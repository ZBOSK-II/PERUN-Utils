# PERUN-Utils

## Overview

This repository contains a collection of utility tools developed for the PERUN project. 

Each utility is maintained as an independent project with its own documentation, configuration, and usage instructions. Detailed installation, configuration, and operational guidance can be found in the README file located within each project's directory.

The repository is primarily managed using `uv`. A standard `pyproject.toml` configuration is provided, allowing the use of other compatible Python package and environment managers; however, only `uv` is actively maintained and tested.

Project-specific instructions for dependency management, installation, and execution are documented in the respective utility documentation.

## Available Utilities

### API CLI

A command-line client for interacting with the PERUN API.

Key capabilities include:

- Listing sandbox tasks
- Uploading analysis samples
- Checking task status
- Retrieving analysis outputs such as:

  - Network capture files (`.pcap`)
  - Memory dumps
  - Additional task-generated artifacts

### Command editor

A utility for modifying PERUN command client executables.

The tool allows users to insert or replace JSON-based command definitions within a precompiled PERUN command client executable, enabling customization of command behavior without rebuilding the executable.

## Documentations

For detailed information about a specific utility, refer to the README file located in its project directory:

- [API CLI](api_cli/README.md)
- [Command Editor](command_editor/README.md)
