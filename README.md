# Plover Python dictionary

Add support for Python dictionaries to Plover.


## Usage

A Python dictionary is simply a single UTF-8 source file with the following API:

``` python
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
```

For example save the following code to `show_stroke.py`:

> **Note**: make sure the file encoding is UTF-8!

``` python
LONGEST_KEY = 2

SHOW_STROKE_STENO = 'STR*'

def lookup(key):
    assert len(key) <= LONGEST_KEY, '%d/%d' % (len(key), LONGEST_KEY)
    if SHOW_STROKE_STENO != key[0]:
        raise KeyError
    if len(key) == 1:
        return ' '
    return key[1]
```

Then add it to your dictionaries stack as you would a normal dictionary.

Now, if you stroke `STR*`, then the next stroke will be shown verbatim
(untranslated), e.g. `-T STROEBG TP-R KW-GS STROEBG KR-GS S STR* STROEBG`
outputs: `the stroke for "stroke" is STROEBG`.


## Release history

### 1.2.0

* use importlib instead of exec ([#12](https://github.com/openstenoproject/plover_python_dictionary/pull/12))

### 1.1.0

* fix type checks for `lookup` and `reverse_lookup`:
  allow bound methods and functors
* fix `reverse_lookup` implementation: return a set.
* fix `__getitem__` / `get` implementations:
  when the key length is out of bounds
* fix `__contains__` implementation
* fix `__delitem__` / `__setitem__` implementations:
  raise the correct exception type

### 1.0.0

* fix possible encoding issue when loading a dictionary:
  from now on, assume and force UTF-8

### 0.5.12

* update changelog...

### 0.5.11

* drop support for Python < 3.6
* fix use of deprecated `imp` module
* rework tests to use `plover_build_utils.testing`
* use PEP 517/518

### 0.5.10

* fix `./setup.py test` handling
* fix default implementation of `reverse_lookup` to return a list (not a tuple)

### 0.5.9

* update to Plover's latest API
