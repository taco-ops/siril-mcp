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

This project uses [Pipenv](https://pipenv.pypa.io/) for Python dependency management and npm for MCP testing tools. Make sure you have both installed:

```bash
pip install pipenv
# Node.js and npm should be installed for MCP integration testing
```

### Setting up the development environment:

```bash
# Clone the repository
git clone https://github.com/taco-ops/siril-mcp
cd siril-mcp

# Install Python dependencies and create virtual environment
pipenv install --dev

# Install Node.js dependencies for MCP testing
npm install

# Activate the virtual environment
pipenv shell

# Install the package in development mode
pipenv install -e .

# Validate setup
npm run validate-ci
```

### Available scripts:

#### Python (Pipenv):
```bash
# Build the package
pipenv run build

# Run Python tests
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

#### MCP Testing (npm):
```bash
# Run basic MCP functionality tests
npm run test

# Run MCP integration tests
npm run test:integration

# Run all MCP tests
npm run test:all

# Validate CI setup readiness
npm run validate-ci
```

## 🧪 Testing & Quality Assurance

This project includes comprehensive testing with both Python unit tests and MCP integration testing.

### Test Suites

#### Python Unit Tests
Traditional pytest-based testing for core functionality:
```bash
# Run all Python tests
pipenv run test

# Run tests with coverage
pipenv run python -m pytest tests/ --cov=siril_mcp --cov-report=html

# Run specific test
pipenv run python -m pytest tests/test_server.py::test_find_siril_binary_macos_location -v
```

#### MCP Integration Tests
Node.js-based testing that validates the complete MCP server functionality:
```bash
# Install Node.js dependencies
npm install

# Run basic functionality tests
npm run test

# Run MCP protocol integration tests
npm run test:integration

# Run all MCP tests
npm run test:all

# Validate CI readiness
npm run validate-ci
```

### CI/CD Pipeline

The project uses GitHub Actions for automated testing and releases:

#### Continuous Integration
- **Triggers**: Every push and PR to `main` and `develop` branches
- **Python Versions**: Tests across Python 3.10, 3.11, and 3.12
- **Test Coverage**: Code formatting, linting, Python tests, and MCP integration tests
- **Environment Adaptive**: Tests automatically adapt to CI environments where Siril isn't available

#### Release Pipeline
- **Triggers**: When version tags (`v*`) are pushed
- **Pre-Release Validation**: Comprehensive testing across all Python versions
- **MCP Protocol Validation**: Ensures MCP server functionality before release
- **Automated Publishing**: Builds and publishes to PyPI only after all tests pass

### Test Coverage Includes
- ✅ Siril binary detection across platforms
- ✅ Version checking and error handling
- ✅ SSF script content validation
- ✅ Project structure validation
- ✅ MCP protocol compliance and tool registration
- ✅ Complete MCP server initialization and tool execution
- ✅ Filter type processing differences
- ✅ Environment variable handling
- ✅ CI/CD environment adaptation
- ✅ Error conditions and edge cases

### Local Development Testing
```bash
# Quick validation of local setup
npm run validate-ci

# Test in CI mode locally (simulates GitHub Actions)
CI=true npm run test:all

# Full local testing
pipenv run test && npm run test:all
```

For detailed testing documentation, see [CI_TESTING.md](CI_TESTING.md).

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

## 🚀 Releases & CI/CD

### Automated Release Process

Releases are automatically built and published with comprehensive validation:

```bash
# Create and push a new version tag
git tag v0.1.0
git push origin v0.1.0
```

This triggers the complete release pipeline:

#### Pre-Release Validation
1. ✅ **Code Quality**: Automated linting and formatting checks
2. ✅ **Multi-Python Testing**: Tests across Python 3.10, 3.11, and 3.12
3. ✅ **Python Unit Tests**: Complete pytest suite validation
4. ✅ **MCP Integration Tests**: Full MCP protocol and tool functionality testing
5. ✅ **Package Building**: Wheel and source distribution validation

#### Release Execution
6. ✅ **GitHub Release**: Automated release creation with artifacts
7. ✅ **PyPI Publishing**: Automatic publishing to PyPI (for stable releases)

### Quality Gates

**No release proceeds unless ALL tests pass**, ensuring every published version is:
- ✅ Properly formatted and linted
- ✅ Compatible across supported Python versions
- ✅ Functionally validated with unit tests
- ✅ MCP protocol compliant
- ✅ Tool functionality verified
- ✅ Package integrity confirmed

### CI Status Badges

The repository includes live status badges showing:
- [![CI](https://github.com/taco-ops/siril-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/taco-ops/siril-mcp/actions/workflows/ci.yml) **Continuous Integration**: Current build status
- [![Release](https://github.com/taco-ops/siril-mcp/actions/workflows/release.yml/badge.svg)](https://github.com/taco-ops/siril-mcp/actions/workflows/release.yml) **Release Pipeline**: Latest release status

## 🤝 Contributing

This project is in early development and contributions are welcome! Here's how to get started:

### Development Setup
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Install development dependencies**:
   ```bash
   pipenv install --dev  # Python dependencies
   npm install           # Node.js testing dependencies
   ```

### Making Changes
4. **Make your changes and add tests**
   - Add Python unit tests in `tests/` directory
   - Update MCP integration tests if modifying tool functionality
5. **Run the complete test suite**:
   ```bash
   pipenv run test      # Python tests
   npm run test:all     # MCP integration tests
   npm run validate-ci  # CI readiness check
   ```
6. **Format and lint your code**:
   ```bash
   pipenv run format    # Black formatting
   pipenv run lint      # Flake8 linting
   ```

### Submitting Changes
7. **Commit your changes**: `git commit -m 'Add amazing feature'`
8. **Push to the branch**: `git push origin feature/amazing-feature`
9. **Open a Pull Request**

### Pull Request Requirements

All PRs must pass:
- ✅ **Code Formatting**: Black formatting compliance
- ✅ **Linting**: Flake8 validation without errors
- ✅ **Python Tests**: All pytest unit tests passing
- ✅ **MCP Integration**: All MCP protocol tests passing
- ✅ **Multi-Python**: Tests passing on Python 3.10, 3.11, and 3.12
- ✅ **CI Validation**: All GitHub Actions workflows passing

### Testing Your Changes Locally

Before submitting a PR, ensure everything works:
```bash
# Quick validation (like CI will run)
npm run validate-ci

# Complete local testing
pipenv run test && npm run test:all

# Test CI mode locally
CI=true npm run test:all
```

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
