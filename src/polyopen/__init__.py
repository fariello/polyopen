"""
polyopen - A Python module for versatile file handling.

This package exposes `polyopen`, `PolyReader`, and `PolyWriter` for easy access.
"""

from .polyopen import polyopen, PolyReader, PolyWriter, FTPSessionWrapper

__all__ = ["polyopen", "PolyReader", "PolyWriter", "FTPSessionWrapper"]
