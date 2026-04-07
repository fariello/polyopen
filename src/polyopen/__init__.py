"""
polyopen - A Python module for versatile file handling.

This package exposes `PolyReader` and `PolyWriter` for easy access.
"""

from .polyopen import PolyReader, PolyWriter, FTPSessionWrapper

__all__ = ["PolyReader", "PolyWriter", "FTPSessionWrapper"]
