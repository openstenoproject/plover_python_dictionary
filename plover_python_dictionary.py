# vim: set fileencoding=utf-8 :

import imp
import sys

from plover.steno_dictionary import StenoDictionary
from plover import resource


class PythonDictionary(StenoDictionary):

    def __init__(self):
        super(PythonDictionary, self).__init__()
        self._mod = None
        self._lookup = None
        self._reverse_lookup = None
        self.readonly = True

    def _load(self, filename):
        imp.acquire_lock()
        try:
            mod = imp.load_source('', filename)
            del sys.modules['']
        finally:
            imp.release_lock()
        self._longest_key = getattr(mod, 'LONGEST_KEY', None)
        if not isinstance(self._longest_key, int) or self._longest_key <= 0:
            raise ValueError('missing or invalid `LONGEST_KEY\' constant: %s\n' % str(longest_key))
        self._lookup = getattr(mod, 'lookup', None)
        if not isinstance(self._lookup, type(lambda x: x)):
            raise ValueError('missing or invalid `lookup\' function: %s\n' % str(lookup))
        self._reverse_lookup = getattr(mod, 'reverse_lookup', lambda x: ())
        if not isinstance(self._reverse_lookup, type(lambda x: x)):
            raise ValueError('invalid `reverse_lookup\' function: %s\n' % str(reverse_lookup))
        self._mod = mod

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __delitem__(self, key):
        raise NotImplementedError()

    def __getitem__(self, key):
        return self._lookup(key)

    def get(self, key, fallback=None):
        try:
            return self._lookup(key)
        except KeyError:
            return fallback

    def reverse_lookup(self, value):
        return self._reverse_lookup(value)
