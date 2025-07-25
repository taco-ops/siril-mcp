#!/usr/bin/env node

/**
 * Integration Test for Siril MCP Server
 * Tests the actual MCP server functionality by running it and making requests
 */

const { spawn } = require('child_process');
const { createInterface } = require('readline');
const fs = require('fs');
const path = require('path');

class MCPIntegrationTester {
    constructor() {
        this.serverProcess = null;
        this.responses = [];
        this.requestId = 1;
    }

    async startServer() {
        console.log('🚀 Starting MCP Server...');

        return new Promise((resolve, reject) => {
            this.serverProcess = spawn('pipenv', ['run', 'python', '-m', 'siril_mcp.server'], {
                stdio: ['pipe', 'pipe', 'pipe'],
                cwd: process.cwd()
            });

            const rl = createInterface({
                input: this.serverProcess.stdout,
                crlfDelay: Infinity
            });

            let initializationComplete = false;
            let initializeResponseReceived = false;

            rl.on('line', (line) => {
                try {
                    const response = JSON.parse(line);
                    this.responses.push(response);

                    // Check for initialization response
                    if (response.result && response.result.capabilities && !initializeResponseReceived) {
                        initializeResponseReceived = true;
                        console.log('✅ Initialization response received');

                        // Send initialized notification
                        this.sendRequest({
                            jsonrpc: "2.0",
                            method: "notifications/initialized"
                        });

                        // Wait a bit then mark as complete
                        setTimeout(() => {
                            initializationComplete = true;
                            console.log('✅ MCP Server initialization complete');
                            resolve();
                        }, 500);
                    }
                } catch (e) {
                    // Ignore non-JSON lines
                }
            });

            this.serverProcess.stderr.on('data', (data) => {
                console.error('Server stderr:', data.toString());
            });

            this.serverProcess.on('error', (error) => {
                reject(error);
            });

            // Send initialization request after a brief delay
            setTimeout(() => {
                this.sendRequest({
                    jsonrpc: "2.0",
                    id: this.requestId++,
                    method: "initialize",
                    params: {
                        protocolVersion: "2024-11-05",
                        capabilities: {
                            roots: {
                                listChanged: true
                            },
                            sampling: {}
                        },
                        clientInfo: {
                            name: "test-client",
                            version: "1.0.0"
                        }
                    }
                });
            }, 500);
        });
    }

    sendRequest(request) {
        if (this.serverProcess && this.serverProcess.stdin.writable) {
            this.serverProcess.stdin.write(JSON.stringify(request) + '\n');
        }
    }

    async testListTools() {
        console.log('\n🔧 Testing tools/list...');

        return new Promise((resolve) => {
            this.sendRequest({
                jsonrpc: "2.0",
                id: this.requestId++,
                method: "tools/list"
            });

            // Wait for response
            setTimeout(() => {
                const listResponse = this.responses.find(r => r.result && r.result.tools);
                if (listResponse && listResponse.result.tools.length > 0) {
                    console.log(`✅ Found ${listResponse.result.tools.length} tools:`);
                    listResponse.result.tools.forEach(tool => {
                        console.log(`   - ${tool.name}: ${tool.description}`);
                    });
                    resolve(true);
                } else {
                    console.log('❌ No tools found in response');
                    resolve(false);
                }
            }, 1000);
        });
    }

    async testFindSirilBinary() {
        console.log('\n🔍 Testing find_siril_binary tool...');

        const isCI = process.env.CI === 'true';

        return new Promise((resolve) => {
            this.sendRequest({
                jsonrpc: "2.0",
                id: this.requestId++,
                method: "tools/call",
                params: {
                    name: "find_siril_binary",
                    arguments: {}
                }
            });

            setTimeout(() => {
                const callResponse = this.responses.find(r =>
                    r.result && r.result.content && r.result.content[0] &&
                    r.result.content[0].text
                );

                if (callResponse) {
                    const responseText = callResponse.result.content[0].text;
                    if (isCI) {
                        console.log('✅ find_siril_binary tool executed (CI environment)');
                        console.log('   Result:', responseText.substring(0, 100) + '...');
                        // In CI, we expect this might fail but the tool should respond
                        resolve(true);
                    } else {
                        console.log('✅ find_siril_binary tool executed successfully');
                        console.log('   Result:', responseText.substring(0, 100) + '...');
                        resolve(responseText.includes('Siril') || responseText.includes('Found'));
                    }
                } else {
                    console.log('❌ find_siril_binary tool failed');
                    resolve(false);
                }
            }, 2000);
        });
    }

    async testCheckProjectStructure() {
        console.log('\n📁 Testing check_project_structure tool...');

        // Create a test project structure
        const testDir = path.join(process.cwd(), 'test-mcp-project');
        const lightsDir = path.join(testDir, 'lights');

        try {
            fs.mkdirSync(lightsDir, { recursive: true });
            fs.writeFileSync(path.join(lightsDir, 'test.fit'), 'MOCK_FITS_DATA');

            return new Promise((resolve) => {
                this.sendRequest({
                    jsonrpc: "2.0",
                    id: this.requestId++,
                    method: "tools/call",
                    params: {
                        name: "check_project_structure",
                        arguments: {
                            project_dir: testDir
                        }
                    }
                });

                setTimeout(() => {
                    const callResponse = this.responses.find(r =>
                        r.result && r.result.content && r.result.content[0] &&
                        r.result.content[0].text && r.result.content[0].text.includes('lights/')
                    );

                    if (callResponse) {
                        console.log('✅ check_project_structure tool executed successfully');
                        console.log('   Result:', callResponse.result.content[0].text.substring(0, 150) + '...');
                        resolve(true);
                    } else {
                        console.log('❌ check_project_structure tool failed');
                        resolve(false);
                    }

                    // Cleanup
                    fs.rmSync(testDir, { recursive: true, force: true });
                }, 2000);
            });
        } catch (error) {
            console.log('❌ Failed to setup test project:', error.message);
            return false;
        }
    }

    async runAllTests() {
        try {
            console.log('🎯 MCP Integration Testing');
            console.log('===========================\n');

            await this.startServer();

            const results = [];
            results.push(await this.testListTools());
            results.push(await this.testFindSirilBinary());
            results.push(await this.testCheckProjectStructure());

            const passed = results.filter(r => r).length;
            const total = results.length;

            console.log('\n📊 Test Results');
            console.log('================');
            console.log(`✅ Passed: ${passed}/${total}`);

            if (passed === total) {
                console.log('🎉 All MCP integration tests passed!');
            } else {
                console.log('❌ Some tests failed');
            }

        } catch (error) {
            console.error('❌ Test suite failed:', error);
        } finally {
            this.cleanup();
        }
    }

    cleanup() {
        if (this.serverProcess) {
            console.log('\n🧹 Cleaning up...');
            this.serverProcess.kill();
        }
    }
}

// Run the tests
async function main() {
    const tester = new MCPIntegrationTester();
    await tester.runAllTests();
}

main().catch(console.error);
