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


@patch("siril_mcp.server._find_siril_binary")
@patch("siril_mcp.server.subprocess.run")
def test_check_siril_version_success(mock_run, mock_find_binary):
    """Test successful Siril version check."""
    from siril_mcp.server import _check_siril_version

    # Mock the binary finder to return a specific path
    mock_find_binary.return_value = "/Applications/Siril.app/Contents/MacOS/Siril"
    
    # Mock successful subprocess call
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "Siril 1.4.0-beta1"
    mock_run.return_value = mock_result

    result = _check_siril_version()
    assert result == "Siril 1.4.0-beta1"
    
    # Verify that _find_siril_binary was called
    mock_find_binary.assert_called_once()
    
    # Verify subprocess was called with the found binary path
    mock_run.assert_called_once_with(
        ["/Applications/Siril.app/Contents/MacOS/Siril", "--version"],
        capture_output=True,
        text=True,
    )


@patch("siril_mcp.server._find_siril_binary")
@patch("siril_mcp.server.subprocess.run")
def test_check_siril_version_failure(mock_run, mock_find_binary):
    """Test failed Siril version check."""
    from siril_mcp.server import _check_siril_version

    # Mock the binary finder to return a specific path
    mock_find_binary.return_value = "/Applications/Siril.app/Contents/MacOS/Siril"
    
    # Mock failed subprocess call
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = "siril: command not found"
    mock_run.return_value = mock_result

    with pytest.raises(RuntimeError, match="Error getting Siril version"):
        _check_siril_version()


@patch("siril_mcp.server.os.environ.get")
@patch("siril_mcp.server.shutil.which")
@patch("siril_mcp.server.os.path.isfile")
@patch("siril_mcp.server.os.access")
def test_find_siril_binary_env_var(mock_access, mock_isfile, mock_which, mock_env_get):
    """Test _find_siril_binary with SIRIL_BINARY environment variable."""
    from siril_mcp.server import _find_siril_binary
    
    # Mock environment variable
    mock_env_get.return_value = "/custom/path/to/siril"
    mock_isfile.return_value = True
    mock_access.return_value = True
    
    result = _find_siril_binary()
    assert result == "/custom/path/to/siril"
    
    mock_env_get.assert_called_once_with("SIRIL_BINARY")
    mock_isfile.assert_called_once_with("/custom/path/to/siril")
    mock_access.assert_called_once_with("/custom/path/to/siril", os.X_OK)


@patch("siril_mcp.server.os.environ.get")
@patch("siril_mcp.server.shutil.which")
def test_find_siril_binary_in_path(mock_which, mock_env_get):
    """Test _find_siril_binary when siril is in PATH."""
    from siril_mcp.server import _find_siril_binary
    
    # Mock no environment variable
    mock_env_get.return_value = None
    # Mock siril found in PATH
    mock_which.return_value = "/usr/bin/siril"
    
    result = _find_siril_binary()
    assert result == "/usr/bin/siril"
    
    mock_env_get.assert_called_once_with("SIRIL_BINARY")
    mock_which.assert_called_once_with("siril")


@patch("siril_mcp.server.os.environ.get")
@patch("siril_mcp.server.shutil.which")
@patch("siril_mcp.server.os.path.isfile")
@patch("siril_mcp.server.os.access")
def test_find_siril_binary_macos_location(mock_access, mock_isfile, mock_which, mock_env_get):
    """Test _find_siril_binary finding macOS app bundle location."""
    from siril_mcp.server import _find_siril_binary
    
    # Mock no environment variable and not in PATH
    mock_env_get.return_value = None
    mock_which.return_value = None
    
    # Mock the macOS location exists
    def mock_isfile_side_effect(path):
        return path == "/Applications/Siril.app/Contents/MacOS/Siril"
    
    def mock_access_side_effect(path, mode):
        return path == "/Applications/Siril.app/Contents/MacOS/Siril" and mode == os.X_OK
    
    mock_isfile.side_effect = mock_isfile_side_effect
    mock_access.side_effect = mock_access_side_effect
    
    result = _find_siril_binary()
    assert result == "/Applications/Siril.app/Contents/MacOS/Siril"


@patch("siril_mcp.server.os.environ.get")
@patch("siril_mcp.server.shutil.which")
@patch("siril_mcp.server.os.path.isfile")
@patch("siril_mcp.server.os.access")
def test_find_siril_binary_not_found(mock_access, mock_isfile, mock_which, mock_env_get):
    """Test _find_siril_binary when Siril is not found anywhere."""
    from siril_mcp.server import _find_siril_binary
    
    # Mock no environment variable, not in PATH, and no files found
    mock_env_get.return_value = None
    mock_which.return_value = None
    mock_isfile.return_value = False
    mock_access.return_value = False
    
    with pytest.raises(RuntimeError, match="Siril binary not found"):
        _find_siril_binary()


@patch("siril_mcp.server.os.environ.get")
def test_find_siril_binary_invalid_env_var(mock_env_get):
    """Test _find_siril_binary with invalid SIRIL_BINARY environment variable."""
    from siril_mcp.server import _find_siril_binary
    
    # Mock environment variable pointing to non-existent file
    mock_env_get.return_value = "/nonexistent/siril"
    
    with pytest.raises(RuntimeError, match="Custom Siril binary specified.*is not found"):
        _find_siril_binary()


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
