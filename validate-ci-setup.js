#!/usr/bin/env node

/**
 * CI Validation Script
 * Validates that the CI testing setup works correctly
 */

const { execSync } = require('child_process');

console.log('🔍 CI Testing Validation');
console.log('========================\n');

async function validateCISetup() {
    const checks = [
        {
            name: 'Node.js dependencies installed',
            command: 'npm list --depth=0',
            description: 'Checking if Node.js dependencies are properly installed'
        },
        {
            name: 'Python environment setup',
            command: 'pipenv --version',
            description: 'Checking if pipenv is available'
        },
        {
            name: 'Python dependencies installed',
            command: 'pipenv run python -c "import fastmcp; print(\'FastMCP available\')"',
            description: 'Checking if Python dependencies are available in pipenv'
        },
        {
            name: 'MCP server module import',
            command: 'pipenv run python -c "from siril_mcp.server import mcp; print(\'MCP server module loads correctly\')"',
            description: 'Checking if the MCP server module loads correctly'
        },
        {
            name: 'Basic test functionality (CI mode)',
            command: 'CI=true npm run test',
            description: 'Running basic tests in CI mode'
        }
    ];

    let passed = 0;
    let total = checks.length;

    for (const check of checks) {
        try {
            console.log(`🧪 ${check.description}...`);
            const result = execSync(check.command, {
                encoding: 'utf8',
                stdio: 'pipe'
            });
            console.log(`✅ ${check.name}\n`);
            passed++;
        } catch (error) {
            console.log(`❌ ${check.name}`);
            console.log(`   Error: ${error.message}\n`);
        }
    }

    console.log('📊 CI Validation Results');
    console.log('========================');
    console.log(`✅ Passed: ${passed}/${total}`);

    if (passed === total) {
        console.log('🎉 CI setup is ready for GitHub Actions!');
        console.log('\n📝 Next Steps:');
        console.log('1. Commit and push your changes');
        console.log('2. Create a pull request to test the CI pipeline');
        console.log('3. Once CI passes, you can create releases with confidence');
        return 0;
    } else {
        console.log('❌ CI setup needs attention before deployment');
        return 1;
    }
}

validateCISetup().then(process.exit).catch(console.error);
