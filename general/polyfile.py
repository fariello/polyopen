#!/usr/bin/env python3

import argparse
import io
import bz2
import gzip
import paramiko
import zstandard as zstd
import requests
from urllib.parse import urlparse
from tqdm import tqdm
import ftplib
import ftputil
import os


class FTPSessionWrapper(ftplib.FTP):
    """
    FTPSessionWrapper as described in https://ftputil.sschwarzer.net/documentation
    """

    def __init__(self, host, userid, password, port):
        """Act like ftplib.FTP's constructor but connect to another port."""
        ftplib.FTP.__init__(self)
        self.connect(host, port)
        self.login(userid, password)
        pass

    pass


class PolyReader:
    """
    A class used to read files line by line, with support for gzip, bz2, and zst compression formats,
    as well as remote files over HTTP, HTTPS, FTP, SSH, and SFTP.

    ...

    Attributes
    ----------
    filename : str
        a string representing the file path or URL to read

    Methods
    -------
    open():
        Opens the file for reading, decompressing it on the fly if necessary.
    close():
        Closes the file.
    """

    def __init__(self, filename: str, show_progress: bool = False):
        """
        Initialize PolyReader with a filename.

        :param filename: The name of the file to read.
        :param show_progress: Whether to show a progress bar.
        """
        self.filename = filename
        self.show_progress = show_progress
        self._fh = None
        self._sftp = None
        self._ftp = None
        self._progress = None
        self._request_iterator = False

    def __enter__(self):
        """
        Open the file when entering the context.
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the file when exiting the context.
        """
        self.close()

    def __iter__(self):
        """
        Make the PolyReader object iterable.
        """
        return self

    def __next__(self):
        """
        Provide the next line in the file.
        """
        if self._request_iterator:
            line = next(self._fh)
        else:
            line = self._fh.readline()
            pass

        if self.show_progress and self._progress is not None:
            self._progress.update(len(line))

        if not line:
            # End of file
            raise StopIteration
        if isinstance(line, bytes):
            return line.decode()
        return line

    def open(self):
        """
        Open the file for reading, decompressing it on the fly if necessary.

        """
        parsed = urlparse(self.filename)

        if parsed.scheme in ('sftp', 'ssh'):
            # Handle SFTP URLs
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.connect(parsed.hostname, username=parsed.username, password=parsed.password)
            sftp = client.open_sftp()
            try:
                f = sftp.file(parsed.path, 'rb')
            except FileNotFoundError as err:
                print(f"ERROR: No such file found: {self.filename}")
                return exit(1)
            if self.filename.endswith('.zst'):
                dctx = zstd.ZstdDecompressor(max_window_size=2**31)
                self._fh = io.TextIOWrapper(dctx.stream_reader(f), encoding='utf-8')
            elif self.filename.endswith('.bz2'):
                self._fh = bz2.BZ2File(f)
            elif self.filename.endswith('.gz'):
                self._fh = gzip.GzipFile(fileobj=f)
            else:
                self._fh = f
                pass
            self._sftp = sftp
        elif  parsed.scheme in ('http', 'https'):
            response = requests.get(self.filename, stream=True)
            if self.filename.endswith(".zst"):
                dctx = zstd.ZstdDecompressor(max_window_size=2**31)
                self._fh = io.TextIOWrapper(dctx.stream_reader(response.content, read_across_frames=True), encoding='utf-8')
            elif self.filename.endswith(".bz2"):
                self._fh = bz2.open(response.raw, 'rt')
            elif self.filename.endswith(".gz"):
                self._fh = gzip.open(response.raw, 'rt')
            else:
                self._fh = response.iter_lines()
                self._request_iterator = True  # Will need to decode the line since it will by bytes.
                pass
        else:
            if self.filename.endswith('.zst'):
                dctx = zstd.ZstdDecompressor(max_window_size=2**31)
                self._fh = io.TextIOWrapper(dctx.stream_reader(open(self.filename, 'rb')), encoding='utf-8')
            elif self.filename.endswith('.bz2'):
                self._fh = bz2.open(self.filename, 'rt')
            elif self.filename.endswith('.gz'):
                self._fh = gzip.open(self.filename, 'rt')
            else:
                self._fh = open(self.filename, 'r')
                pass
            pass

        if self.show_progress:
            file_size = self._get_file_size()
            if file_size is not None:
                self._progress = tqdm(total=file_size, unit='B', unit_scale=True)
                pass
            pass
        pass

    def _get_file_size(self) -> int:
        """
        Get the size of the file in bytes.
        """
        if self._sftp is not None:
            return self._sftp.stat(self.filename).st_size
        else:
            return os.path.getsize(self.filename)
        pass

    def close(self):
        """
        Close the file.
        """
        if self._fh is not None:
            self._fh.close()
        if self._sftp is not None:
            self._sftp.close()
        if self._progress is not None:
            self._progress.close()
            pass
        pass

    pass


class PolyWriter:
    """
    A class used to write files line by line, with support for gzip, bz2, and zst compression formats,
    as well as remote files over HTTP, HTTPS, FTP, SSH, and SFTP.

    ...

    Attributes
    ----------
    filename : str
        a string representing the file path or URL to read
    show_progress : bool
        a boolean indicating whether to show a progress bar (default is False)
    file : io.TextIOWrapper or gzip.GzipFile or bz2.BZ2File or paramiko.SFTPFile
        the file object for reading
    sftp : paramiko.SFTPClient
        the SFTP client for reading from SFTP servers
    progress : tqdm.tqdm
        the progress bar object

    Methods
    -------
    open():
        Opens the file for reading, decompressing it on the fly if necessary.
    close():
        Closes the file.
    """
    def __init__(self, filename: str):
        """
        Initialize PolyWriter with a filename.

        :param filename: The name of the file to write to.
        """
        self.filename = filename
        self._fh = None
        pass

    def __enter__(self):
        """
        Open the file for writing when entering the context.
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the file when exiting the context.
        """
        self.close()
        pass

    def open(self):
        """
        Open the file for writing, compressing it on the fly if necessary.
        """
        parsed = urlparse(self.filename)

        if parsed.scheme == 'ftp':
            print("FTP\n"
                  f"  hostname={parsed.hostname}\n"
                  f"  port={parsed.port}\n"
                  f"  username={parsed.username}\n"
                  f"  password={parsed.password}\n"
                  f"  path={parsed.path}"
            )
            # self._ftp = FTP().connect(host=parsed.hostname, port=int(parsed.port))
            # self._ftp.login(parsed.username, parsed.password)
            # self.remote_filename = os.path.basename(parsed.path)
            self._ftp = ftputil.FTPHost(parsed.hostname, parsed.username, parsed.password, port=parsed.port,
                                        session_factory=FTPSessionWrapper)
            self.remote_filename = parsed.path
            self._fh = self._ftp.open(parsed.path, 'wb')
            if parsed.path.endswith('.zst'):
                dctx = zstd.ZstdCompressor(level=22)
                self._fh = io.TextIOWrapper(dctx.stream_writer(self._fh), encoding='utf-8')
            elif self.filename.endswith('.bz2'):
                self._fh = bz2.open(self._fh, compresslevel=9, mode='wt')
            elif self.filename.endswith('.gz'):
                self._fh = gzip.open(self._fh, compresslevel=9, mode='wt')
                pass
            pass
        elif parsed.scheme in ('sftp', 'ssh'):
            # Handle SFTP URLs
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.connect(parsed.hostname, username=parsed.username, password=parsed.password)
            sftp = client.open_sftp()
            try:
                self._fh = sftp.file(parsed.path, 'wt')
            except FileNotFoundError as err:
                print(f"ERROR: No such file found: {self.filename}")
                return exit(1)
            if self.filename.endswith('.zst'):
                dctx = zstd.ZstdCompressor(level=22)
                self._fh = io.TextIOWrapper(dctx.stream_writer(self._fh), encoding='utf-8')
            elif self.filename.endswith('.bz2'):
                self._fh = bz2.open(self._fh, compresslevel=9, mode='wt')
            elif self.filename.endswith('.gz'):
                self._fh = gzip.open(self._fh, compresslevel=9, mode='wt')
                pass
            self._sftp = sftp
        else:
            if self.filename.endswith('.zst'):
                cctx = zstd.ZstdCompressor()
                self._fh = io.TextIOWrapper(cctx.stream_writer(open(self.filename, 'wb')), encoding='utf-8')
            elif self.filename.endswith('.bz2'):
                self._fh = bz2.open(self.filename, 'wt')
            elif self.filename.endswith('.gz'):
                self._fh = gzip.open(self.filename, 'wt')
            else:
                self._fh = open(self.filename, 'w')
                pass
            pass
        pass

    def write(self, data):
        """
        Write data to the file.
        """
        self._fh.write(data)
        pass

    def close(self):
        """
        Close the file.
        """
        if self._fh is not None:
            self._fh.close()
            if self._ftp is not None:
                self._ftp.close()
            pass
        pass

    pass

fmt = None
def pinfo(preface: str, filename:str, line_count:int, bytes_count:int, seconds:float):
    global fmt
    if fmt is None:
        from general.constants import CommonFormattingBase
        fmt = CommonFormattingBase()
        pass
    rate = line_count/seconds
    print(
        f"{preface} {filename}. "
        f"{line_count:,d} lines / {fmt.pbytes(bytes_count)} "
        f"at {fmt.prate(rate)} ({fmt.pbyterate(bytes_count/seconds)}). "
        f"Total time: {fmt.psecs(seconds)})."
    )
    pass


def main():
    """
    Main function, mostly for testing.
    """
    import time

    parser = argparse.ArgumentParser(description='Test reading of plain text, gzipped, bzip2, or zstandard compressed files locally and remotely.')
    parser.add_argument('files', type=str, nargs='*', default=[], help='The input file(s) to process', metavar="file")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', '-w', action='store_true', help='Write mode')
    group.add_argument('--read', '-r', action='store_true', help='Read mode')
    parser.add_argument('--input-file', '-i', type=str, help='File to read when testing read mode.')

    args = parser.parse_args()

    if args.write and not args.input_file:
        parser.error("--input-file/-i is required with --read")
        exit(1)
        pass

    # if not args.input_file and not args.output_file:
    #     return parser.error("At least one of --input-file or --output-file are required.")

    if args.read:
        for input_file in args.files:
            print(f"TESTING reading {input_file}")
            with PolyReader(input_file) as reader:
                line_count = 0
                t0 = time.monotonic()
                bytes_count = 0
                for line in reader:
                    line_count += 1
                    bytes_count += len(line)
                    pass
                # print(f"Last line: {line}")
                pinfo("FINISHED Reading.", reader.filename, line_count, bytes_count, time.monotonic() - t0)
                pass
            pass
        pass
    else:
        print(f"Will Read from {args.input_file}")
        for output_file in args.files:
            with PolyReader(args.input_file) as reader:
                with PolyWriter(output_file) as writer:
                    print(f"Writing {writer.filename}")
                    line_count = 0
                    t0 = time.monotonic()
                    bytes_count = 0
                    for line in reader:
                        line_count += 1
                        bytes_count += len(line)
                        writer.write(line)
                        pass
                    pinfo("FINISHED Writing.", writer.filename, line_count, bytes_count, time.monotonic() - t0)
                    pass
                pass
            pass
        pass
    pass

if __name__ == "__main__":
    main()
