from contextlib import contextmanager
from typing import Callable, TypeVar

import fs.base
import fs.osfs

from .conf import mc
from .path import Path


class FileSystem:
    """
    Abstract filesystem. Could be one of these states:

    - Instance of fs.base.FS
    - Callable[[], Instance of fs.base.FS], including fs.base.FS itself (like OSFS).

    Note FileSystem is designed to work in lazy, thus before `with self.open()` is called,

    """

    def __init__(self, filesystem=None, base_path='.'):
        if isinstance(filesystem, FileSystem):
            self.filesystem = filesystem.filesystem
            self.base_path = filesystem.base_path
        else:
            self.filesystem = filesystem
            self.base_path = base_path

    def _fs_args(self, base_path=None):
        import fs.memoryfs
        if self.filesystem == fs.memoryfs.MemoryFS:
            return ()
        else:
            if base_path is None:
                return (self.base_path,)
            else:
                return (base_path,)

    @contextmanager
    def open(self, base_path=None) -> fs.base.FS:
        """
        Returns opened instance of fs.base.FS.
        """
        try:
            if isinstance(self.filesystem, fs.base.FS):
                self.filesystem.check()
                if base_path is not None:
                    raise TypeError(
                        "Argument base_path must be non for instanced filesystem.")
                yield self.filesystem
            else:
                with self.filesystem(*self._fs_args(base_path)) as fs_instance:
                    yield fs_instance
        except Exception as e:
            raise e

    @property
    def info(self):
        """
        Returns Dict of basic types or str, i.e. able to serialized by JSON.
        """
        with self.open() as fs:
            return str(fs)


class ObjectOnFileSystem:
    def __init__(self, filesystem: FileSystem, path: Path):
        if filesystem is None:
            filesystem = mc.default_filesystem
        self.filesystem = FileSystem(filesystem)
        self.path = Path(path)

    @property
    def info(self):
        return {'filesystem': self.filesystem.info,
                'path': self.path.s}

    def exists(self):
        with self.filesystem.open() as fs:
            return fs.exists(self.path.s)

    def match(self, patterns):
        with self.filesystem.open() as sfs:
            return sfs.match(patterns, self.path.s)

    def system_path(self):
        import fs.errors
        with self.filesystem.open() as sfs:
            try:
                return Path(sfs.getsyspath(self.path.s)).s
            except fs.errors.NoSysPath:
                return self.path.s

    def copy_to(self, target_path):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError
