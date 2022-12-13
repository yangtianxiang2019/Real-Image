from django.conf import settings
from django.utils.functional import LazyObject
from django.utils.module_loading import import_string

from .base import Storage
from .filesystem import FileSystemStorage

__all__ = (
    "FileSystemStorage",
    "Storage",
    "DefaultStorage",
    "default_storage",
    "get_storage_class",
)


def get_storage_class(import_path=None):
    return import_string(import_path or settings.DEFAULT_FILE_STORAGE)


class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class()()


default_storage = DefaultStorage()
