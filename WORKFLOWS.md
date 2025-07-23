# GitHub Workflows

This repository includes several GitHub Actions workflows for continuous integration and deployment:

## Workflows

### 1. CI Workflow (`.github/workflows/ci.yml`)
- **Triggers**: Push to `main` or `develop` branches, pull requests
- **Actions**:
  - Runs on Python 3.10, 3.11, and 3.12
  - Checks code formatting with Black
  - Checks import sorting with isort
  - Lints code with flake8
  - Runs tests with pytest
  - Builds the package to verify it can be built

### 2. Release Workflow (`.github/workflows/release.yml`)
- **Triggers**: Push of version tags (e.g., `v1.0.0`, `v1.2.3`)
- **Actions**:
  - Runs all CI checks
  - Builds the Python package
  - Creates a GitHub release
  - Uploads wheel and source distribution as release assets
  - (Optional) Publishes to PyPI

### 3. Format Workflow (`.github/workflows/format.yml`)
- **Triggers**: Manual dispatch only
- **Actions**:
  - Formats code with Black
  - Sorts imports with isort
  - Commits changes back to the repository

## Usage

### Running CI
CI runs automatically on pushes and pull requests. All checks must pass before merging.

### Creating a Release
1. Update the version in `pyproject.toml`
2. Create and push a git tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. The release workflow will automatically create a GitHub release with downloadable assets

### Manual Code Formatting
To manually trigger code formatting:
1. Go to Actions tab in your GitHub repository
2. Select "Format Code" workflow
3. Click "Run workflow"

### Local Development
You can run the same checks locally using the Pipfile scripts:

```bash
# Install dependencies
pipenv install --dev

# Check formatting
pipenv run format-check

# Format code
pipenv run format

# Run linting
pipenv run lint

# Run tests
pipenv run test

# Build package
pipenv run build
```

## Configuration Files

- `.flake8`: Flake8 linting configuration
- `pyproject.toml`: Contains Black and isort configuration
- `Pipfile`: Development dependencies and scripts

## PyPI Publishing (Optional)

To enable automatic PyPI publishing on releases:

1. Uncomment the PyPI publishing section in `.github/workflows/release.yml`
2. Add your PyPI API token as a GitHub secret named `PYPI_API_TOKEN`
3. Go to Repository Settings → Secrets → Actions
4. Add new secret: `PYPI_API_TOKEN` with your PyPI token value
