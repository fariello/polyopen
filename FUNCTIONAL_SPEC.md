# Functional Specification: `polyopen`

*[Return to Main README](README.md)*

**Version:** 0.1.0
**Last Updated:** 2026-04-07

## 1. Purpose and Scope
`polyopen` is a lightweight, zero-configuration Python library designed to natively unify read, write, and append operations across multiple remote protocols and stream-based data compression algorithms. It acts as an augmented drop-in replacement for CPython's standard `builtins.open()` context manager, resolving complex external transport layers securely out-of-the-box.

**Non-Goals:** `polyopen` is deliberately not designed for cloud infrastructure management (e.g., AWS S3 multipart streaming) or complex Posix archival system manipulation (`.tar`, `.zip`). 

## 2. Core Concepts and Terminology
- **Unified Wrapper:** The `polyopen()` entry point intelligently infers behavior, automatically delegating execution to the proper internal handler (e.g., `PolyReader` or `PolyWriter`) based on the invocation mode.
- **Transparent Decompression:** Utilizing standard library extensions (`_compression` and `io.TextIOWrapper`), stream algorithms like `.zst` or `.gz` are evaluated entirely lazily and piped back into standard UTF-8 string fragments automatically.
- **Dynamic Backup Rotation:** A unique local/network resiliency feature that auto-detects destination overwrite collisions, caching historical overwrites iteratively with sequential `.001.bu` numeric tags rather than blindly destroying data.

## 3. Supported Protocols & Data Models
Because `polyopen` is explicitly configured for contiguous stream parsing, it asserts rigorous internal guards defining file boundaries. 

### 3.1 Network Transports
- `file://` (Implicit): 100% feature compliance.
- `ftp://`: Fully supported (relies on `ftputil`).
- `ssh://` or `sftp://`: Fully supported (relies on `paramiko` mapping context configuration via `~/.ssh/known_hosts` natively). 
- `http://` / `https://`: Stream fetching supported natively (relies on `requests`). **Read-Only**.

**Refusals:** `s3://`, `gs://`, `hdfs://`, `az://` will actively trigger a hard crash alerting users to instead leverage dedicated `smart_open` binaries.

### 3.2 Compression Models
Natively supported stream architectures:
1. `bz2` (Standard Python binding)
2. `gz` (Standard Python binding)
3. `xz` (Standard Python lzma binding)
4. `zst` (Requires `zstandard` module)

**Archival Containers (e.g., `.zip`, `.tar`, `.rar`) are explicitly rejected** during I/O instantiation because `readline()`/`write()` streams catastrophically corrupt their embedded binary file-tables.

## 4. Public API 
### `polyopen(filename: str, mode: str = 'r', backup: bool = True, show_progress: bool = False)`
- **`mode`**: Interrogates trailing strings (e.g., `r`, `wt`, `ab`). Determines branching into `PolyReader` or `PolyWriter`.
- **`backup`**: Autonomously intercepts `w` directives (ignoring `a`) to preserve files sequentially (`file.001.bu`). 
- **`show_progress`**: Injects an instantiated `tqdm` output bar tracking the binary read depth over UI consoles. **Note:** Currently only functional on `PolyReader` objects.

*(Internal objects `PolyReader` and `PolyWriter` provide identical internal contextual mapping `__enter__` and `__exit__` execution, but are typically obfuscated behind the unified parser)*.

## 5. Command-Line Interface (CLI) Behavior
The package exposes testing evaluation loops directly via standard environment execution.
`python -m polyopen.polyopen`
- `--read` (`-r`): Required for executing performance benchmarks across provided target `files`. Returns lines processed, exact chunk sizes, and streaming speeds natively.
- `--write` (`-w`): Pips the binary string stream of `file[0]` dynamically into all trailing positional `files[1:]` broadcast targets inherently mirroring legacy Unix primitives perfectly.
*Exit Semantics:* Returns `0` gracefully on correct routing, throws `parser.error` alongside `exit(1)` if arguments clash (like missing targets). 

## 6. Edge Cases & Boundary Conditions
1. **Append & Backup Collision:** Passing `polyopen(file, 'a', backup=True)` inherently triggers `ValueError("Cannot have both append and backup set to True")`.
2. **Infinite Backup Sequences:** Rotating backups rely on `os.path.exists()` or `sftp.stat()` iterating to infinity. If 999 backups exist, the system continues polling increment counters manually.
3. **Chunk Shearing Limitations:** `zstandard` internal payloads are 128KB by default. Extremely massive line structures (e.g., lines scaling over 300,000 sequential characters) are successfully parsed due to strict delegation of string-rebuilding natively back to the Python standard `io.TextIOWrapper` boundary constraints.

## 7. Security and Safety Considerations
1. **Remote Shell Code Execution Risk:** SSH client endpoints enforce `load_system_host_keys()`, actively refusing blind Hostkey injections by default on fresh environments to thwart Man-In-The-Middle network redirections.
2. **Archival Destruction Safety:** Archival rejection is hardcoded in memory via static array evaluations ensuring a user can never permanently destroy localized central directory maps of remote zip files via blindly appending data frames.
3. **Cloud Credentials Bleed Avoidance:** Rejection of `boto3` logic natively secures developers against accidentally mapping AWS environment access tokens directly through untracked repository executions.
