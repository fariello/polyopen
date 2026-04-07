# Polyopen

A Python module for versatile file handling, providing unified stream-level access to both local and remote files with transparent compression support.

Extracted and refined from the monolithic `pylib` workspace, `polyopen` is designed to stand alone as an easy-to-use utility library for fetching and writing data across a variety of protocols and formats.

## Features

- **Transparent Compression**: Seamlessly reads and writes `.gz`, `.bz2`, `.xz`, and `.zst` files on the fly.
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

The easiest way to use the library is with the unifed `polyopen()` wrapper, which automatically routes to a `PolyReader` or `PolyWriter` and acts exactly like Python's built-in `open()`. 

You can use it universally for both standard I/O and remote/compressed files!

### Basic Usage

```python
from polyopen import polyopen

# 1. Writing to a local compressed file
with polyopen("output.bz2", 'w') as f:
    f.write("Hello, World!\n")

# 2. Appending without producing backup files
with polyopen("output.bz2", 'a') as f:
    f.write("Appended line.\n")

# 3. Reading it back efficiently
with polyopen("output.bz2", 'r') as f:
    for line in f:
        print(line.strip())
```

## Capabilities & Support Matrix

Because `polyopen` is designed absolutely for stream-based parsing, it supports appending natively to compatible stream formats, but actively restricts container archives to prevent unintentional corruption.

### 🟢 Supported Stream Formats
| Format / Protocol | Read? | Write? | Append? (`'a'`) | Notes |
| :--- | :---: | :---: | :---: | :--- |
| Plain Text (`.txt`, `.csv`, etc.) | ✅ | ✅ | ✅ | StandardUTF-8 streams |
| Zstandard (`.zst`) | ✅ | ✅ | ✅ | Extremely fast, supports concatenated frames |
| GZIP (`.gz`) | ✅ | ✅ | ✅ | Standard Python `gzip` bindings |
| BZIP2 (`.bz2`) | ✅ | ✅ | ✅ | Standard Python `bz2` bindings |
| LZMA (`.xz`) | ✅ | ✅ | ✅ | Standard Python `lzma` bindings |
| Local File (`file://` or implicit) | ✅ | ✅ | ✅ | Standard local OS operations, handles backup `.bu` rotation |
| SSH / SFTP (`ssh://`, `sftp://`) | ✅ | ✅ | ✅ | Fully authenticated remote transfer, supports backups |
| FTP (`ftp://`) | ✅ | ✅ | ✅ | Standard FTP transfer, supports backups |
| HTTP / HTTPS (`http://`, `https://`) | ✅ | ❌ | ❌ | Protected stream-fetching only, throws `ReadOnlyProtocolError` on write |

### 🔴 Unsupported Archive Formats
These formats are **Archival Containers** (miniature file systems), not uniform text streams. If passed to `polyopen`, they will instantly raise an `UnsupportedArchiveError` to protect you from inadvertently corrupting them.

| Container Extension | Supported? | Reason | Alternative |
| --- | :---: | --- | --- |
| `.zip` | ❌ | Writing streams overwrites the Central Directory index map, corrupting the file. | Use Python's built-in `zipfile` |
| `.tar` | ❌ | Contains POSIX file headers and multiple internal hierarchy layers. | Use Python's built-in `tarfile` |
| `.rar`, `.7z` | ❌ | Binary filesystem maps rather than single-file text compression streams. | Use 3rd party archive managers |
| `.tar.gz`, `.tgz` | ❌ | Sits underneath a `.tar` extraction layer. | Use Python's built-in `tarfile` |

### Advanced Networking

Pass network protocols seamlessly without changing syntax. (`polyopen` will natively `.gz`, `.bz2`, and `.zst` wrap via the file extension)

```python
from polyopen import polyopen

# Write directly to a remote SSH/sftp box (auto-maintains .bu backups on overwrite!)
with polyopen("sftp://username:password@hostname/data.csv.zst", 'w', backup=True) as f:
    f.write("id,name\n1,john\n")

# Read a remote HTTP Stream
with polyopen("http://example.com/data.txt.gz", 'r') as f:
    for line in f:
        print(line.strip())
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
