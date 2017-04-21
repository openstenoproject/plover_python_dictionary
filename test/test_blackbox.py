
import os
import unittest

from plover import log, system
from plover.config import DEFAULT_SYSTEM_NAME
from plover.dictionary.base import load_dictionary
from plover.formatting import Formatter
from plover.registry import registry
from plover.steno import normalize_steno, Stroke
from plover.steno_dictionary import StenoDictionary
from plover.translation import Translator


log.set_level(log.DEBUG)


class CaptureOutput(object):

    def __init__(self):
        self.instructions = []
        self.text = u''

    def send_backspaces(self, n):
        assert n <= len(self.text)
        self.text = self.text[:-n]
        self.instructions.append(('b', n))

    def send_string(self, s):
        self.text += s
        self.instructions.append(('s', s))

    def send_key_combination(self, c):
        self.instructions.append(('c', c))

    def send_engine_command(self, c):
        self.instructions.append(('e', c))

        dictionary = StenoDictionary()
        dictionary.save = lambda: None
        self.dictionary.set_dicts([dictionary])

def steno_to_stroke(steno):
    stroke = Stroke(())
    stroke.rtfcre = steno
    return stroke


class BlackboxTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        registry.update()
        system.setup(DEFAULT_SYSTEM_NAME)

    def setUp(self):
        self.output = CaptureOutput()
        self.formatter = Formatter()
        self.formatter.set_output(self.output)
        self.translator = Translator()
        self.translator.add_listener(self.formatter.format)
        self.dictionary = self.translator.get_dictionary()
        dictionary = StenoDictionary()
        dictionary.save = lambda: None
        self.dictionary.set_dicts([dictionary])

    def test_basic(self):
        d = load_dictionary(os.path.join(os.path.dirname(__file__), 'show_stroke.py'))
        self.assertEqual(d.readonly, True)
        self.assertEqual(d.longest_key, 2)
        with self.assertRaises(KeyError):
            d[('STR',)]
        self.assertEqual(d.get(('STR',)), None)
        self.assertEqual(d[('STR*', 'STR')], 'STR')
        self.assertEqual(d.get(('STR*', 'STR')), 'STR')
        self.assertEqual(d.reverse_lookup('STR'), ())
        self.dictionary.set_dicts([d] + self.dictionary.dicts)
        self.dictionary.set(normalize_steno('STR'), u'center')
        for steno in (
            'STR',
            'STR*',
            'STR',
            'STR',
        ):
            stroke = steno_to_stroke(steno)
            self.translator.translate(stroke)
        self.assertEqual(self.output.text, u' center STR center')
