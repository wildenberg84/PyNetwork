"""
Custom Exceptions module

Containing all custom exceptions used in PyNetwork.

Classes
-------
    NonWritableMemoryviewError
    
"""

# raised when expecting a writable memoryview, but receiving a read-only memoryview
class NonWritableMemoryviewError(Exception):
# TODO: add docstring
    def __init__(self, message):
        super().__init__(message)
        
class IllegalArgumentError(ValueError):
# TODO: add docstring
    def __init__(self, message):
        super().__init__(message)
