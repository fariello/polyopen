"""
polyopen - A Python module for versatile file handling.

This package exposes `polyopen`, `PolyReader`, and `PolyWriter` for easy access.
"""

__version__ = "0.1.0"
__author__ = "Gabriele Fariello"
__email__ = ""  # Leaving blank or user can fill in

from .polyopen import polyopen, PolyReader, PolyWriter, FTPSessionWrapper

__all__ = ["polyopen", "PolyReader", "PolyWriter", "FTPSessionWrapper", "__version__", "__author__"]
