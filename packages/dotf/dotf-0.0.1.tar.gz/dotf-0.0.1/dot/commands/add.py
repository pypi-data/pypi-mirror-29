from ..print import print_line


def add(manager, args):
    for file in args.files:
        manager.add(file)
        print_line(
            '🔗  Added {:green}',
            file
        )
