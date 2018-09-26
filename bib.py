import sys
from os import popen


# library:
# taken from github: wpoely86/jabref-abbreviations:
with open('list-abbreviations.txt', 'r') as f:
    lines = f.readlines()

dictionary = {}

for l in lines[1:]:
    full, abbr = l.split('=')
    full = ' '.join(full.lower().split())
    dictionary[full] = ' '.join(abbr.split())


def abbrev(_s):
    if _s.lower() in dictionary:
        return dictionary[_s.lower()]
    elif 'the' == _s.lower()[:3]:
        if _s.lower()[4:] in dictionary:
            return dictionary[_s.lower()[4:]]
    else:
        if '.' not in _s:
            print('no abbreviation for "{}"'.format(_s))
        return _s


def proc(_fname):
    with open(_fname, 'r') as _f:
        _read_str = _f.read()

    _new_fname = _fname.split('.')[0] + '_modified.bib'

    with open(_new_fname, 'w') as _f:
        while _read_str.find('journal') != -1:
            _journal = _read_str.find('journal') + 7
            _f.write(_read_str[:_journal])
            _read_str = _read_str[_journal:]
            _starting = _read_str.find('=')

            # check for unexpected string
            _find_next = False
            while _read_str[:_starting].split():
                # pulling the 'journal' to '='
                _journal = _read_str.find('journal')
                if _journal == -1:
                    _find_next = True
                    break
                _journal += 7
                _starting -= _journal
                _f.write(_read_str[:_journal])
                _read_str = _read_str[_journal:]

            _f.write(_read_str[:_starting+1])
            _read_str = _read_str[_starting+1:]
            if _find_next:
                continue

            # find the outer {} block or "" block
            _outer_count = 1
            _starting = min(_read_str.find('{'), _read_str.find('"'))
            if _starting == -1:
                break
            # unexpected string: find next
            elif _read_str[:_starting].split():
                continue

            _starting_char = _read_str[_starting]

            _f.write(_read_str[:_starting])
            _read_str = _read_str[_starting+1:]
            _p = -1

            # detect extra '{' which is paired with extra '}'
            if _starting_char == '{':
                while _outer_count > 0:
                    _p += 1
                    if '{' == _read_str[_p]:
                        _outer_count += 1
                    elif '}' == _read_str[_p]:
                        _outer_count -= 1
                # when break: p -> '}'

            else:
                _p = _read_str.find('"')

            _to_abbrev = _read_str[:_p]
            _abbreviated = abbrev(_to_abbrev)
            if _to_abbrev != _abbreviated:
                print('{:60} -> {:30}'.format(_to_abbrev, _abbreviated))

            _f.write(_starting_char + _abbreviated)
            _read_str = _read_str[_p:]
        _f.write(_read_str)

for fname in sys.argv[1:]:
    try:
        proc(fname)
    except FileExistsError:
        print('please make sure the file "{}" exists'.format(fname))

