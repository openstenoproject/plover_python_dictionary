# vim: set fileencoding=utf-8 :

import typing
import importlib.util
import sys
import os

from plover.steno_dictionary import StenoDictionary
from plover import log

class PythonDictionary(StenoDictionary):

    readonly = True

    def __init__(self):
        super().__init__()
        self._mod = None
        self._lookup = None
        self._reverse_lookup = None
        self.readonly = True

    def _load(self, filename): 
        log.info("loading Python dictionary: %s", filename)
        
        module_name = filename # include full path

        spec = importlib.util.spec_from_file_location(module_name, filename)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load module spec from {filename}")

        mod = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = mod  # Optional but allows re-imports and traceback clarity
        spec.loader.exec_module(mod)

        longest_key = getattr(mod, 'LONGEST_KEY', None)
        if not isinstance(longest_key, int) or longest_key <= 0:
            raise ValueError(f"Missing or invalid `LONGEST_KEY` constant: {longest_key}")

        lookup = getattr(mod, 'lookup', None)
        if not isinstance(lookup, typing.Callable):
            raise ValueError(f"Missing or invalid `lookup` function: {lookup}")

        reverse_lookup = getattr(mod, 'reverse_lookup', lambda x: set())
        if not isinstance(reverse_lookup, typing.Callable):
            raise ValueError(f"Invalid `reverse_lookup` function: {reverse_lookup}")

        self._mod = mod
        self._lookup = lookup
        self._longest_key = longest_key
        self._reverse_lookup = reverse_lookup

    def __contains__(self, key):
        if len(key) > self._longest_key:
            return False
        try:
            self._lookup(key)
        except KeyError:
            return False
        return True

    def __getitem__(self, key):
        if len(key) > self._longest_key:
            raise KeyError
        return self._lookup(key)

    def get(self, key, fallback=None):
        if len(key) > self._longest_key:
            return fallback
        try:
            return self._lookup(key)
        except KeyError:
            return fallback

    def reverse_lookup(self, value):
        return set(self._reverse_lookup(value))
