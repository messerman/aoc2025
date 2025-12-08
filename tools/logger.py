import os
from enum import Enum

class DebugLevel(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4

DEBUG_LEVEL = DebugLevel[os.environ['DEBUG_LEVEL'].upper()] if 'DEBUG_LEVEL' in os.environ else DebugLevel.INFO

class DebugLogger:
    @classmethod
    def log(cls, level: DebugLevel, val, *args, **kwargs):
        if level.value >= DEBUG_LEVEL.value:
            printable_args = ' '.join([str(val)] + list(map(str,args)))
            print(f'[{level.name}] {printable_args}', **kwargs)

    @classmethod
    def trace(cls, val, *args, **kwargs):
        cls.log(DebugLevel.TRACE, val, *args, **kwargs)

    @classmethod
    def debug(cls, val, *args, **kwargs):
        cls.log(DebugLevel.DEBUG, val, *args, **kwargs)

    @classmethod
    def info(cls, val, *args, **kwargs):
        cls.log(DebugLevel.INFO, val, *args, **kwargs)

    @classmethod
    def warn(cls, val, *args, **kwargs):
        cls.log(DebugLevel.WARN, val, *args, **kwargs)

    @classmethod
    def error(cls, val, *args, **kwargs):
        cls.log(DebugLevel.ERROR, val, *args, **kwargs)

