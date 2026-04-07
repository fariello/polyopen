# Command Line Interface (CLI) Guide

*[Return to Main README](../README.md)*

While `polyopen` is natively configured as a backend scripting dependency wrapper module utilized internally inside larger Python topologies, it also ships alongside an executable CLI environment structure.

The CLI serves principally dual-purposes natively:
1. Validating structural algorithmic IO streaming speeds.
2. Rapidly mapping file-broadcast architectures explicitly across remote nodes.

## Usage Blueprint

```bash
python -m polyopen.polyopen [-h] (--write | --read) [--input-file INPUT_FILE] [file ...]
```

## Flags & Arguments

* `file ...` (Positional): The unified target file string maps. These define the external operational endpoints internally handling destination mappings identically.
* `--read`, `-r` (Mutually Exclusive Boolean Context): Declares the execution process triggers sequence mapping strictly invoking native read logic looping constructs over all positional `file` payload arrays systematically.
* `--write`, `-w` (Mutually Exclusive Boolean Context): Engages localized file generation logic pushing IO output natively over designated destination targets explicitly. Positionally extracts `file[0]` identically mapping towards `file[1:]`.

## Practical Examples

### Benchmarking Streams Natively (`--read`)
Passing isolated compression bundles iteratively triggers an assessment routine extracting explicit ingestion rates uniformly across target payload sequences.

```bash
python -m polyopen.polyopen --read syslog.01.zst syslog.02.bz2 https://server.com/archive.gz
```
**Output Profile:**
```
TESTING reading syslog.01.zst
FINISHED Reading. syslog.01.zst. 238,901 lines / 48.2MB at 41,200.5/s (8.1MB/s). Total time: 5.79 Secs.
...
```

### Broadcasting Datasets Structurally (`--write`)
By combining `--write` flags natively against an `--input-file` declaration loop, `polyopen` sequentially parses identical string arrays natively injecting datasets consecutively across an endless matrix array dynamically broadcasting payloads natively!

```bash
# Iteratively parse the central SQL-dump map, converting it continuously across
# native GZIP, BZ2, and remote SFTP topological endpoints sequentially perfectly formatted!
python -m polyopen.polyopen --write -i postgres_dump.sql local_archive.gz local_archive.bz2 sftp://user@node/dump.zst
```

## Known Limitations
* **Broadcast Execution Modality:** Because `polyopen` is an inherently linear streaming evaluation block tracking `io.TextIOWrapper` endpoints iteratively, providing dozens of positional broadcast parameters utilizing `--write` behaves strictly synchronously (O(n) latency map). High concurrency multithreading execution boundaries natively dictating remote parallel IO bursts must be configured outside the CLI by leveraging the programmatic Python `polyopen(...)` library directly cleanly.
