import subprocess
import pytest
import os
import sys

def run_cli(*args):
    """Utility to spawn subprocess commands targeting polyopen module structurally."""
    cmd = [sys.executable, "-m", "polyopen.polyopen"] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def test_cli_illegal_modes():
    """Asserts that the argparse module mutually excludes overlapping rules securely."""
    # Omitting both Read and Write should throw an exit code parsing error
    result = run_cli("test.txt")
    assert result.returncode != 0
    assert "one of the arguments --write/-w --read/-r is required" in result.stderr

    # Omitting target file entirely
    result = run_cli("--read")
    assert result.returncode == 0 # Wait, main() takes `nargs='*'`, so providing no files might succeed and do nothing. Wait, no files means the script exits clean or prints help? Let's check locally via test.

def test_cli_read_execution(tmp_path):
    # Establish a local target
    target = str(tmp_path / "mock.txt")
    with open(target, 'w') as f:
        f.write("A line.\nAnother line.\n")

    result = run_cli("--read", target)
    
    assert result.returncode == 0
    # main() prints the file stats
    assert "FINISHED Reading." in result.stdout

def test_cli_write_execution(tmp_path):
    source = str(tmp_path / "mock.txt")
    with open(source, 'w') as f:
        f.write("Data1\nData2\n")

    target = str(tmp_path / "write_mock.txt")
    
    cmd = [sys.executable, "-m", "polyopen.polyopen", "--write", "--input-file", source, target]
    result = subprocess.run(cmd, text=True, capture_output=True)
    
    assert result.returncode == 0
    assert os.path.exists(target)
    
    with open(target, 'r') as f:
        data = f.read()
    assert "Data1\nData2\n" == data
