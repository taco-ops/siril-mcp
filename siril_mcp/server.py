#!/usr/bin/env python3
import os
import shutil
import subprocess
from typing import Literal, Optional

from fastmcp import Context, FastMCP

mcp = FastMCP(name="Siril SeeStar Mosaic Processor")


# SSF Script contents from https://github.com/naztronaut/siril-scripts
# (C) Nazmus Nasir (Naztronomy.com) - Used under GPL-3.0 license
SSF_SCRIPT_CONTENTS = {
    "broadband": """#
# Script for Siril 1.4.0-beta1
#
# May 2025
# (C) Nazmus Nasir (Naztronomy.com)
# (C) Cyril Richard
#
# Naztronomy_Seestar_Broadband_Mosaic v1.0
#
########### PREPROCESSING SCRIPT ###########
#
# Script for Broadband mosaic preprocessing, see 
# other script for Narrowband mosaic preprocessing
# This script plate solves, aligns, stacks, then does SPCC
#
# Only needs a lights directory with .fit files from your Seestar:
#  lights/
#
############################################

requires 1.4.0-beta1

# Convert Light Frames to .fit files
cd lights
convert light -out=../process
cd ../process

# Platesolve 
seqplatesolve light_ -nocache -force -disto=ps_distortion

# Align lights
# Note: This seems to also debayer the sequence
seqapplyreg light_ -filter-round=2.5k -framing=max -drizzle -scale=1.0 -pixfrac=1.0 -kernel=square

# Stack calibrated lights to result.fit
stack r_light_ rej 3 3 -norm=addscale -output_norm -rgb_equal -maximize -feather=5 -out=result 

#save result using FITS keywords for the name
load result
save ../$OBJECT:%s$_$STACKCNT:%d$x$EXPTIME:%d$sec_$DATE-OBS:dt$_og

# Force platesolve for SPCC 
platesolve -force 

# Enable for Broadband only
spcc "-oscsensor=ZWO Seestar S50" "-oscfilter=UV/IR Block" -catalog=localgaia "-whiteref=Average Spiral Galaxy"

# Enable for Narrowband Only
# spcc "-oscsensor=ZWO Seestar S50" -narrowband -rwl=656.28 -rbw=20 -gwl=500.70 -gbw=30 -bwl=500.70 -bbw=30 -catalog=localgaia "-whiteref=Average Spiral Galaxy"

# Saved after SPCC 
save ../$OBJECT:%s$_$STACKCNT:%d$x$EXPTIME:%d$sec_$DATE-OBS:dt$_SPCC

# Autostretch is done just to show a good initial result
# To do your own stretch, load the _spcc file which is color calibrated or go back further and load the _og file
autostretch

# Alternative Stretch with GHS 
# uncomment to use - every image is different so autoghs doesn't always work as expected
# autoghs 0 145 -b=5

# LOAD _SPCC file to do your own stretch and _og file to do your own SPCC. 
#
# https://www.Naztronomy.com
# https://www.YouTube.com/Naztronomy 
############################################
""",
    "narrowband": """#
# Script for Siril 1.4.0-beta1
#
# May 2025
# (C) Nazmus Nasir (Naztronomy.com)
# (C) Cyril Richard
#
# Naztronomy_Seestar_Narrowband_Mosaic v1.0
#
########### PREPROCESSING SCRIPT ###########
#
# Script for Narrowband mosaic preprocessing, see 
# other script for Broadband mosaic preprocessing
# This script plate solves, aligns, stacks, then does SPCC
#
# Only needs a lights directory with .fit files from your Seestar:
#  lights/
#
############################################

requires 1.4.0-beta1

# Convert Light Frames to .fit files
cd lights
convert light -out=../process
cd ../process

# Platesolve 
seqplatesolve light_ -nocache -force -disto=ps_distortion

# Align lights
# Note: This seems to also debayer the sequence
seqapplyreg light_ -filter-round=2.5k -framing=max -drizzle -scale=1.0 -pixfrac=1.0 -kernel=square

# Stack calibrated lights to result.fit
stack r_light_ rej 3 3 -norm=addscale -output_norm -rgb_equal -maximize -feather=5 -out=result 

#save result using FITS keywords for the name
load result
save ../$OBJECT:%s$_$STACKCNT:%d$x$EXPTIME:%d$sec_$DATE-OBS:dt$_og

# Force platesolve for SPCC 
platesolve -force 

# Enable for Broadband only
#spcc "-oscsensor=ZWO Seestar S50" "-oscfilter=UV/IR Block" -catalog=localgaia "-whiteref=Average Spiral Galaxy"

# Enable for Narrowband Only 
spcc "-oscsensor=ZWO Seestar S50" -narrowband -rwl=656.28 -rbw=20 -gwl=500.70 -gbw=30 -bwl=500.70 -bbw=30 -catalog=localgaia "-whiteref=Average Spiral Galaxy"

# Saved after SPCC 
save ../$OBJECT:%s$_$STACKCNT:%d$x$EXPTIME:%d$sec_$DATE-OBS:dt$_SPCC

# Autostretch is done just to show a good initial result
# To do your own stretch, load the _spcc file which is color calibrated or go back further and load the _og file
autostretch

# Alternative Stretch with GHS 
# uncomment to use - every image is different so autoghs doesn't always work as expected
# autoghs 0 145 -b=5

# LOAD _SPCC file to do your own stretch and _og file to do your own SPCC. 
#
# https://www.Naztronomy.com
# https://www.YouTube.com/Naztronomy 
############################################
""",
}

SSF_SCRIPTS = {
    "broadband": "Naztronomy-Seestar_Broadband_Mosaic.ssf",  # UV/IR block
    "narrowband": "Naztronomy-Seestar_Narrowband_Mosaic.ssf",  # LP filter
}


def _find_siril_binary() -> str:
    """
    Find the Siril binary in common locations.

    Returns the path to the Siril executable, checking:
    1. SIRIL_BINARY environment variable (if set)
    2. PATH environment variable (siril command)
    3. macOS app bundle location
    4. Common Linux/Windows locations

    Raises RuntimeError if Siril cannot be found.
    """
    # First check if user specified a custom binary path via environment variable
    custom_binary = os.environ.get("SIRIL_BINARY")
    if custom_binary:
        if os.path.isfile(custom_binary) and os.access(custom_binary, os.X_OK):
            return custom_binary
        else:
            raise RuntimeError(
                f"Custom Siril binary specified in SIRIL_BINARY environment variable "
                f"is not found or not executable: {custom_binary}"
            )

    # Check if 'siril' is in PATH
    siril_path = shutil.which("siril")
    if siril_path:
        return siril_path

    # Common locations to check
    possible_locations = [
        # macOS app bundle
        "/Applications/Siril.app/Contents/MacOS/Siril",
        # Alternative macOS locations
        "/usr/local/bin/siril",
        "/opt/homebrew/bin/siril",
        # Linux locations
        "/usr/bin/siril",
        "/usr/local/bin/siril",
        # Windows locations (if running under WSL or similar)
        "/mnt/c/Program Files/Siril/siril.exe",
        "/mnt/c/Program Files (x86)/Siril/siril.exe",
    ]

    for location in possible_locations:
        if os.path.isfile(location) and os.access(location, os.X_OK):
            return location

    # If we get here, Siril wasn't found
    raise RuntimeError(
        "Siril binary not found. Please ensure Siril is installed and either:\n"
        "1. Add 'siril' to your PATH, or\n"
        "2. Install Siril in a standard location like /Applications/Siril.app (macOS), or\n"
        "3. Set the SIRIL_BINARY environment variable to the full path of your Siril binary\n"
        f"Searched locations: {possible_locations}"
    )


def _check_siril_version() -> str:
    """
    Internal function to check Siril version.
    Separated for easier testing.
    """
    siril_binary = _find_siril_binary()
    proc = subprocess.run(
        [siril_binary, "--version"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        # Fail the tool call so the client sees an error
        raise RuntimeError(f"Error getting Siril version: {proc.stderr.strip()}")
    return proc.stdout.strip()


@mcp.tool
def check_siril_version() -> str:
    """
    Runs 'siril --version' on the local machine and returns the version string.
    """
    return _check_siril_version()


@mcp.tool
async def find_siril_binary(ctx: Context) -> str:
    """
    Locates the Siril binary on your system and returns its path.
    This is useful for troubleshooting installation issues or confirming
    which version of Siril will be used.
    """
    try:
        await ctx.info("Searching for Siril binary...")
        siril_path = _find_siril_binary()
        await ctx.info(f"Found Siril binary at: {siril_path}")

        # Test that we can actually run it
        await ctx.debug("Testing Siril binary...")
        proc = subprocess.run(
            [siril_path, "--version"], capture_output=True, text=True, timeout=10
        )
        if proc.returncode == 0:
            version_info = proc.stdout.strip()
            await ctx.info("Siril binary test successful")
            return f"✅ Found working Siril binary at: {siril_path}\n{version_info}"
        else:
            await ctx.error(f"Siril binary test failed: {proc.stderr.strip()}")
            return f"⚠️ Found Siril binary at {siril_path} but it failed to run: {proc.stderr.strip()}"
    except Exception as e:
        await ctx.error(f"Error finding Siril binary: {str(e)}")
        return f"❌ {str(e)}"


@mcp.tool
async def validate_siril_binary(binary_path: str, ctx: Context) -> str:
    """
    Tests whether a specific Siril binary path works correctly.
    Useful for validating custom installations or non-standard locations.

    :param binary_path: Full path to the Siril binary to test
    """
    await ctx.info(f"Validating Siril binary at: {binary_path}")

    if not os.path.isfile(binary_path):
        await ctx.error(f"File not found: {binary_path}")
        return f"❌ File not found: {binary_path}"

    if not os.access(binary_path, os.X_OK):
        await ctx.error(f"File is not executable: {binary_path}")
        return f"❌ File is not executable: {binary_path}"

    try:
        await ctx.debug("Testing binary execution...")
        proc = subprocess.run(
            [binary_path, "--version"], capture_output=True, text=True, timeout=10
        )
        if proc.returncode == 0:
            version_info = proc.stdout.strip()
            await ctx.info("Binary validation successful")
            return (
                f"✅ Siril binary works correctly!\nPath: {binary_path}\n{version_info}"
            )
        else:
            await ctx.error(f"Binary execution failed: {proc.stderr.strip()}")
            return f"❌ Binary failed to run: {proc.stderr.strip()}"
    except subprocess.TimeoutExpired:
        await ctx.error("Binary execution timed out")
        return f"❌ Binary timed out (may be hanging)"
    except Exception as e:
        await ctx.error(f"Error testing binary: {str(e)}")
        return f"❌ Error testing binary: {str(e)}"


def _process_seestar_mosaic(
    project_dir: str,
    filter_type: str = "broadband",
) -> str:
    """
    Internal function to process Seestar mosaic.
    Separated for easier testing.
    """
    # Validate inputs
    ssf_name = SSF_SCRIPTS.get(filter_type)
    if ssf_name is None:
        raise ValueError(f"Unknown filter_type '{filter_type}'")
    lights_dir = os.path.join(project_dir, "lights")
    if not os.path.isdir(lights_dir):
        raise FileNotFoundError(f"No 'lights' folder found at {lights_dir}")

    # Change into the project dir so Siril picks up the .ssf script automatically
    cwd = os.getcwd()
    try:
        os.chdir(project_dir)

        # Create the SSF script file if it doesn't exist
        ssf_path = os.path.join(project_dir, ssf_name)
        if not os.path.isfile(ssf_path):
            with open(ssf_path, "w", encoding="utf-8") as f:
                f.write(SSF_SCRIPT_CONTENTS[filter_type])

        # Invoke Siril in batch/script mode
        siril_binary = _find_siril_binary()
        cmd = [siril_binary, "-s", ssf_name]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"Siril failed:\n{proc.stderr}")

        # By convention the script writes its mosaic into a 'process/' subdir
        # with a predictable name—adjust if the script differs.
        output_path = os.path.join(project_dir, "process", "mosaic.fits")
        if not os.path.isfile(output_path):
            # Note: Can't log here since this is not an async function
            pass
        return output_path
    finally:
        os.chdir(cwd)


@mcp.tool
async def process_seestar_mosaic(
    project_dir: str,
    filter_type: Literal["broadband", "narrowband"] = "broadband",
    ctx: Context = None,
) -> str:
    """
    Runs the appropriate Siril .ssf mosaic script on all FIT(S) in project_dir/lights,
    stacking them into a mosaic according to Seestar S30/S50 conventions.

    This function automatically creates the required SSF script files in your project
    directory, so you don't need to manually download them from the repository.

    :param project_dir: path to your project root (must contain a 'lights/' subdir)
    :param filter_type: 'broadband' for UV/IR block or 'narrowband' for LP filter
    :returns: path to the resulting mosaic FIT
    """
    if ctx:
        await ctx.info(f"Starting Seestar mosaic processing in {project_dir}")
        await ctx.info(f"Filter type: {filter_type}")

    try:
        result = _process_seestar_mosaic(project_dir, filter_type)
        if ctx:
            await ctx.info(f"Mosaic processing completed successfully")
        return result
    except Exception as e:
        if ctx:
            await ctx.error(f"Mosaic processing failed: {str(e)}")
        raise


@mcp.tool
def preprocess_with_gui(project_dir: str) -> str:
    """
    Launches the full Naztronomy-Smart_Telescope_PP.py GUI in headless mode.
    (Requires sirilpy installed and a display server.)
    """
    script = "Naztronomy-Smart_Telescope_PP.py"
    # You might run this via your virtualenv / pipenv
    cmd = ["python3", script, "--headless", project_dir]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"GUI script failed:\n{proc.stderr}")
    return f"Completed GUI-driven preprocessing in {project_dir}"


@mcp.tool
async def download_latest_ssf_scripts(project_dir: str, ctx: Context) -> str:
    """
    Downloads the latest SSF script files from the naztronaut/siril-scripts repository
    and saves them to your project directory. This ensures you have the most up-to-date
    versions of the Siril scripts.

    :param project_dir: path to your project root where scripts will be saved
    :returns: confirmation message with script locations
    """
    import urllib.request

    await ctx.info(f"Downloading latest SSF scripts to {project_dir}")
    base_url = "https://raw.githubusercontent.com/naztronaut/siril-scripts/main/"
    scripts_downloaded = []

    for filter_type, script_name in SSF_SCRIPTS.items():
        try:
            script_url = base_url + script_name
            script_path = os.path.join(project_dir, script_name)

            await ctx.info(f"Downloading {script_name} from {script_url}")
            urllib.request.urlretrieve(script_url, script_path)
            scripts_downloaded.append(script_name)

        except Exception as e:
            await ctx.warning(f"Failed to download {script_name}: {e}")
            # Fall back to embedded version
            await ctx.info(f"Creating fallback version of {script_name}")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(SSF_SCRIPT_CONTENTS[filter_type])
            scripts_downloaded.append(f"{script_name} (fallback)")

    result = f"Downloaded scripts to {project_dir}: {', '.join(scripts_downloaded)}"
    await ctx.info("Script download completed")
    return result


@mcp.tool
def check_project_structure(project_dir: str) -> str:
    """
    Checks and displays the structure of a Seestar project directory,
    showing what files are present and what might be missing.

    :param project_dir: path to your project root
    :returns: detailed project structure analysis
    """
    if not os.path.isdir(project_dir):
        return f"❌ Project directory '{project_dir}' does not exist"

    analysis = [f"📁 Project Directory: {project_dir}\n"]

    # Check for lights directory
    lights_dir = os.path.join(project_dir, "lights")
    if os.path.isdir(lights_dir):
        fits_files = [
            f for f in os.listdir(lights_dir) if f.lower().endswith((".fit", ".fits"))
        ]
        analysis.append(f"✅ lights/ directory found with {len(fits_files)} FITS files")
        if fits_files:
            analysis.append(
                f"   Sample files: {', '.join(fits_files[:3])}{'...' if len(fits_files) > 3 else ''}"
            )
    else:
        analysis.append("❌ lights/ directory not found - this is required!")

    # Check for process directory
    process_dir = os.path.join(project_dir, "process")
    if os.path.isdir(process_dir):
        process_files = os.listdir(process_dir)
        analysis.append(f"📁 process/ directory found with {len(process_files)} files")
        if process_files:
            analysis.append(
                f"   Contents: {', '.join(process_files[:5])}{'...' if len(process_files) > 5 else ''}"
            )
    else:
        analysis.append(
            "📁 process/ directory will be created automatically during processing"
        )

    # Check for SSF scripts
    analysis.append("\n🔧 SSF Scripts:")
    for filter_type, script_name in SSF_SCRIPTS.items():
        script_path = os.path.join(project_dir, script_name)
        if os.path.isfile(script_path):
            analysis.append(f"✅ {script_name} (for {filter_type} processing)")
        else:
            analysis.append(
                f"📝 {script_name} will be created automatically (for {filter_type} processing)"
            )

    # General file listing
    try:
        all_files = [
            f
            for f in os.listdir(project_dir)
            if os.path.isfile(os.path.join(project_dir, f))
        ]
        if all_files:
            analysis.append(
                f"\n📄 Other files in project root: {', '.join(all_files[:10])}{'...' if len(all_files) > 10 else ''}"
            )
    except PermissionError:
        analysis.append("\n⚠️ Permission denied reading project directory")

    return "\n".join(analysis)


def main():
    """Entry point for the siril-mcp command."""
    mcp.run()


if __name__ == "__main__":
    # By default this uses STDIO transport, perfect for local CLI integration
    main()
