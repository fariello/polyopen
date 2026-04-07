import os
import pytest
from polyopen import polyopen

# The golden files injected contain 3 lines of byte-converted text.
EXPECTED_LINES = ["line 1\n", "line 2\n", "line 3\n"]

@pytest.mark.parametrize("ext", [".txt", ".txt.gz", ".txt.bz2", ".txt.xz", ".txt.zst"])
def test_golden_file_integrity(ext):
    """
    Guarantees that third-party streaming dependencies (like zstandard and lzma) 
    do not alter their native extraction algorithms across API updates.
    """
    # Map the current static path relative to this script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fixture_path = os.path.join(base_dir, "fixtures", f"gold{ext}")
    
    assert os.path.exists(fixture_path), f"Golden fixture missing: {fixture_path}"

    lines = []
    with polyopen(fixture_path, 'r') as reader:
        for line in reader:
            lines.append(line)
            
    assert lines == EXPECTED_LINES
