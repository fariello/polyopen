# Public API Reference: `polyopen`

*[Return to Main README](../README.md)*

This document serves as the formal specification for developers programmatically integrating `polyopen` into Python workspaces. 

## The Core Wrapper

### `polyopen(filename: str, mode: str = 'r', backup: bool = True, show_progress: bool = False)`
This function is intended to be a 1-to-1 drop-in replacement for the native Python `builtins.open()` context manager. It completely obfuscates the intricacies of remote protocol connectivity, auto-routing execution pathways locally underneath.

#### Parameters
- **`filename`** (`str`): The target path or URL. (e.g. `tests/data.txt`, `https://example.com/log.zst`, or `ssh://user@host/syslog`).
- **`mode`** (`str`): Target IO operation format sequence:
  - Reading operations (`'r'`, `'rt'`, `'rb'`) trigger `PolyReader`.
  - Writing / Truncating (`'w'`, `'wt'`, `'wb'`) trigger `PolyWriter(append=False)`.
  - Appending operations (`'a'`, `'at'`, `'ab'`) trigger `PolyWriter(append=True)`.
- **`backup`** (`bool`): Determines whether `polyopen` creates rolling numeric backups (`file.001.bu`) naturally before overwriting existing destinations locally or across SSH/FTP topologies. Default is `True`. 
  - *Guard Rails:* Triggers a `ValueError` if used alongside `'a'` Mode constraints natively, since Appending inherently avoids structural replacement.
- **`show_progress`** (`bool`): Enables a console `tqdm` IO progress bar reporting binary line ingestion progress. 
  - *Guard Rails:* This flag only governs iteration over `PolyReader`. Providing `show_progress=True` dynamically atop a `PolyWriter` execution inherently triggers a `NotImplementedError` directly natively avoiding deceptive execution gaps sequentially.

#### Exceptions
To structurally isolate pipeline operations, `polyopen` leverages a custom native exception tree tracking boundary violations inherently. All exceptions inherit from a base `PolyopenError` package class.

`UnsupportedArchiveError`: Triggered preemptively when an invocation dynamically catches trailing Posix archival indicators exclusively blocking operations across (`.zip`, `.tar`, `.tgz`, `.7z`, or `.rar` paths).
`ReadOnlyProtocolError`: Actively denies logical Appending/Write stream permutations initiated against natively stateless retrieval environments strictly (e.g., triggering `polyopen("https://...", 'w')`).
`UnsupportedProtocolError`: Caught intentionally whenever `urllib.parse` queries detect an enterprise object-storage protocol map request string (`s3://`, `gs://`, `az://`). Prevents blind authentication failures while structurally directing users toward heavier alternative Python library SDKs mapping explicitly to those platforms (like `smart_open` or native `boto3`).

---

## Direct Handler Abstractions

Advanced users bypassing the unified `polyopen(...)` entry wrapper may interact iteratively directly with the backend object components handling the connection semantics dynamically below.

### `class PolyReader`
Invoked autonomously internally mapped for file ingestion paths dynamically.

#### Methods
- **`__init__(self, filename: str, show_progress: bool = False)`**: Assesses URL handlers internally mapped to sequence connections natively.
- **`open(self) -> 'PolyReader'`**: Establishes active network session constraints. Explicitly tracks file size limits across valid endpoints (`_http_file_size` internal metadata block natively established via `requests.get()` headers). 
- **`close(self) -> None`**: Flushes stream operations closing remote SFTP objects gracefully alongside the localized native internal `io.TextIOWrapper` dependencies cleanly.
- **`__next__(self) -> str`**: Lazily pulls chunk iterations utilizing `self._fh.readline()`, automatically handling continuous chunk slicing boundaries locally and appending fragments seamlessly via CPython standard buffering constraints inherently!

### `class PolyWriter`
Explicitly tracks outbound stream algorithms natively determining optimal output frames mathematically.

#### Methods
- **`__init__(self, filename: str, show_progress: bool = False)`**: Natively identical.
- **`open(self, append: bool = False, backup: bool = True) -> 'PolyWriter'`**: Dynamically evaluates the structural network routing, natively invoking explicit `try/catch` `.stat()` lookup sequences dynamically triggering robust `.bu` backwards archival generation iteratively over remote environments cleanly.
- **`write(self, data: str) -> None`**: Securely casts textual IO frames sequentially passing payloads statically to the isolated algorithmic dictionary chunking structures effectively (`zstd.ZstdCompressor.stream_writer`, `bz2.BZ2File`, etc).
