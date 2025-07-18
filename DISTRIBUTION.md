# Distribution Guide for Siril MCP Server

## Summary

Your Siril MCP server is now properly configured for distribution using **Pipenv** for Python package management. Here's what was implemented:

## ✅ What We Added

### 1. **Automatic SSF Script Creation**
- **No more manual downloads**: The SSF scripts are embedded in the code and created automatically
- **Latest versions included**: Contains the current broadband and narrowband scripts from naztronaut/siril-scripts
- **Fallback support**: If network downloads fail, embedded versions are used
- **Proper attribution**: Credits to Nazmus Nasir (Naztronomy.com) under GPL-3.0 license

### 2. **Enhanced Tools**
- `check_siril_version()` - Check your Siril installation
- `process_seestar_mosaic()` - **Auto-creates SSF scripts** and processes your images
- `check_project_structure()` - Analyze your project directory structure
- `download_latest_ssf_scripts()` - Download latest scripts from GitHub (optional)
- `preprocess_with_gui()` - Launch Naztronomy GUI tools

### 3. **Pipenv-Based Development**
- **Pipfile** with production and development dependencies
- **Pipenv scripts** for common tasks (build, test, lint, format)
- **Automated testing** with pytest
- **Code formatting** with Black
- **Linting** with Flake8
- **Release automation** script

### 4. **Comprehensive Testing**
- Unit tests for core functionality
- Mocked external dependencies (Siril subprocess calls)
- Validation tests for project structure
- SSF script content verification

### 5. **Professional Package Structure**
```
siril_mcp/
├── LICENSE (MIT)
├── README.md (comprehensive docs)
├── pyproject.toml (modern Python packaging)
├── Pipfile (Pipenv configuration)
├── Pipfile.lock (locked dependencies)
├── MANIFEST.in (package manifest)
├── setup.cfg (tool configuration)
├── release.sh (automated release script)
├── siril_mcp/
│   ├── __init__.py
│   └── server.py (main MCP server with embedded SSF scripts)
└── tests/
    ├── __init__.py
    └── test_server.py (comprehensive tests)
```

## 🚀 Distribution Methods

### 1. **PyPI Distribution (Recommended)**
```bash
# Build and test
pipenv run build
pipenv run test

# Upload to Test PyPI first
./release.sh test

# Then upload to production PyPI
./release.sh prod
```

### 2. **GitHub Releases**
Upload the files in `dist/` to a GitHub release.

### 3. **Direct Installation**
Users can install directly from GitHub:
```bash
pipenv install git+https://github.com/yourusername/siril-mcp.git
```

## 📦 User Installation Options

### Option 1: Using Pipenv (Recommended)
```bash
pipenv install siril-mcp
pipenv run siril-mcp
```

### Option 2: Using pip
```bash
pip install siril-mcp
siril-mcp
```

### Option 3: Development Installation
```bash
git clone https://github.com/yourusername/siril-mcp
cd siril-mcp
pipenv install --dev
pipenv shell
```

## 🔧 Available Pipenv Scripts

```bash
pipenv run build      # Build the package
pipenv run test       # Run tests with pytest
pipenv run format     # Format code with Black
pipenv run lint       # Lint code with Flake8
pipenv run upload-test # Upload to Test PyPI
pipenv run upload     # Upload to production PyPI
```

## 🎯 Key Advantages

1. **Self-Contained**: No external script downloads required
2. **User-Friendly**: Automatic SSF script creation
3. **Reliable**: Embedded scripts ensure consistency
4. **Modern**: Uses current Python packaging standards
5. **Tested**: Comprehensive test suite
6. **Maintainable**: Pipenv for dependency management
7. **Professional**: Clean code, documentation, and structure

## 📝 Next Steps

1. **Update** your personal details in `pyproject.toml`
2. **Create** a GitHub repository and push your code
3. **Set up** PyPI account and get API tokens
4. **Test** on TestPyPI before production release
5. **Consider** adding GitHub Actions for CI/CD

Your MCP server is now ready for professional distribution! 🎉
