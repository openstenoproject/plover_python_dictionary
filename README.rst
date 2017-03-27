Add support for Python dictionaries to Plover. A Python dictionary is
simply a single module with the following API:

.. code:: python

    # Length of the longest supported key (number of strokes).
    LONGEST_KEY = 1

    # Lookup function: return the translation for <key> (a tuple of strokes)
    # or raise KeyError if no translation is available/possible.
    def lookup(key):
        assert len(key) <= LONGEST_KEY
        raise KeyError

    # Optional: return an array of stroke tuples that would translate back
    # to <text> (an empty array if not possible).
    def reverse_lookup(text):
        return []

For example with the following dictionary:

.. code:: python

    LONGEST_KEY = 2

    SHOW_STROKE_STENO = 'STR*'

    def lookup(key):
        assert len(key) <= LONGEST_KEY, '%d/%d' % (len(key), LONGEST_KEY)
        if SHOW_STROKE_STENO != key[0]:
            raise KeyError
        if len(key) == 1:
            return ' '
        return key[1]

If you stroke ``STR*``, then the next stroke will be shown verbatim
(untranslated), e.g.
``-T STROEBG TP-R KW-GS STROEBG KR-GS S STR* STROEBG`` outputs:
``the stroke for "stroke" is STROEBG``.
