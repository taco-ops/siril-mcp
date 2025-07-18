# Siril MCP Server (WIP)

A Model Context Protocol (MCP) server that provides tools for working with Siril astronomical image processing software and Seestar telescope data.

## Features

- **Version Checking**: Check your installed Siril version
- **Mosaic Processing**: Process Seestar S30/S50 telescope images into mosaics
- **Filter Support**: Supports both broadband (UV/IR block) and narrowband (LP filter) processing
- **Auto Script Creation**: Automatically creates the required SSF scripts (no manual downloads needed!)
- **Script Updates**: Download latest scripts from the Naztronomy repository
- **Project Analysis**: Check your project structure and file organization
- **GUI Integration**: Launch Naztronomy preprocessing tools in headless mode

## Prerequisites

- Python 3.10+
- [Siril](https://siril.org/) installed and available in your PATH

## Installation

### From PyPI (once published)
```bash
# Using pip
pip install siril-mcp

# Using pipenv (recommended)
pipenv install siril-mcp
```

### From Source
```bash
git clone https://github.com/yourusername/siril-mcp
cd siril-mcp

# Using pipenv (recommended)
pipenv install --dev
pipenv shell

# Or using pip
pip install -e .
```

## Development Setup

This project uses [Pipenv](https://pipenv.pypa.io/) for dependency management. Make sure you have Pipenv installed:

```bash
pip install pipenv
```

### Setting up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/siril-mcp
cd siril-mcp

# Install dependencies and create virtual environment
pipenv install --dev

# Activate the virtual environment
pipenv shell

# Install the package in development mode
pipenv install -e .
```

### Available Pipenv scripts:

```bash
# Build the package
pipenv run build

# Run tests
pipenv run test

# Format code with Black
pipenv run format

# Lint code with Flake8
pipenv run lint

# Upload to Test PyPI
pipenv run upload-test

# Upload to production PyPI
pipenv run upload
```

## Usage

### As an MCP Server
Run the server directly:
```bash
# If installed globally
siril-mcp

# If using pipenv
pipenv run siril-mcp

# Or activate the environment first
pipenv shell
siril-mcp
```

### With Claude Desktop
Add to your Claude Desktop configuration:
```json
{
  "mcpServers": {
    "siril": {
      "command": "siril-mcp"
    }
  }
}
```

## Project Structure

Your Seestar project should be organized like this:
```
project_root/
├── lights/                 # Your FITS files go here
│   ├── Light_001.fits
│   ├── Light_002.fits
│   └── ...
└── process/               # Output directory (created automatically)
    └── mosaic.fits        # Final processed mosaic
```

**Note**: The SSF script files are created automatically - you don't need to download them manually!

## Available Tools

### `check_siril_version()`
Returns the version of your installed Siril software.

### `process_seestar_mosaic(project_dir, filter_type)`
Processes FITS files in the project directory using the appropriate Siril script.
- `project_dir`: Path to your project root
- `filter_type`: Either "broadband" or "narrowband"

**The function automatically creates the required SSF scripts**, so you don't need to download anything manually.

### `check_project_structure(project_dir)`
Analyzes your project directory and shows what files are present and what might be missing.

### `download_latest_ssf_scripts(project_dir)`
Downloads the latest SSF script files from the [naztronaut/siril-scripts](https://github.com/naztronaut/siril-scripts) repository.

### `preprocess_with_gui(project_dir)`
Launches the Naztronomy Smart Telescope preprocessing GUI in headless mode.

## Filter Types Available

- **`broadband`**: For UV/IR block filters (most common)
- **`narrowband`**: For light pollution (LP) filters

## Credits

This MCP server uses SSF scripts from the [naztronomy/siril-scripts](https://github.com/naztronaut/siril-scripts) repository by Nazmus Nasir (Naztronomy.com), used under the GPL-3.0 license.

## License

MIT License - see LICENSE file for details.
