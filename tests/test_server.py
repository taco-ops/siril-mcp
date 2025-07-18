"""Tests for the Siril MCP server."""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from siril_mcp.server import SSF_SCRIPTS, SSF_SCRIPT_CONTENTS


def test_ssf_scripts_defined():
    """Test that SSF scripts are properly defined."""
    assert "broadband" in SSF_SCRIPTS
    assert "narrowband" in SSF_SCRIPTS
    assert SSF_SCRIPTS["broadband"] == "Naztronomy-Seestar_Broadband_Mosaic.ssf"
    assert SSF_SCRIPTS["narrowband"] == "Naztronomy-Seestar_Narrowband_Mosaic.ssf"


def test_ssf_script_contents_defined():
    """Test that SSF script contents are properly defined."""
    assert "broadband" in SSF_SCRIPT_CONTENTS
    assert "narrowband" in SSF_SCRIPT_CONTENTS

    # Check that content is not empty
    assert len(SSF_SCRIPT_CONTENTS["broadband"]) > 100
    assert len(SSF_SCRIPT_CONTENTS["narrowband"]) > 100

    # Check that content contains expected Siril commands
    assert "convert light" in SSF_SCRIPT_CONTENTS["broadband"]
    assert "seqplatesolve" in SSF_SCRIPT_CONTENTS["broadband"]
    assert "stack r_light_" in SSF_SCRIPT_CONTENTS["broadband"]

    assert "convert light" in SSF_SCRIPT_CONTENTS["narrowband"]
    assert "seqplatesolve" in SSF_SCRIPT_CONTENTS["narrowband"]
    assert "stack r_light_" in SSF_SCRIPT_CONTENTS["narrowband"]


def test_broadband_vs_narrowband_differences():
    """Test that broadband and narrowband scripts have appropriate differences."""
    broadband = SSF_SCRIPT_CONTENTS["broadband"]
    narrowband = SSF_SCRIPT_CONTENTS["narrowband"]

    # Broadband should have UV/IR Block filter enabled and narrowband commented out
    assert 'spcc "-oscsensor=ZWO Seestar S50" "-oscfilter=UV/IR Block"' in broadband
    assert (
        '# Enable for Narrowband Only\n# spcc "-oscsensor=ZWO Seestar S50" -narrowband'
        in broadband
    )

    # Narrowband should have narrowband processing enabled and broadband commented out
    assert (
        '# Enable for Broadband only\n#spcc "-oscsensor=ZWO Seestar S50" "-oscfilter=UV/IR Block"'
        in narrowband
    )
    assert 'spcc "-oscsensor=ZWO Seestar S50" -narrowband' in narrowband


@patch("siril_mcp.server.subprocess.run")
def test_check_siril_version_success(mock_run):
    """Test successful Siril version check."""
    from siril_mcp.server import _check_siril_version

    # Mock successful subprocess call
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Siril 1.4.0-beta1"
    mock_run.return_value = mock_result

    result = _check_siril_version()
    assert result == "Siril 1.4.0-beta1"
    mock_run.assert_called_once_with(
        ["siril", "--version"],
        capture_output=True,
        text=True,
    )


@patch("siril_mcp.server.subprocess.run")
def test_check_siril_version_failure(mock_run):
    """Test failed Siril version check."""
    from siril_mcp.server import _check_siril_version

    # Mock failed subprocess call
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "siril: command not found"
    mock_run.return_value = mock_result

    with pytest.raises(RuntimeError, match="Error getting Siril version"):
        _check_siril_version()


def test_project_structure_validation():
    """Test project structure validation logic."""
    from siril_mcp.server import _process_seestar_mosaic

    with tempfile.TemporaryDirectory() as temp_dir:
        # Test missing lights directory
        with pytest.raises(FileNotFoundError, match="No 'lights' folder found"):
            _process_seestar_mosaic(temp_dir, "broadband")

        # Test invalid filter type
        lights_dir = os.path.join(temp_dir, "lights")
        os.makedirs(lights_dir)

        with pytest.raises(ValueError, match="Unknown filter_type"):
            _process_seestar_mosaic(temp_dir, "invalid_filter")


if __name__ == "__main__":
    pytest.main([__file__])
