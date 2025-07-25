#!/usr/bin/env node

/**
 * Version synchronization script
 * Keeps pyproject.toml and package.json versions in sync
 */

const fs = require('fs');
const path = require('path');

// Read package.json version
const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
const newVersion = packageJson.version;

// Read pyproject.toml
const pyprojectPath = 'pyproject.toml';
let pyprojectContent = fs.readFileSync(pyprojectPath, 'utf8');

// Update version in pyproject.toml
const versionRegex = /^version\s*=\s*"[^"]*"/m;
pyprojectContent = pyprojectContent.replace(versionRegex, `version = "${newVersion}"`);

// Write back to pyproject.toml
fs.writeFileSync(pyprojectPath, pyprojectContent);

console.log(`✅ Synchronized version to ${newVersion} in pyproject.toml`);

// Also update it in __init__.py if it exists
const initPyPath = path.join('siril_mcp', '__init__.py');
if (fs.existsSync(initPyPath)) {
    let initContent = fs.readFileSync(initPyPath, 'utf8');
    const versionLineRegex = /^__version__\s*=\s*"[^"]*"/m;

    if (versionLineRegex.test(initContent)) {
        initContent = initContent.replace(versionLineRegex, `__version__ = "${newVersion}"`);
    } else {
        initContent = `__version__ = "${newVersion}"\n` + initContent;
    }

    fs.writeFileSync(initPyPath, initContent);
    console.log(`✅ Synchronized version to ${newVersion} in __init__.py`);
}
