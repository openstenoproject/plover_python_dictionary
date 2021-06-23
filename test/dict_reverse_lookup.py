_DICT = {
    ('S-G',): 'something',
    ('SPH-G',): 'something',
    ('SPH*G',): 'Something',
    ('SPH', 'THEUPBG'): 'something',
}

LONGEST_KEY = max(len(k) for k in _DICT)

def lookup(key):
    assert len(key) <= LONGEST_KEY
    return _DICT[key]

def reverse_lookup(text):
    return [
        k
        for k, v in _DICT.items()
        if v == text
    ]
