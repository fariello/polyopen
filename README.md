# Polyopen

A Python module for versatile file handling, providing unified stream-level access to both local and remote files with transparent compression support.

Extracted and refined from the monolithic `pylib` workspace, `polyopen` is designed to stand alone as an easy-to-use utility library for fetching and writing data across a variety of protocols and formats.

## Features

- **Transparent Compression**: Seamlessly reads and writes `.gz`, `.bz2`, and `.zst` files on the fly.
- **Multiple Protocols**: Directly read from and write to remote sources via `HTTP`, `HTTPS`, `FTP`, `SSH`, and `SFTP`.
- **Automatic Backups**: Creates numbered `.bu` backup files natively when overwriting existing files or destinations.
- **Easy Context Management**: Fully supports standard `with` statements, behaving like Python's built-in `open()`.

## Installation

Install using standard Python package management (`pip`):

```bash
pip install polyopen
```

(*Note*: Depends on `paramiko`, `zstandard`, `requests`, `tqdm`, and `ftputil`.)

## Quick Start

### Reading Files

To read from a local gzipped file:
```python
from polyopen import PolyReader

with PolyReader("path/to/localfile.gz") as reader:
    for line in reader:
        print(line)
```

To read from a remote HTTP source:
```python
with PolyReader("http://example.com/data.txt") as reader:
    for line in reader:
        # process(line)
```

To read from a remote SSH server with zstd compression:
```python
with PolyReader("ssh://username:password@hostname/path/to/remote.zst") as reader:
    for line in reader:
        # process(line)
```

### Writing Files

To write to a local bz2 compressed file:
```python
from polyopen import PolyWriter

with PolyWriter("path/to/outputfile.bz2") as writer:
    writer.write("Some data to write\n")
```

To write to a remote SFTP server:
```python
with PolyWriter("sftp://username:password@hostname/path/to/outputfile.txt") as writer:
    writer.write("Remote data writing works identically.\n")
```

## Built-in Test CLI
You can test reading and writing directly without a Python script:

```bash
# Read a compressed file and show progress
python -m polyopen.polyopen --read path/to/large.zst

# Copy data across boundaries
python -m polyopen.polyopen --write http://source.com/data.csv.gz sftp://user:pass@host/dest.csv.zst
```

## Development
To set up a local development environment:

```bash
git clone <repository_url>
cd polyopen
pip install -e .[dev] pytest
python -m pytest tests/
```
