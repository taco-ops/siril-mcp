# Siril MCP Server

[![CI](https://github.com/taco-ops/siril-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/taco-ops/siril-mcp/actions/workflows/ci.yml)
[![Release](https://github.com/taco-ops/siril-mcp/actions/workflows/release.yml/badge.svg)](https://github.com/taco-ops/siril-mcp/actions/workflows/release.yml)
[![Python Versions](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://github.com/taco-ops/siril-mcp)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Development Status](https://img.shields.io/badge/status-work%20in%20progress-yellow.svg)](https://github.com/taco-ops/siril-mcp)

> **⚠️ Work in Progress**: This project is under active development and not yet ready for production use. APIs may change without notice.

A Model Context Protocol (MCP) server that provides tools for working with Siril astronomical image processing software and Seestar telescope data.

## 🚧 Current Status

This project is in **early development**. Current features include:

- ✅ **Siril Binary Detection**: Smart detection of Siril installations across platforms
- ✅ **Version Checking**: Check your installed Siril version  
- ✅ **Basic Mosaic Processing**: Process Seestar S30/S50 telescope images
- ✅ **Filter Support**: Supports both broadband and narrowband processing
- ✅ **Auto Script Creation**: Automatically creates required SSF scripts
- ✅ **FastMCP Integration**: Proper async logging and error handling
- 🔄 **Script Updates**: Download latest scripts from Naztronomy repository
- 🔄 **Project Analysis**: Check project structure and file organization  
- ❌ **GUI Integration**: Headless preprocessing tools (planned)
- ❌ **PyPI Package**: Not yet published

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
- [Siril](https://siril.org/) astronomical image processing software

### Siril Installation & Detection

The server automatically detects Siril installations in the following order:

1. **Custom Path**: Set `SIRIL_BINARY` environment variable to specify a custom location
2. **System PATH**: Checks if `siril` command is available in your PATH
3. **macOS App Bundle**: `/Applications/Siril.app/Contents/MacOS/Siril`
4. **Common Locations**: `/usr/bin/siril`, `/usr/local/bin/siril`, `/opt/homebrew/bin/siril`

**macOS Users**: If you installed Siril as an application, no additional setup is needed - it will be detected automatically.

**Custom Installation**: For non-standard installations, set the environment variable:
```bash
export SIRIL_BINARY="/path/to/your/siril/binary"
```

## Installation

> **Note**: This package is not yet published to PyPI. Install from source for now.

### From Source (Development)
```bash
git clone https://github.com/taco-ops/siril-mcp
cd siril-mcp

# Using pipenv (recommended)
pipenv install --dev
pipenv shell

# Or using pip
pip install -e .
```

### Future PyPI Installation
Once published, you'll be able to install via:
```bash
# Using pip
pip install siril-mcp

# Using pipenv
pipenv install siril-mcp
```

## Development Setup

This project uses [Pipenv](https://pipenv.pypa.io/) for dependency management. Make sure you have Pipenv installed:

```bash
pip install pipenv
```

### Setting up the development environment:

```bash
# Clone the repository
git clone https://github.com/taco-ops/siril-mcp
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

## 🧪 Testing

The project includes comprehensive tests for all major functionality:

```bash
# Run all tests
pipenv run test

# Run tests with coverage
pipenv run python -m pytest tests/ --cov=siril_mcp --cov-report=html

# Run specific test
pipenv run python -m pytest tests/test_server.py::test_find_siril_binary_macos_location -v
```

**Test Coverage Includes:**
- ✅ Siril binary detection across platforms
- ✅ Version checking and error handling  
- ✅ SSF script content validation
- ✅ Project structure validation
- ✅ Filter type processing differences
- ✅ Environment variable handling
- ✅ Error conditions and edge cases

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

### `find_siril_binary()`
Locates and validates the Siril binary on your system. Useful for troubleshooting installation issues.

### `validate_siril_binary(binary_path)`
Tests whether a specific Siril binary path works correctly. Useful for validating custom installations.

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

### `preprocess_with_gui(project_dir)` *(Planned)*
Future feature to launch Naztronomy Smart Telescope preprocessing GUI in headless mode.

## Filter Types Available

- **`broadband`**: For UV/IR block filters (most common)
- **`narrowband`**: For light pollution (LP) filters

## 🚀 Releases

Releases are automatically built and published when tags are pushed:

```bash
# Create and push a new version tag
git tag v0.1.0
git push origin v0.1.0
```

This will trigger:
- ✅ Automated testing across Python 3.10, 3.11, and 3.12
- ✅ Building wheel and source distributions  
- ✅ Creating a GitHub release with artifacts
- ✅ Publishing to PyPI (for stable releases)

## 🤝 Contributing

This project is in early development and contributions are welcome! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Install development dependencies**: `pipenv install --dev`
4. **Make your changes and add tests**
5. **Run the test suite**: `pipenv run test`
6. **Format your code**: `pipenv run format`
7. **Lint your code**: `pipenv run lint`
8. **Commit your changes**: `git commit -m 'Add amazing feature'`
9. **Push to the branch**: `git push origin feature/amazing-feature`
10. **Open a Pull Request**

### Development Roadmap

- [ ] Complete GUI integration for preprocessing tools
- [ ] Add support for additional telescope types
- [ ] Implement batch processing capabilities  
- [ ] Add image quality assessment tools
- [ ] Create comprehensive documentation site
- [ ] Publish to PyPI for stable releases
- [ ] Add Docker container support

## Filter Types Available

## Credits

This MCP server uses SSF scripts from the [naztronomy/siril-scripts](https://github.com/naztronaut/siril-scripts) repository by Nazmus Nasir (Naztronomy.com), used under the GPL-3.0 license.

## License

MIT License - see LICENSE file for details.
