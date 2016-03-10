# vim: set fileencoding=utf-8 :

import imp
import sys

from plover.steno_dictionary import StenoDictionary
from plover.exception import DictionaryLoaderException
from plover import resource


class PythonDictionary(StenoDictionary):

    def __init__(self, mod):
        super(PythonDictionary, self).__init__()
        self._mod = mod
        self._longest_key = mod.LONGEST_KEY
        if not hasattr(mod, 'reverse_lookup'):
            mod.reverse_lookup = lambda value: ()

    def reverse_lookup(self, value):
        return self._mod.reverse_lookup(value)

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __delitem__(self, key):
        raise NotImplementedError()

    def __getitem__(self, key):
        return self._mod.lookup(key)


def load_dictionary(name):
    filename = resource.resource_filename(name)
    imp.acquire_lock()
    try:
        try:
            mod = imp.load_source('', filename)
        except Exception as e:
            raise DictionaryLoaderException('Could not load dictionary: %s\n' % str(e))
        else:
            del sys.modules['']
    finally:
        imp.release_lock()
    longest_key = getattr(mod, 'LONGEST_KEY', None)
    if not isinstance(longest_key, int) or longest_key <= 0:
        raise DictionaryLoaderException('Invalid dictionary: missing or invalid `LONGEST_KEY\' constant: %s\n' % str(longest_key))
    lookup = getattr(mod, 'lookup', None)
    if not isinstance(lookup, type(lambda x: x)):
        raise DictionaryLoaderException('Invalid dictionary: missing or invalid `lookup\' function: %s\n' % str(lookup))
    reverse_lookup = getattr(mod, 'reverse_lookup', None)
    if reverse_lookup is not None and not isinstance(reverse_lookup, type(lambda x: x)):
        raise DictionaryLoaderException('Invalid dictionary: invalid `reverse_lookup\' function: %s\n' % str(reverse_lookup))
    return PythonDictionary(mod)
