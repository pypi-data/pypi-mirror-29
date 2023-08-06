from .state import State
import os
import re


class Manager(object):
    ignored_files = (
        re.compile(r'\.git'),
    )

    def __init__(self, source_dir, target_dir):
        self.source_dir = source_dir
        self.target_dir = target_dir

    def target(self, source):
        """Builds the path to the target symlink for a given source file."""

        if os.path.isabs(source):
            source = os.path.relpath(source, self.source_dir)

        return os.path.join(self.target_dir, '.{}'.format(source))

    def reverse(self, target):
        """Builds the path to the source from given a target location."""

        if os.path.isabs(target):
            target = os.path.relpath(target, self.target_dir)

        if not target.startswith('.'):
            raise Exception(
                "This doesn't appear to be a dotfiles (its relative path from "
                "the target directory doesn't start with a '.')."
            )

        return os.path.join(self.source_dir, target[1:])

    def should_ignore(self, path):
        """Decides whether a file/directory should be ignored by dot."""
        return any([
            regexp.search(path)
            for regexp in self.ignored_files
        ])

    def walk(self, with_target=True):
        """Iterates over all (source file) -> (target link) mappings."""

        for (dirpath, _, filenames) in os.walk(self.source_dir):
            for filename in filenames:
                source = os.path.join(dirpath, filename)

                if self.should_ignore(source):
                    continue

                if with_target:
                    yield (source, self.target(source))
                else:
                    yield source

    def count(self):
        """Returns the number of files managed by this manager."""
        return len(list(self.walk(False)))

    def state(self, source):
        """Return the state of the given source file."""

        target = self.target(source)

        if not os.path.isfile(source):
            # Source file does not exist
            return State.SOURCE_MISSING

        if os.path.lexists(target):
            # Target exists

            if not os.path.exists(target):
                # Target is a broken link
                return State.BROKEN_LINK

            if os.path.islink(target) and os.path.realpath(target) == source:
                # Target si a link pointing to source
                return State.OK

            # Target is either a file or a link pointing to something else
            return State.TARGET_EXISTS

        return State.UNLINKED

    def snapshot(self):
        """Returns the state of the entire source directory."""

        snapshot = {
            state: set()
            for state in State
        }

        for source in self.walk(with_target=False):
            state = self.state(source)
            snapshot[state].add(source)

        return snapshot

    def link(self, source):
        """Creates a single link to a source file."""

        if not os.path.isabs(source):
            source = os.path.join(self.source_dir, source)

        target = self.target(source)

        dirpath = os.path.dirname(target)
        os.makedirs(dirpath, exist_ok=True)

        os.symlink(source, target)

    def add(self, target):
        """Adds a file to the tracked dotfiles."""

        # Find the associated source
        source = self.reverse(target)

        # Move existing (target) file to source
        os.rename(target, source)

        # Link
        self.link(source)
