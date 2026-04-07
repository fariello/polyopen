# Polyopen

A Python module for versatile file handling, providing unified stream-level access to both local and remote files with transparent compression support.

Extracted and refined from the monolithic `pylib` workspace, `polyopen` is designed to stand alone as an easy-to-use utility library for fetching and writing data across a variety of protocols and formats.

## Background & Philosophy

`polyopen` was originally developed circa 2007 alongside a larger private monolithic repository. At the time, no intuitive unified solution existed in the Python ecosystem to seamlessly juggle disparate compression formats and remote stream protocols behind a single standard API. It has been battle-tested (famous last words) and refined for personal usage for over a decade before being fully extracted into this dedicated, standalone package.

**Why not just use `smart_open`?**
While the fantastic `smart_open` library eventually emerged to solve a similar problem space, `polyopen` is maintained to provide a distinct, highly-focused alternative:
- **Lightweight Architecture:** `smart_open` is inherently wired for massive cloud data lakes, utilizing heavy overarching SDKs (`boto3`, GCS, etc.) to manage complex object chunking. `polyopen` strictly eschews massive cloud architectures in favor of blistering-fast import times, strictly lazy-loaded dependencies, and base-level infrastructure (Linux protocols, HTTP, FTP).
- **Inherent Resiliency:** `polyopen` uniquely features automatic backup rotation. When explicitly overwriting destination datasets locally or over SSH/FTP, `polyopen` seamlessly rolls sequential `.bu` backwards backups without forcing you to write complex filesystem manipulation logic.

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

### Supported Stream Formats
| Format / Protocol | Read? | Write? | Append? | Notes |
| :--- | :---: | :---: | :---: | :--- |
| Plain Text (`.txt`, `.csv`, etc.) | Yes | Yes | Yes | StandardUTF-8 streams |
| Zstandard (`.zst`) | Yes | Yes | Yes | Extremely fast, supports concatenated frames |
| GZIP (`.gz`) | Yes | Yes | Yes | Standard Python `gzip` bindings |
| BZIP2 (`.bz2`) | Yes | Yes | Yes | Standard Python `bz2` bindings |
| LZMA (`.xz`) | Yes | Yes | Yes | Standard Python `lzma` bindings |
| Local File (`file://` or implicit) | Yes | Yes | Yes | Standard local OS operations, handles backup `.bu` rotation |
| SSH / SFTP (`ssh://`, `sftp://`) | Yes | Yes | Yes | Fully authenticated remote transfer, supports backups |
| FTP (`ftp://`) | Yes | Yes | Yes | Standard FTP transfer, supports backups |
| HTTP / HTTPS (`http://`, `https://`) | Yes | No | No | Protected stream-fetching only, throws `ReadOnlyProtocolError` on write |

### Unsupported Archive Formats
These formats are **Archival Containers** (miniature file systems), not uniform text streams. If passed to `polyopen`, they will instantly raise an `UnsupportedArchiveError` to protect you from inadvertently corrupting them.

| Container Extension | Supported? | Reason | Alternative |
| --- | :---: | --- | --- |
| `.zip` | No | Writing streams overwrites the Central Directory index map, corrupting the file. | Use Python's built-in `zipfile` |
| `.tar` | No | Contains POSIX file headers and multiple internal hierarchy layers. | Use Python's built-in `tarfile` |
| `.rar`, `.7z` | No | Binary filesystem maps rather than single-file text compression streams. | Use 3rd party archive managers |
| `.tar.gz`, `.tgz` | No | Sits underneath a `.tar` extraction layer. | Use Python's built-in `tarfile` |

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

# Copy data across boundaries natively (Source -> Destination)
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

## Full Documentation & Architecture

For deep-dives into the precise mechanical routing topologies, algorithm boundary mappings, or exact programmatic SDK constraints, consult the formal internal documentation map:
- [Public API Specs](docs/API.md): Parameter lists, native Exception hierarchy behavior, `PolyReader` semantics natively.
- [CLI Behaviors](docs/CLI.md): Exact bash evaluations tracking positional broadcast parameters internally natively.
- [Architecture Overview](ARCHITECTURE.md): Structural evaluations analyzing native `io.TextIOWrapper` chunk interception safely verifying Mock CI endpoints identically.
- [Functional Specification](FUNCTIONAL_SPEC.md): Formal pre-release technical constraints capturing all system operational scope comprehensively.

## Acknowledgements and Limitations

While the module is heavily structurally covered, developers should accurately understand exact integration constraints natively:
- **Cloud Immutability Exclusions**: Due strictly to architectural constraints barring internal S3 file appending recursively natively, execution flows evaluating exact enterprise object strings natively (`s3://`, `gs://`, `az://`) are securely blocked. Use `smart_open` appropriately to manipulate those objects dynamically.
- **Write Tracking Limitation (v0.1.0)**: Executing specific parameter flags injecting `show_progress=True` executes flawlessly across `PolyReader` streaming iterations, but is inherently disabled iteratively executing across `PolyWriter` pipelines natively.
- **Infinite Blocking Risk**: Executing backup checks against SFTP topologies actively sequentially evaluates `stat(file.XXX.bu)` numbers manually. Remote nodes structurally hosting thousands of sequential `.bu` files natively will incur mathematically linear blocking overhead dynamically polling arrays gracefully before generating sequential bounds fundamentally.
