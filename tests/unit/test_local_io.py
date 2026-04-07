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

@pytest.mark.parametrize("ext", [".gz", ".bz2", ".zst", ".xz"])
def test_rigorous_line_chunking(tmp_path, ext):
    """
    Rigorously assess how CPython buffers streaming algorithms across native memory constraints.
    Default IO chunks are routinely 131,072 bytes. This suite generates payloads explicitly 
    engineered to collide cleanly across chunk frames.
    """
    filepath = str(tmp_path / f"rigorous_chunk_test{ext}")
    
    # Constructing lines to meet explicit chunking edge logic
    CHUNK_SIZE = 131072
    lines_to_write = [
        "A short line with whitespace. \n", # 1. Less than chunk size
        "A" * int(CHUNK_SIZE * 0.8) + "\n", # Fill up end of chunk 1
        "B" * int(CHUNK_SIZE * 0.5) + " words \n", # 2. Starts in chunk 1, ends in chunk 2
        "C" * int(CHUNK_SIZE * 2.5) + " traversing \n", # 3. Starts in chunk 2, traverses chunk 3, ends in 4
        "Short middle line \n",
        "Another string with random whitespaces \n",
        "More string padding to shift the buffer windows around \n",
        "Small 8th line \n",
        "D" * int(CHUNK_SIZE * 0.3) + " testing \n",
        "E" * 500 + "\n",
        "F" * 200 + "\n",
        "G" * int(CHUNK_SIZE * 1.5) + " final line \n" # 4. Ends file spanning across final chunk
    ]
    
    with PolyWriter(filepath) as writer:
        for line in lines_to_write:
            writer.write(line)
            
    read_data = []
    with PolyReader(filepath) as reader:
        for line in reader:
             read_data.append(line)
             
    # Asserting exact identical retrieval
    assert len(read_data) == 12
    assert read_data == lines_to_write
