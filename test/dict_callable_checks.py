LONGEST_KEY = 1

class Dictionary:

    def __call__(self, key):
        return 'text'

    def reverse_lookup(self, text):
        return [('STENO',)]

_dict = Dictionary()
lookup = _dict
reverse_lookup = _dict.reverse_lookup
