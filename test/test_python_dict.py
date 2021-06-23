from pathlib import Path

from plover.dictionary.base import load_dictionary
from plover_build_utils.testing import dictionary_test

from plover_python_dictionary import PythonDictionary


def _test_dict_path(name):
    return Path(__file__).parent / f'dict_{name}.py'


@dictionary_test
class TestPythonDictionary:

    DICT_CLASS = PythonDictionary
    DICT_EXTENSION = 'py'
    DICT_REGISTERED = True
    DICT_SUPPORT_SEQUENCE_METHODS = False
    DICT_SUPPORT_REVERSE_LOOKUP = False
    DICT_LOAD_TESTS = (
        lambda: (
            'show_stroke',
            '''
            # Present.
            "STR*": ' ',
            "STR*/STR": 'STR',
            "STR*/TEFT": 'TEFT',
            # Missing.
            "STR*/TEFT/-G": None,
            "TEFT": None,
            "TEFT/-G": None,
            '''),
        lambda: (
            'utf8',
            '''
            # Present.
            "STR*": '(╯°□°）╯︵ ┻━┻',
            "TEFT": '(╯°□°）╯︵ ┻━┻',
            "THROE": '(╯°□°）╯︵ ┻━┻',
            # Missing.
            "STR*/STR": None,
            "STR*/TEFT": None,
            "STR*/TEFT/-G": None,
            "TEFT/-G": None,
            '''),
    )
    DICT_SAMPLE = 'show_stroke'

    @staticmethod
    def make_dict(name):
        return _test_dict_path(name).read_bytes()


@dictionary_test
class TestPythonDictionaryWithReverseLookup(TestPythonDictionary):

    DICT_SUPPORT_REVERSE_LOOKUP = True
    DICT_LOAD_TESTS = (
        lambda: (
            'reverse_lookup',
            '''
            'S-G': 'something',
            'SPH-G': 'something',
            'SPH*G': 'Something',
            'SPH/THEUPBG': 'something',
            '''),
    )
    DICT_SAMPLE = 'reverse_lookup'


# Check on Python 3.6!
def test_utf8_dictionary(monkeypatch):
    monkeypatch.setenv('PYTHONIOENCODING', 'ascii')
    load_dictionary(str(_test_dict_path('utf8')))


def test_callable_checks():
    d = load_dictionary(str(_test_dict_path('callable_checks')))
    d[('TEFT',)] == 'text'
    d.reverse_lookup('text') == {('STENO',)}
