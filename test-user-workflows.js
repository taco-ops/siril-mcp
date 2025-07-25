const { MCPTestClient } = require('mcp-test-client');
const fs = require('fs');
const path = require('path');

class UserWorkflowTests {
    constructor() {
        this.client = null;
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
    }

    async disconnect() {
        if (this.client) {
            await this.client.disconnect();
        }
    }

    // Simulate: Complete workflow for a new user
    async testNewUserWorkflow() {
        console.log("🆕 Testing New User Workflow");
        console.log("Scenario: User just got a Seestar telescope and wants to process their first images");

        // Step 1: User asks "Do I have Siril installed?"
        console.log("\n1️⃣ Checking if Siril is installed...");
        try {
            const detection = await this.client.callTool("find_siril_binary", {});
            console.log("✅ Response:", detection.content[0]?.text || JSON.stringify(detection.content));
        } catch (error) {
            console.log("❌ Error:", error.message);
        }

        // Step 2: User asks "What version do I have?"
        console.log("\n2️⃣ Checking Siril version...");
        try {
            const version = await this.client.callTool("check_siril_version", {});
            console.log("✅ Response:", version.content[0]?.text || JSON.stringify(version.content));
        } catch (error) {
            console.log("❌ Error:", error.message);
        }

        // Step 3: User asks "Can you get me the latest processing scripts?"
        console.log("\n3️⃣ Downloading latest scripts...");
        const scriptDir = path.join(process.cwd(), 'new-user-project');
        fs.mkdirSync(scriptDir, { recursive: true });

        try {
            const scripts = await this.client.callTool("download_latest_ssf_scripts", {
                project_dir: scriptDir
            });
            console.log("✅ Response:", scripts.content[0]?.text || JSON.stringify(scripts.content));
        } catch (error) {
            console.log("❌ Error:", error.message);
        }

        // Step 4: User creates a project and asks to process
        console.log("\n4️⃣ Analyzing project structure...");
        const testDir = this.createMockProject("M42_Orion_Nebula");

        try {
            const structure = await this.client.callTool("check_project_structure", {
                project_dir: testDir
            });
            console.log("✅ Project Analysis:", structure.content[0]?.text || JSON.stringify(structure.content));
        } catch (error) {
            console.log("❌ Error:", error.message);
        }

        console.log("\n5️⃣ Processing first astrophoto...");
        try {
            const processing = await this.client.callTool("process_seestar_mosaic", {
                project_dir: testDir,
                filter_type: "broadband"
            });
            console.log("✅ Processing Result:", processing.content[0]?.text || JSON.stringify(processing.content));
        } catch (error) {
            console.log("❌ Error:", error.message);
        }

        // Cleanup
        fs.rmSync(testDir, { recursive: true, force: true });
        fs.rmSync(scriptDir, { recursive: true, force: true });
    }

    // Simulate: Advanced user trying different filters
    async testAdvancedUserWorkflow() {
        console.log("\n🔬 Testing Advanced User Workflow");
        console.log("Scenario: Experienced user wants to process narrowband nebula data");

        // User has custom Siril installation
        console.log("\n1️⃣ Validating custom Siril installation...");
        try {
            const validation = await this.client.callTool("validate_siril_binary", {
                binary_path: "/Applications/Siril.app/Contents/MacOS/Siril"
            });
            console.log("✅ Validation Result:", validation.content[0]?.text || JSON.stringify(validation.content));
        } catch (error) {
            console.log("❌ Error:", error.message);
        }

        // Process narrowband data
        console.log("\n2️⃣ Processing narrowband nebula data...");
        const testDir = this.createMockProject("IC1396_Elephant_Trunk", [
            "IC1396_Ha_001.fit",
            "IC1396_Ha_002.fit",
            "IC1396_OIII_001.fit",
            "IC1396_OIII_002.fit"
        ]);

        try {
            const processing = await this.client.callTool("process_seestar_mosaic", {
                project_dir: testDir,
                filter_type: "narrowband"
            });
            console.log("✅ Narrowband Processing:", processing.content[0]?.text || JSON.stringify(processing.content));
        } catch (error) {
            console.log("❌ Error:", error.message);
        }

        // Cleanup
        fs.rmSync(testDir, { recursive: true, force: true });
    }

    // Simulate: Troubleshooting workflow
    async testTroubleshootingWorkflow() {
        console.log("\n🔧 Testing Troubleshooting Workflow");
        console.log("Scenario: User is having problems and needs help");

        // User reports Siril not working
        console.log("\n1️⃣ User reports: 'Siril doesn't seem to be working'");
        try {
            const detection = await this.client.callTool("find_siril_binary", {});
            console.log("✅ Diagnostic Result:", detection.content[0]?.text || JSON.stringify(detection.content));
        } catch (error) {
            console.log("❌ Error:", error.message);
        }

        // Test a non-existent path
        console.log("\n2️⃣ User asks: 'Can you test this path: /usr/local/bin/siril'");
        try {
            const validation = await this.client.callTool("validate_siril_binary", {
                binary_path: "/usr/local/bin/siril"
            });
            console.log("✅ Path Test Result:", validation.content[0]?.text || JSON.stringify(validation.content));
        } catch (error) {
            console.log("❌ Error (expected):", error.message);
        }

        // Test with empty project
        console.log("\n3️⃣ User asks: 'Why isn't my project processing?'");
        const emptyDir = path.join(process.cwd(), 'empty-test');
        fs.mkdirSync(path.join(emptyDir, 'lights'), { recursive: true });

        try {
            const structure = await this.client.callTool("check_project_structure", {
                project_dir: emptyDir
            });
            console.log("✅ Empty Project Analysis:", structure.content[0]?.text || JSON.stringify(structure.content));
        } catch (error) {
            console.log("❌ Error:", error.message);
        }

        try {
            const processing = await this.client.callTool("process_seestar_mosaic", {
                project_dir: emptyDir,
                filter_type: "broadband"
            });
            console.log("✅ Processing Result:", processing.content[0]?.text || JSON.stringify(processing.content));
        } catch (error) {
            console.log("❌ Error (expected):", error.message);
        }

        // Cleanup
        fs.rmSync(emptyDir, { recursive: true, force: true });
    }

    createMockProject(name, fileNames = null) {
        const testDir = path.join(process.cwd(), `test-${name}`);
        const lightsDir = path.join(testDir, 'lights');

        fs.mkdirSync(lightsDir, { recursive: true });

        const defaultFiles = fileNames || [
            `${name}_light_001.fit`,
            `${name}_light_002.fit`,
            `${name}_light_003.fit`
        ];

        defaultFiles.forEach(filename => {
            fs.writeFileSync(path.join(lightsDir, filename), `MOCK_${name}_DATA`);
        });

        return testDir;
    }

    async runAllWorkflows() {
        await this.connect();

        try {
            await this.testNewUserWorkflow();
            await this.testAdvancedUserWorkflow();
            await this.testTroubleshootingWorkflow();
        } finally {
            await this.disconnect();
        }
    }
}

// Run the workflow tests
async function main() {
    const workflowTests = new UserWorkflowTests();
    await workflowTests.runAllWorkflows();
}

main().catch(console.error);
