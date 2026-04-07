import os
import pytest
from polyopen import PolyReader, PolyWriter, polyopen

def test_plain_text(tmp_path):
    data = ["hello", "world", "this", "is", "a", "test"]
    filepath = str(tmp_path / "test.txt")

    # Test writing
    with PolyWriter(filepath) as writer:
        for line in data:
            writer.write(line + '\n')
    
    assert os.path.exists(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        assert f.read().splitlines() == data

    # Test reading
    read_data = []
    with PolyReader(filepath) as reader:
        for line in reader:
            read_data.append(line.rstrip('\n'))
            
    assert read_data == data

@pytest.mark.parametrize("ext", [".gz", ".bz2", ".zst", ".xz"])
def test_compressed_files(tmp_path, ext):
    data = ["line1 compressed", "line2 compressed", f"some data for {ext}"]
    filepath = str(tmp_path / f"test_data{ext}")

    # Write compressed
    with PolyWriter(filepath) as writer:
        for line in data:
            writer.write(line + '\n')

    assert os.path.exists(filepath)
    
    # Read compressed
    read_data = []
    with PolyReader(filepath) as reader:
        for line in reader:
            read_data.append(line.rstrip('\n'))
            
    assert read_data == data

def test_polyopen_shorthand(tmp_path):
    filepath = str(tmp_path / "shorthand_test.zst")
    data = ["polyopen", "shorthand", "rocks"]
    
    # Test writing
    with polyopen(filepath, 'w') as writer:
        for line in data:
            writer.write(line + '\n')
            
    assert os.path.exists(filepath)
    
    # Test appending
    append_data = ["another", "line"]
    with polyopen(filepath, 'a') as writer:
        for line in append_data:
            writer.write(line + '\n')
            
    read_appended = []
    with polyopen(filepath, 'r') as reader:
        for line in reader:
            read_appended.append(line.rstrip('\n'))
            
    assert read_appended == data + append_data

def test_backup_rotation(tmp_path):
    filepath = str(tmp_path / "backup.txt")
    
    with polyopen(filepath, 'w', backup=True) as w:
        w.write("First.\n")
        
    with polyopen(filepath, 'w', backup=True) as w:
        w.write("Second.\n")
        
    backup_path = f"{filepath}.001.bu"
    assert os.path.exists(backup_path)
    
    with open(backup_path, 'r') as f:
        assert f.read() == "First.\n"
