from ..print import print_line, print_section
from ..state import State


def link_sources(manager, sources):
    for source in sources:
        manager.link(source)


def deploy(manager, args):
    print_line('🔍  Found {:green} dotfiles!', manager.count())

    snapshot = manager.snapshot()

    print_section(
        snapshot[State.OK],
        '✨  {count:green} dotfiles are already linked',
        show_files=False,
        level=1
    )
    print_section(
        snapshot[State.SOURCE_MISSING],
        '🕵️‍♂️  {count:red} source files are missing:',
        level=1
    )
    print_section(
        snapshot[State.TARGET_EXISTS],
        '🤔  {count:red} target files already exists (and are not links):',
        level=1
    )
    print_section(
        snapshot[State.BROKEN_LINK],
        '🚨  {count:yellow} links are broken:',
        level=1
    )
    print_section(
        snapshot[State.UNLINKED],
        '📦  {count:yellow} dotfiles are not yet linked:',
        level=1
    )

    if len(snapshot[State.UNLINKED]) > 0:
        link_sources(manager, snapshot[State.UNLINKED])
        print('')
        print_section(
            snapshot[State.UNLINKED],
            '🎉  Linked {count:green} new files:',
        )
