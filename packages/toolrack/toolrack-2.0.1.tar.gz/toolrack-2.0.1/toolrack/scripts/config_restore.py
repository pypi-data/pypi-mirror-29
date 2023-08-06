"""Restore files from a list, handling permissions and ownership."""

import os
from argparse import ArgumentParser, FileType
import yaml
from glob import glob
import shutil

from ..script import Script


class FileEntry:
    """A single file/directory to install."""

    def __init__(self, name, parent_entry):
        self.name = name
        self.parent_entry = parent_entry

    def __getattr__(self, attr):
        if attr in ('mode', 'user', 'group'):
            return getattr(self.parent_entry, attr)
        raise AttributeError(attr)

    @property
    def target(self):
        """The complete target path."""
        name = self._target_name() or self.name
        return os.path.join(self.parent_entry.target, name)

    def _target_name(self):
        name_pattern = self.parent_entry.name_pattern
        if name_pattern:
            return name_pattern.format(name=os.path.basename(self.name))


class Entry:
    """An entry from the config file.

    It can be iterated and yields FileEntries for each file matching the glob.

    """

    def __init__(self, glob, target, name_pattern=None, mode=None, user=None,
                 group=None):
        self.glob = glob
        self.target = target
        self.name_pattern = name_pattern
        self.mode = mode
        self.user = user
        self.group = group

    def __iter__(self):
        return (FileEntry(name, self) for name in glob(self.glob))


class ConfigRestoreScript(Script):
    """Restore configuration files."""

    def get_parser(self):
        """Return a configured ArgumentParser."""
        parser = ArgumentParser(description=__doc__)
        parser.add_argument(
            '--no-act', '-n', action='store_true', default=False,
            help="just print actions, don't copy")
        parser.add_argument(
            'config', type=FileType('r'),
            help='config file with mapping for files/directories')
        return parser

    def main(self, args):
        entries = self._get_entries(args.config)
        for entry in entries:
            self._install_entry(entry, print_only=args.no_act)

    def _get_entries(self, config_file):
        """Return the configuration from file."""
        config = yaml.load(config_file)
        return [
            self._get_entry_details(entry, target)
            for target, entries in config.items()
            for entry in entries]

    def _get_entry_details(self, entry, target):
        """Return a Entry object from details."""
        details = {}
        if isinstance(entry, dict):
            glob, details = entry.popitem()
        else:
            glob = entry
        return Entry(
            glob, target, name_pattern=details.get('name-pattern'),
            mode=details.get('mode'), user=details.get('user'),
            group=details.get('group'))

    def _install_entry(self, entry, print_only=False):
        """Install files for an entry."""
        for file_entry in entry:
            self._print_message(file_entry)
            if print_only:
                continue

            if os.path.isdir(file_entry.name):
                shutil.copytree(file_entry.name, file_entry.target)
            elif os.path.isfile(file_entry.name):
                shutil.copy(file_entry.name, file_entry.target)

            if (file_entry.user, file_entry.group) != (None, None):
                shutil.chown(
                    file_entry.target, user=file_entry.user,
                    group=file_entry.group)
            if file_entry.mode is not None:
                os.chmod(file_entry.target, file_entry.mode)

    def _print_message(self, file_entry):
        """Print a message about the operation."""
        parts = [file_entry.target]
        if file_entry.mode is not None:
            parts.append('mode={:o}'.format(file_entry.mode))
        if file_entry.user is not None:
            parts.append('user={}'.format(file_entry.user))
        if file_entry.group is not None:
            parts.append('group={}'.format(file_entry.group))
        print('{} -> {}'.format(file_entry.name, ' '.join(parts)))


script = ConfigRestoreScript()
