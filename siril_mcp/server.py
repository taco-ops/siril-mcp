#!/usr/bin/env python3
import os
import subprocess
from typing import Literal

from fastmcp import FastMCP

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


def _check_siril_version() -> str:
    """
    Internal function to check Siril version.
    Separated for easier testing.
    """
    proc = subprocess.run(
        ["siril", "--version"],
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
            mcp.log(f"Creating {ssf_name} script in {project_dir}")
            with open(ssf_path, "w", encoding="utf-8") as f:
                f.write(SSF_SCRIPT_CONTENTS[filter_type])

        # Invoke Siril in batch/script mode
        cmd = ["siril", "-s", ssf_name]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"Siril failed:\n{proc.stderr}")

        # By convention the script writes its mosaic into a 'process/' subdir
        # with a predictable name—adjust if the script differs.
        output_path = os.path.join(project_dir, "process", "mosaic.fits")
        if not os.path.isfile(output_path):
            mcp.log(f"⚠️ Mosaic script completed but no '{output_path}' found.")
        return output_path
    finally:
        os.chdir(cwd)


@mcp.tool
def process_seestar_mosaic(
    project_dir: str,
    filter_type: Literal["broadband", "narrowband"] = "broadband",
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
    return _process_seestar_mosaic(project_dir, filter_type)


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
def download_latest_ssf_scripts(project_dir: str) -> str:
    """
    Downloads the latest SSF script files from the naztronaut/siril-scripts repository
    and saves them to your project directory. This ensures you have the most up-to-date
    versions of the Siril scripts.

    :param project_dir: path to your project root where scripts will be saved
    :returns: confirmation message with script locations
    """
    import urllib.request

    base_url = "https://raw.githubusercontent.com/naztronaut/siril-scripts/main/"
    scripts_downloaded = []

    for filter_type, script_name in SSF_SCRIPTS.items():
        try:
            script_url = base_url + script_name
            script_path = os.path.join(project_dir, script_name)

            mcp.log(f"Downloading {script_name} from {script_url}")
            urllib.request.urlretrieve(script_url, script_path)
            scripts_downloaded.append(script_name)

        except Exception as e:
            mcp.log(f"⚠️ Failed to download {script_name}: {e}")
            # Fall back to embedded version
            mcp.log(f"Creating fallback version of {script_name}")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(SSF_SCRIPT_CONTENTS[filter_type])
            scripts_downloaded.append(f"{script_name} (fallback)")

    return f"Downloaded scripts to {project_dir}: {', '.join(scripts_downloaded)}"


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
