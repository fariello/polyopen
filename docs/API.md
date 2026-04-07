# Polyopen API Reference

The `polyopen` module exposes robust context managers for handling transparent multi-format, multi-protocol file streams.

---

## `class PolyReader`

A class used to read files line by line, with native support for `gzip`, `bz2`, and `zst` compression formats, as well as remote files via `HTTP`, `HTTPS`, `FTP`, `SSH`, and `SFTP`.

### `__init__(self, filename: str, show_progress: bool = False)`

Initialize `PolyReader` with a specific filename structure. 

**Parameters:**
- `filename`: A literal file path or a complete URI denoting the location and protocol of the file. Supported schemes:
  - Local filesystem (`path/to/file.ext`)
  - HTTP / HTTPS (`http://domain.com/path/...`)
  - SSH / SFTP (`ssh://user:pass@host/path/...`, `sftp://user:pass@host/path/...`)
- `show_progress`: `bool`, optional. If `True`, a console progress bar utilizes `tqdm` based on the file stream's underlying length (when computable).

### Methods

#### `open(self) -> 'PolyReader'`
Manually trigger the open and parsing logic. 
*Note: Generally you should prefer using `PolyReader` as a context manager `with PolyReader(...) as reader:` which implicitly evaluates this method.*

#### `close(self)`
Safely flush buffers and shut down networking session hooks.

#### Yields (`__iter__`)
A stream of decompressed, UTF-8 encoded text lines.
```python
with PolyReader("myfile.txt.gz") as reader:
    for line in reader:
        print(line)
```

---

## `class PolyWriter`

A class used to safely write line-by-line buffers directly to transparent compressions (`gzip`, `bz2`, `zst`) and routing to remote architectures (`FTP`, `SSH`, `SFTP`, Local).

### `__init__(self, filename: str)`

Initialize `PolyWriter` with a specific target filename.

**Parameters:**
- `filename`: Target output file path. The stream respects the `.gz`, `.bz2`, or `.zst` termination by wrapping standard python text-streams through their relevant dictionary compression. Supported network destinations:
  - Local files (`out.gz`)
  - FTP (`ftp://user:pass@host/path/...`)
  - SSH / SFTP (`ssh://user:pass@host/path/...`)

### Methods

#### `open(self, append: bool = False, backup: bool = True) -> 'PolyWriter'`
Manually opens the file allocation, providing safety bindings for appending data or copying backup revisions. To utilize these flags with a context manager, you must manually initialize `open()`.

**Parameters:**
- `append`: `bool` (default `False`). Open in text-append translation mode (`"at"`/`"ab"`).
- `backup`: `bool` (default `True`). If a file already exists at the requested path, polywriter renames the previous representation to `.001.bu`.
- *Throws ValueError if both `append` and `backup` are `True`.*

#### `write(self, data: str)`
Emit data sequentially to the stream context.

#### `close(self)`
Commit file handles safely.

---

## `class FTPSessionWrapper`
*Internal Use Context Provider*
A direct interface adapter wrapping `ftplib.FTP`, supporting FTP connections against non-standard runtime ports to service `PolyWriter` and `PolyReader` network abstractions.
