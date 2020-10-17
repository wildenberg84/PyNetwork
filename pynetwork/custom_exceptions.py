"""This is the custom_ module.

This module does IPv4 stuff.

TODO: rewrite module description
"""

# raised when expecting a writable memoryview, but receiving a read-only memoryview
class NonWritableMemoryviewError(Exception):
    def __init__(self, message):
        super().__init__(message)