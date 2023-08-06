from ..print import print_section
from ..state import State


def status(manager, args):
    snapshot = manager.snapshot()

    print_section(
        snapshot[State.OK],
        '✨  {count:green} dotfiles are already linked'
    )
    print_section(
        snapshot[State.SOURCE_MISSING],
        '🕵️‍♂️  {count:red} source files are missing:'
    )
    print_section(
        snapshot[State.TARGET_EXISTS],
        '🤔  {count:red} target files already exists (and are not links):'
    )
    print_section(
        snapshot[State.BROKEN_LINK],
        '🚨  {count:yellow} links are broken:'
    )
    print_section(
        snapshot[State.UNLINKED],
        '📦  {count:yellow} dotfiles are not yet linked:'
    )
