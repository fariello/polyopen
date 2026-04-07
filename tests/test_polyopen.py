import os
import shutil
import tempfile
import pytest

from polyopen import PolyReader, PolyWriter

@pytest.fixture
def temp_dir():
    # Create a temporary directory for test files
    test_dir = tempfile.mkdtemp()
    yield test_dir
    # Cleanup
    shutil.rmtree(test_dir)

def create_raw_file(filepath, lines):
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

def read_raw_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

def test_plain_text(temp_dir):
    data = ["hello", "world", "this", "is", "a", "test"]
    filepath = os.path.join(temp_dir, "test.txt")

    # Test writing
    with PolyWriter(filepath) as writer:
        for line in data:
            writer.write(line + '\n')
    
    assert os.path.exists(filepath)
    assert read_raw_file(filepath) == data

    # Test reading
    read_data = []
    with PolyReader(filepath) as reader:
        for line in reader:
            read_data.append(line.rstrip('\n'))
            
    assert read_data == data

@pytest.mark.parametrize("ext", [".gz", ".bz2", ".zst"])
def test_compressed_files(temp_dir, ext):
    data = ["line1 compressed", "line2 compressed", f"some data for {ext}"]
    filepath = os.path.join(temp_dir, f"test_data{ext}")

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

def test_append_and_backup(temp_dir):
    filepath = os.path.join(temp_dir, "backup_test.txt")
    data_initial = ["first write"]
    
    # Initial write
    with PolyWriter(filepath) as writer:
        for line in data_initial:
            writer.write(line + '\n')

    # Test backup configuration (default backup=True, should create .bu file)
    data_overwrite = ["second write"]
    with PolyWriter(filepath) as writer:
        # Default behavior is to create a backup
        for line in data_overwrite:
            writer.write(line + '\n')
            
    backup_path = f"{filepath}.001.bu"
    assert os.path.exists(backup_path)
    assert read_raw_file(backup_path) == data_initial
    assert read_raw_file(filepath) == data_overwrite

    # Test append
    data_append = ["third append"]
    # We must set append=True, backup=False according to PolyWriter logic
    # The open method needs to be called properly, or we can instantiate and rely on __enter__?
    # Wait, PolyWriter.__enter__ calls self.open() which uses defaults append=False, backup=True.
    # To append, we need to call open(append=True, backup=False) explicitly, or PolyWriter should accept these as init params.
    # Let's check PolyWriter source for how append works...
    writer = PolyWriter(filepath)
    writer.open(append=True, backup=False)
    for line in data_append:
        writer.write(line + '\n')
    writer.close()

    expected_combined = data_overwrite + data_append
    assert read_raw_file(filepath) == expected_combined
