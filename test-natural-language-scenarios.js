const { MCPTestClient } = require('mcp-test-client');
const fs = require('fs');
const path = require('path');

class NaturalLanguageTestSuite {
    constructor() {
        this.client = null;
        this.testResults = [];
    }

    async connect() {
        this.client = new MCPTestClient({
            name: "siril-mcp-server",
            command: "python",
            args: ["-m", "siril_mcp.server"],
            env: {
                PYTHONPATH: process.cwd(),
                SIRIL_BINARY: "/Applications/Siril.app/Contents/MacOS/Siril"
            }
        });
        await this.client.connect();
        console.log("🔌 Connected to Siril MCP server");
    }

    async disconnect() {
        if (this.client) {
            await this.client.disconnect();
        }
    }

    async runTest(testName, description, toolCall) {
        console.log(`\n🧪 ${testName}`);
        console.log(`📝 Scenario: ${description}`);
        
        try {
            const startTime = Date.now();
            const result = await toolCall();
            const duration = Date.now() - startTime;
            
            console.log(`✅ Success (${duration}ms)`);
            console.log(`📤 Result: ${JSON.stringify(result.content, null, 2)}`);
            
            this.testResults.push({
                test: testName,
                status: 'PASS',
                duration,
                result: result.content
            });
            
        } catch (error) {
            console.log(`❌ Failed: ${error.message}`);
            this.testResults.push({
                test: testName,
                status: 'FAIL',
                error: error.message
            });
        }
    }

    // Simulate: "Can you check if Siril is installed on my system?"
    async testSirilDetection() {
        await this.runTest(
            "Siril Detection",
            "User asks: 'Can you check if Siril is installed on my system?'",
            () => this.client.callTool("find_siril_binary", {})
        );
    }

    // Simulate: "What version of Siril do I have installed?"
    async testVersionCheck() {
        await this.runTest(
            "Version Check",
            "User asks: 'What version of Siril do I have installed?'",
            () => this.client.callTool("check_siril_version", {})
        );
    }

    // Simulate: "I have Siril installed at a custom location, can you verify it works?"
    async testCustomBinaryValidation() {
        await this.runTest(
            "Custom Binary Validation",
            "User asks: 'I have Siril installed at /Applications/Siril.app/Contents/MacOS/Siril, can you verify it works?'",
            () => this.client.callTool("validate_siril_binary", {
                binary_path: "/Applications/Siril.app/Contents/MacOS/Siril"
            })
        );
    }

    // Simulate: "Can you test if this random path has a working Siril?"
    async testInvalidBinaryValidation() {
        await this.runTest(
            "Invalid Binary Test",
            "User asks: 'Can you test if /usr/bin/nonexistent has a working Siril?'",
            () => this.client.callTool("validate_siril_binary", {
                binary_path: "/usr/bin/nonexistent"
            })
        );
    }

    // Simulate: "Please download the latest Siril scripts for processing my images"
    async testScriptDownload() {
        const testDir = path.join(process.cwd(), 'test-script-download');
        fs.mkdirSync(testDir, { recursive: true });

        await this.runTest(
            "Script Download",
            "User asks: 'Please download the latest Siril scripts for processing my images'",
            () => this.client.callTool("download_latest_ssf_scripts", {
                project_dir: testDir
            })
        );

        // Cleanup
        fs.rmSync(testDir, { recursive: true, force: true });
    }

    // Simulate: "Can you analyze my project structure to see if it's ready for processing?"
    async testProjectStructureCheck() {
        const testDir = path.join(process.cwd(), 'test-project-structure');
        const lightsDir = path.join(testDir, 'lights');
        
        // Create test project structure
        fs.mkdirSync(lightsDir, { recursive: true });
        fs.writeFileSync(path.join(lightsDir, 'M31_001.fit'), 'MOCK_DATA');
        fs.writeFileSync(path.join(lightsDir, 'M31_002.fit'), 'MOCK_DATA');

        await this.runTest(
            "Project Structure Check",
            "User asks: 'Can you analyze my project structure to see if it's ready for processing?'",
            () => this.client.callTool("check_project_structure", {
                project_dir: testDir
            })
        );

        // Cleanup
        fs.rmSync(testDir, { recursive: true, force: true });
    }

    // Simulate: "I have Seestar telescope images in a folder, can you process them?"
    async testMosaicProcessingBroadband() {
        // Create a realistic test project structure
        const testDir = path.join(process.cwd(), 'test-seestar-data');
        const lightsDir = path.join(testDir, 'lights');
        
        // Setup test data
        fs.mkdirSync(lightsDir, { recursive: true });
        
        // Create mock .fit files with realistic names
        const mockFiles = [
            'M31_light_01.fit',
            'M31_light_02.fit', 
            'M31_light_03.fit'
        ];
        
        mockFiles.forEach(filename => {
            fs.writeFileSync(path.join(lightsDir, filename), 'MOCK_FIT_DATA');
        });

        await this.runTest(
            "Broadband Mosaic Processing",
            "User asks: 'I have Seestar telescope images of M31 in my project folder, can you process them as a broadband mosaic?'",
            () => this.client.callTool("process_seestar_mosaic", {
                project_dir: testDir,
                filter_type: "broadband"
            })
        );

        // Cleanup
        fs.rmSync(testDir, { recursive: true, force: true });
    }

    // Simulate: "What happens if I try to process a folder that doesn't exist?"
    async testInvalidProjectDir() {
        await this.runTest(
            "Invalid Project Directory",
            "User asks: 'What happens if I try to process a folder that doesn't exist?'",
            () => this.client.callTool("process_seestar_mosaic", {
                project_dir: "/path/that/does/not/exist",
                filter_type: "broadband"
            })
        );
    }

    // Simulate: "List all the tools you have available for astrophotography"
    async testToolDiscovery() {
        await this.runTest(
            "Tool Discovery",
            "User asks: 'List all the tools you have available for astrophotography'",
            async () => {
                const tools = await this.client.listTools();
                return {
                    content: [{
                        type: "text",
                        text: `Available tools:\n${tools.map(t => 
                            `• ${t.name}: ${t.description}`
                        ).join('\n')}`
                    }]
                };
            }
        );
    }

    async runAllTests() {
        console.log("🚀 Starting Natural Language MCP Test Suite");
        console.log("=" .repeat(60));

        await this.connect();

        try {
            // Basic functionality tests
            await this.testSirilDetection();
            await this.testVersionCheck();
            await this.testCustomBinaryValidation();
            await this.testInvalidBinaryValidation();
            
            // Script management tests
            await this.testScriptDownload();
            await this.testProjectStructureCheck();
            
            // Processing tests
            await this.testMosaicProcessingBroadband();
            
            // Error handling tests
            await this.testInvalidProjectDir();
            
            // Discovery tests
            await this.testToolDiscovery();

        } finally {
            await this.disconnect();
        }

        this.printSummary();
    }

    printSummary() {
        console.log("\n" + "=" .repeat(60));
        console.log("📊 TEST SUMMARY");
        console.log("=" .repeat(60));

        const passed = this.testResults.filter(r => r.status === 'PASS').length;
        const failed = this.testResults.filter(r => r.status === 'FAIL').length;
        
        console.log(`✅ Passed: ${passed}`);
        console.log(`❌ Failed: ${failed}`);
        console.log(`📈 Success Rate: ${(passed / this.testResults.length * 100).toFixed(1)}%`);

        if (failed > 0) {
            console.log("\n❌ FAILED TESTS:");
            this.testResults.filter(r => r.status === 'FAIL').forEach(test => {
                console.log(`  • ${test.test}: ${test.error}`);
            });
        }

        console.log("\n⏱️  PERFORMANCE:");
        this.testResults.filter(r => r.duration).forEach(test => {
            console.log(`  • ${test.test}: ${test.duration}ms`);
        });
    }
}

// Run the test suite
async function main() {
    const testSuite = new NaturalLanguageTestSuite();
    await testSuite.runAllTests();
}

main().catch(console.error);
