from enum import Enum


class State(Enum):
    BROKEN_LINK = 'BROKEN_LINK'
    TARGET_EXISTS = 'TARGET_EXISTS'
    OK = 'OK'
    SOURCE_MISSING = 'SOURCE_MISSING'
    UNLINKED = 'UNLINKED'
