import os

from plover import log, system
from plover.config import DEFAULT_SYSTEM_NAME
from plover.dictionary.base import load_dictionary
from plover.formatting import Formatter
from plover.registry import registry
from plover.steno import normalize_steno
from plover.steno_dictionary import StenoDictionary
from plover.translation import Translator

from plover_build_utils.testing import CaptureOutput, steno_to_stroke

import pytest


log.set_level(log.DEBUG)


def test_python_dictionary():
    # Setup.
    registry.update()
    system.setup(DEFAULT_SYSTEM_NAME)
    output = CaptureOutput()
    formatter = Formatter()
    formatter.set_output(output)
    translator = Translator()
    translator.add_listener(formatter.format)
    dictionary = translator.get_dictionary()
    empty_dict = StenoDictionary()
    empty_dict.save = lambda: None
    dictionary.set_dicts([empty_dict])
    # Test.
    d = load_dictionary(os.path.join(os.path.dirname(__file__), 'show_stroke.py'))
    assert d.readonly is True
    assert d.longest_key == 2
    with pytest.raises(KeyError):
        d[('STR',)]
    assert d.get(('STR',)) is None
    assert d[('STR*', 'STR')] == 'STR'
    assert d.get(('STR*', 'STR')) == 'STR'
    assert d.reverse_lookup('STR') == []
    dictionary.set_dicts([d] + dictionary.dicts)
    dictionary.set(normalize_steno('STR'), 'center')
    for steno in (
        'STR',
        'STR*',
        'STR',
        'STR',
    ):
        stroke = steno_to_stroke(steno)
        translator.translate(stroke)
    assert output.text == ' center STR center'


# Check on Python 3.6!
def test_utf8_dictionary(monkeypatch):
    monkeypatch.setenv('PYTHONIOENCODING', 'ascii')
    registry.update()
    system.setup(DEFAULT_SYSTEM_NAME)
    load_dictionary(os.path.join(os.path.dirname(__file__), 'utf8_dict.py'))
