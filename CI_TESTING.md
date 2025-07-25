# 🚀 CI/CD Testing Documentation

## Overview

This repository includes comprehensive CI/CD testing for the Siril MCP server, ensuring that every release is thoroughly validated before deployment.

## Testing Strategy

### 🧪 Test Suites

1. **Simple MCP Test** (`simple-mcp-test.js`)
   - Tests basic functionality and internal functions
   - Validates script generation capabilities  
   - Tests project structure validation logic
   - **CI-Aware**: Adapts behavior when Siril binary is not available

2. **MCP Integration Test** (`test-mcp-integration.js`)
   - Tests the actual MCP server with proper protocol handshake
   - Validates tool listing functionality
   - Tests real MCP tool execution
   - **CI-Aware**: Handles missing Siril binary gracefully

### 🏗️ CI Workflows

#### Regular CI (`ci.yml`)
Triggered on pushes and PRs to `main` and `develop` branches:

1. **Lint and Format** - Code quality checks
2. **MCP Integration Test** - Full MCP functionality validation
3. **Build Test** - Package build validation

#### Release CI (`release.yml`)
Triggered on version tags (`v*`):

1. **Lint and Test** - Code quality and Python tests
2. **MCP Integration Test** - Full MCP functionality validation across Python versions
3. **Build and Release** - Package build and PyPI publishing

### 🔄 CI Environment Adaptations

The test suite automatically detects CI environments and adapts accordingly:

- **Local Development**: Full testing including Siril binary detection
- **CI Environment**: Modified testing that skips Siril-specific operations while still validating MCP protocol functionality

## Running Tests

### Locally
```bash
# Run basic functionality tests
npm run test

# Run MCP integration tests  
npm run test:integration

# Run all tests
npm run test:all
```

### CI Environment
Tests automatically run in CI with appropriate environment detection:

```bash
# Set CI flag for adapted testing
CI=true npm run test:all
```

## What Gets Tested

### ✅ Always Tested (Local + CI)
- Module imports and dependencies
- MCP protocol compliance
- Tool registration and listing
- Project structure validation logic
- Script generation functionality
- Package building

### 🖥️ Local Development Only
- Siril binary detection and validation
- Actual Siril version checking
- Full end-to-end workflow testing

## Adding New Tests

1. Add test logic to appropriate test file
2. Ensure CI-awareness using `process.env.CI` checks
3. Update this documentation
4. Test locally and in CI environment

## Release Process

Before any release (`v*` tag), the CI system will:

1. ✅ Validate code formatting and linting
2. ✅ Run comprehensive MCP testing across Python versions
3. ✅ Build and validate the package
4. 🚀 Only then proceed with PyPI publishing

This ensures every release is thoroughly validated and ready for production use!
