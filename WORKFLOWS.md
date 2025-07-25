# GitHub Workflows

This repository includes comprehensive GitHub Actions workflows for continuous integration, MCP testing, and automated deployment with robust quality gates.

## Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)
- **Triggers**: Push to `main` or `develop` branches, pull requests
- **Multi-Stage Pipeline**:

  **Stage 1: Lint and Format**
  - Runs on Python 3.10, 3.11, and 3.12
  - Checks code formatting with Black
  - Checks import sorting with isort
  - Lints code with flake8
  - Runs Python unit tests with pytest

  **Stage 2: MCP Integration Testing**
  - Sets up Python environment with pipenv
  - Sets up Node.js 18 with npm dependencies
  - Runs comprehensive MCP functionality tests
  - Validates MCP protocol compliance and tool execution
  - **CI-Aware**: Adapts testing for environments without Siril binary

  **Stage 3: Build Testing**
  - Builds the Python package to verify integrity
  - Validates package structure with twine
  - Uploads build artifacts for verification

### 2. Release Workflow (`.github/workflows/release.yml`)
- **Triggers**: Push of version tags (e.g., `v1.0.0`, `v1.2.3`)
- **Comprehensive Release Pipeline**:

  **Stage 1: Lint and Test**
  - Multi-Python validation (3.10, 3.11, 3.12)
  - Code quality checks (Black, isort, flake8)
  - Python unit test validation with pytest

  **Stage 2: MCP Integration Validation**
  - Full MCP server testing across all Python versions
  - Protocol compliance validation
  - Tool functionality verification
  - **Quality Gate**: Release only proceeds if ALL MCP tests pass

  **Stage 3: Build and Release**
  - Builds Python package (wheel and source distribution)
  - Creates GitHub release with downloadable assets
  - **Optional**: Publishes to PyPI (requires API token configuration)
  - **Dependency**: Only runs after successful completion of previous stages

### 3. Format Workflow (`.github/workflows/format.yml`)
- **Triggers**: Manual dispatch only
- **Actions**:
  - Formats code with Black
  - Sorts imports with isort
  - Commits changes back to the repository

### 4. Test CI Setup Workflow (`.github/workflows/test-ci-setup.yml`)
- **Triggers**: Manual dispatch (for CI validation)
- **Purpose**: Validates that CI testing infrastructure works correctly
- **Actions**:
  - Tests CI setup across Python 3.10, 3.11, and 3.12
  - Validates Node.js and npm dependency installation
  - Runs comprehensive CI validation checks
  - Executes full test suite in CI mode

## Usage

### Running CI
CI runs automatically on pushes and pull requests. **All checks must pass before merging**, including:
- ✅ Code formatting and linting
- ✅ Python unit tests across all supported versions
- ✅ MCP integration tests and protocol validation
- ✅ Package build verification

### Creating a Release
1. Update the version in `pyproject.toml`
2. Create and push a git tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. **Automated Release Pipeline Executes**:
   - Comprehensive testing across Python versions
   - MCP functionality validation
   - Package building and integrity checks
   - GitHub release creation with assets
   - Optional PyPI publishing (if configured)

**Quality Assurance**: No release proceeds unless ALL validation stages pass successfully.

### Manual Code Formatting
To manually trigger code formatting:
1. Go to Actions tab in your GitHub repository
2. Select "Format Code" workflow
3. Click "Run workflow"

### Manual CI Validation
To test CI setup without creating a release:
1. Go to Actions tab in your GitHub repository
2. Select "Test CI Setup" workflow
3. Click "Run workflow" to validate CI infrastructure

### Local Development
You can run the same checks locally using both Python and Node.js tools:

#### Python Testing (Pipenv):
```bash
# Install Python dependencies
pipenv install --dev

# Check formatting
pipenv run format-check

# Format code
pipenv run format

# Run linting
pipenv run lint

# Run Python unit tests
pipenv run test

# Build package
pipenv run build
```

#### MCP Integration Testing (npm):
```bash
# Install Node.js dependencies
npm install

# Run basic MCP functionality tests
npm run test

# Run MCP integration tests
npm run test:integration

# Run all MCP tests
npm run test:all

# Validate CI readiness
npm run validate-ci

# Test in CI mode locally
CI=true npm run test:all
```

## Configuration Files

### Python Configuration:
- `.flake8`: Flake8 linting configuration
- `pyproject.toml`: Contains Black and isort configuration
- `Pipfile`: Python development dependencies and scripts

### Node.js Configuration:
- `package.json`: Node.js dependencies and MCP testing scripts
- MCP testing files:
  - `simple-mcp-test.js`: Basic functionality tests
  - `test-mcp-integration.js`: Complete MCP protocol validation
  - `validate-ci-setup.js`: CI readiness validation

### Documentation:
- `CI_TESTING.md`: Comprehensive testing strategy documentation
- `WORKFLOWS.md`: This file - workflow documentation

## Testing Strategy

### Multi-Layer Testing Approach:
1. **Python Unit Tests**: Traditional pytest-based testing for core functionality
2. **MCP Integration Tests**: Node.js-based testing for complete MCP server validation
3. **CI Environment Testing**: Adaptive testing that works both locally and in CI
4. **Release Validation**: Comprehensive pre-release testing across all Python versions

### Environment Adaptation:
- **Local Development**: Full testing including Siril binary detection and validation
- **CI Environment**: Modified testing that skips Siril-specific operations while maintaining MCP protocol validation
- **Automatic Detection**: Tests automatically detect environment and adapt behavior accordingly

## PyPI Publishing (Optional)

To enable automatic PyPI publishing on releases:

1. **Uncomment PyPI Publishing**: Uncomment the PyPI publishing section in `.github/workflows/release.yml`
2. **Configure API Token**: Add your PyPI API token as a GitHub secret
3. **Setup Instructions**:
   - Go to Repository Settings → Secrets → Actions
   - Add new secret: `PYPI_API_TOKEN` with your PyPI token value
4. **Security**: API token is securely stored and only used during successful releases

**Important**: PyPI publishing only occurs after ALL quality gates pass:
- ✅ Code quality validation
- ✅ Multi-Python testing
- ✅ MCP integration testing
- ✅ Package build verification

## Quality Gates

This repository implements strict quality gates to ensure reliable releases:

### Pre-Merge Requirements (CI):
- ✅ Code formatting compliance (Black)
- ✅ Import sorting compliance (isort)
- ✅ Linting without errors (flake8)
- ✅ Python unit tests passing
- ✅ MCP integration tests passing
- ✅ Package building successfully

### Pre-Release Requirements (Release):
- ✅ All CI requirements across Python 3.10, 3.11, and 3.12
- ✅ MCP protocol validation across all Python versions
- ✅ Complete tool functionality verification
- ✅ Package integrity validation

**No code merges or releases proceed unless ALL requirements are satisfied.**
