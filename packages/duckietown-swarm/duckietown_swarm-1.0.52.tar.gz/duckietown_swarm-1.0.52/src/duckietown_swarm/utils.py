from contextlib import contextmanager
import math
from tempfile import NamedTemporaryFile
import time

import base58
from contracts.utils import indent
from decorator import decorator


def get_sha256_base58(contents):
    import hashlib
    m = hashlib.sha256()
    m.update(contents)
    s = m.digest()
    return base58.b58encode(s)


def yaml_dump_omaps(s):
    from ruamel import yaml
    res = yaml.dump(s, Dumper=yaml.RoundTripDumper, allow_unicode=False)
    return res


def yaml_load_omaps(s):
    from ruamel import yaml
    res = yaml.load(s, Loader=yaml.UnsafeLoader)
    return res


@contextmanager
def tmpfile(suffix):
    ''' Yields the name of a temporary file '''
    temp_file = NamedTemporaryFile(suffix=suffix)
    try:
        yield temp_file.name
    finally:
        temp_file.close()

# -*- coding: utf-8 -*-


__all__ = [
    'memoize_simple',
]


def memoize_simple(obj):
    cache = obj.cache = {}

    def memoizer(f, *args):
        key = (args)
        if key not in cache:
            cache[key] = f(*args)
        assert key in cache

        try:
            cached = cache[key]
            return cached
        except ImportError:  # pragma: no cover  # impossible to test
            del cache[key]
            cache[key] = f(*args)
            return cache[key]

            # print('memoize: %s %d storage' % (obj, len(cache)))

    return decorator(memoizer, obj)


def pretty_print_dictionary(d):
    lengths = [len(k) for k in d.keys()]
    if not lengths:
        return 'Empty.'

    s = ""
    for k, v in d.items():
        if isinstance(k, tuple):
            k = k.__repr__()
        if s:
            s += '\n\n'
        s += k
        s += '\n\n' + indent(str(v), '  ')
    return s


def get_all_available(queue):
    ''' Gets all that are available currently. '''
    from Queue import Empty
    res = []
    while True:
        try:
            x = queue.get(block=False)
            res.append(x)
        except Empty:
            break
    return res


def get_at_least_one(queue, timeout):
    """ This waits for one, and then waits at most timeout. """
    from Queue import Empty
    s = []
    t0 = time.time()
    while True:
        try:
            block = len(s) == 0
            x = queue.get(block=block, timeout=timeout)
            s.append(x)

            if time.time() < t0 + timeout:
                wait = t0 + timeout - time.time()
                time.sleep(wait)
        except Empty:
            break

    T = time.time() - t0
    if False:
        print('Got %s objects after %.1f s (timeout %.1f s)' % (len(s), T, timeout))
    return s


def friendly_time_since(t0):
    if t0 == 0:
        return 'never'
    delta = time.time() - t0
    return duration_compact(delta)


def duration_compact(seconds):
    if seconds < 0:
        raise ValueError(seconds)
    seconds = int(math.ceil(seconds))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365.242199)

    minutes = int(minutes)
    hours = int(hours)
    days = int(days)
    years = int(years)

    duration = []
    if years > 0:
        duration.append('%dy' % years)
    else:
        if days > 0:
            duration.append('%dd' % days)
        if (days < 3) and (years == 0):
            if hours > 0:
                duration.append('%dh' % hours)
            if (hours < 3) and (days == 0):
                if minutes > 0:
                    duration.append('%dm' % minutes)
                if (minutes < 3) and (hours == 0):
                    if seconds > 0:
                        duration.append('%ds' % seconds)

    return ' '.join(duration)


class DoAtInterval():

    def __init__(self, every_s):
        self.last = 0
        self.every = every_s

    def its_time(self):
        delta = time.time() - self.last
        if delta > self.every:
            self.last = time.time()
            return True
        else:
            return False


class MakeLines():

    def __init__(self):
        self.data = ''
        self.lines_in = []

    def get_lines(self):
        for l in self.lines_in:
            yield l
        self.lines_in = []

    def push(self, ks):
        for k in ks:
            if k == '\n':
                self.lines_in.append(self.data)
                self.data = ''
            else:
                self.data += k


class LineSplitter(object):
    """ A simple utility to split an incoming sequence of chars
        in lines. Push characters using append_chars() and
        get the completed lines using lines(). """

    def __init__(self):
        self.current = ''
        self.current_lines = []

    def append_chars(self, s):
        # TODO: make this faster
        s = str(s)
        for char in s:
            if char == '\n':
                self.current_lines.append(self.current)
                self.current = ''
            else:
                self.current += char

    def lines(self):
        """ Returns a list of line; empties the buffer """
        l = list(self.current_lines)
        self.current_lines = []
        return l
