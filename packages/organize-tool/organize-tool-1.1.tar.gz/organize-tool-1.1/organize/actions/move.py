import logging
import os
import shutil

from organize.utils import Path, fullpath, find_unused_filename

from .action import Action
from .trash import Trash


class Move(Action):

    """
    Move a file to a new location. The file can also be renamed.
    If the specified path does not exist it will be created.

    If you only want to rename the file and keep the folder, it is
    easier to use the Rename-Action.

    :param str dest:
        can be a format string which uses file attributes from a filter.
        If `dest` is a folder path, the file will be moved into this folder and
        not renamed.

    :param bool overwrite:
        specifies whether existing files should be overwritten.
        Otherwise it will start enumerating files (append a counter to the
        filename) to resolve naming conflicts. [Default: False]

    Examples:
        - Move into `/some/folder/` and keep filenames

          .. code-block:: yaml

              filters:
                - Move: {dest: '/some/folder/'}

        - Move to `some/path/` and change the name to include the full date

          .. code-block:: yaml

              - Move: {dest: '/some/path/some-name-{year}-{month:02}-{day:02}.pdf'}

        - Move into the folder `Invoices` on the same folder level as the file
          itself. Keep the filename but do not overwrite existing files (adds
          an index to the file)

          .. code-block:: yaml

              - Move: {dest: '{path.parent}/Invoices', overwrite: False}
    """

    def __init__(self, dest: str, overwrite=False):
        self.dest = dest
        self.overwrite = overwrite
        self.log = logging.getLogger(__name__)

    def run(self, basedir: Path, path: Path, attrs: dict, simulate: bool):
        full_path = fullpath(path)

        expanded_dest = self.fill_template_tags(
            self.dest, basedir, path, attrs)
        # if only a folder path is given we append the filename to have the full
        # path. We use os.path for that because pathlib removes trailing slashes
        if expanded_dest.endswith(('\\', '/')):
            expanded_dest = os.path.join(expanded_dest, path.name)

        new_path = fullpath(expanded_dest)
        new_path_exists = new_path.exists()
        new_path_samefile = new_path_exists and new_path.samefile(full_path)
        if new_path_exists and not new_path_samefile:
            if self.overwrite:
                self.print('File already exists')
                Trash().run(basedir, path=new_path, attrs=attrs, simulate=simulate)
            else:
                new_path = find_unused_filename(new_path)

        if new_path_samefile and new_path == full_path:
            self.print('Keep location')
        else:
            self.print('Move to "%s"' % new_path)
            if not simulate:
                self.log.info(
                    'Creating folder if not exists: %s', new_path.parent)
                new_path.parent.mkdir(parents=True, exist_ok=True)
                self.log.info('Moving "%s" to "%s"', full_path, new_path)
                shutil.move(src=str(full_path), dst=str(new_path))
        return new_path

    def __str__(self):
        return 'Move(dest=%s, overwrite=%s)' % (self.dest, self.overwrite)
