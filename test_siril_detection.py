#!/usr/bin/env python3
"""
Test script to verify Siril binary detection functionality.
"""
import os
import shutil
import sys

# Add the current directory to path so we can import our module
sys.path.insert(0, ".")


def test_siril_detection():
    """Test the Siril binary detection logic"""
    print("🔍 Testing Siril binary detection...\n")

    # Test 1: Check SIRIL_BINARY environment variable
    custom_binary = os.environ.get("SIRIL_BINARY")
    print(f"1. SIRIL_BINARY env var: {custom_binary}")

    # Test 2: Check if siril is in PATH
    siril_path = shutil.which("siril")
    print(f"2. siril in PATH: {siril_path}")

    # Test 3: Check macOS app bundle
    macos_siril = "/Applications/Siril.app/Contents/MacOS/Siril"
    if os.path.isfile(macos_siril) and os.access(macos_siril, os.X_OK):
        print(f"3. ✅ Found macOS Siril: {macos_siril}")
    else:
        print(f"3. ❌ macOS Siril not found: {macos_siril}")

    # Test 4: Test our actual function
    print("\n4. Testing our _find_siril_binary() function:")
    try:
        from siril_mcp.server import _find_siril_binary

        binary = _find_siril_binary()
        print(f"   ✅ Function returned: {binary}")

        # Test 5: Test version check
        print("\n5. Testing version check with detected binary:")
        import subprocess

        proc = subprocess.run(
            [binary, "--version"], capture_output=True, text=True, timeout=10
        )
        if proc.returncode == 0:
            version_info = proc.stdout.strip()
            print("   ✅ Version check successful:")
            print(f"   {version_info}")
        else:
            print(f"   ❌ Version check failed: {proc.stderr.strip()}")

    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        print("   This suggests fastmcp is not installed or not in the Python path")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 6: Test the async find_siril_binary tool (simplified test)
    print("\n6. Testing async tool import:")
    try:
        # Just test that the module can be imported, don't import the function
        from siril_mcp import server  # noqa: F401

        print("   ✅ Successfully imported siril_mcp.server module")
        print(
            "   Note: find_siril_binary is an async function that requires "
            "a Context parameter"
        )
        print(
            "         Use 'pipenv run python -m siril_mcp.server' to run "
            "the full MCP server"
        )
    except Exception as e:
        print(f"   ❌ Error importing module: {e}")

    print("\n" + "=" * 60)
    print("Test completed!")


if __name__ == "__main__":
    test_siril_detection()
