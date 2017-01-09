import codecs
import functools
import gzip
import os
import stat
import string
import sys

from collections import deque

def remove_if_present(element, list):
    try:
        list.remove(element)
    except ValueError:
        pass

def makedirs(path):
    try:
        os.makedirs(path)
    except OSError:
        pass # directory exists, TODO check if that is really the cause

def delete_if_exists(path):
    try:
        os.unlink(path)
    except OSError:
        pass

def makedirs_file(path):
    makedirs(os.path.dirname(path))

def slurp(filename, encoding='UTF-8'):
    with codecs.open(filename, encoding=encoding) as file:
        return file.read()

def slurp_stream(stream, encoding='UTF-8'):
    with codecs.getreader(encoding)(stream) as reader:
        return reader.read()

def spew(string, filename, encoding='UTF-8'):
    with codecs.open(filename, 'w', encoding=encoding) as file:
        file.write(string)

def spew_stream(string, stream, encoding='UTF-8'):
    with codecs.getwriter(encoding)(stream) as writer:
        writer.write(string)

def instantiate_file_template(src, dst, mapping):
    spew(string.Template(slurp(src)).substitute(mapping), dst)

def pad(ints):
    """Pads a list of integers with leading spaces so the results all have the
    same length."""
    strings = map(str, ints)
    length = max(map(len, strings))
    for string in strings:
        yield (length - len(string)) * ' ' + string

def lpad(string, length):
    string = str(string)
    return ' ' * (length - len(string)) + string

def rpad(string, length):
    string = str(string)
    return string + ' ' * (length - len(string))

def extsplit(filename):
    index = filename.rfind('.')
    if index == -1:
        prefix = filename
        suffix = ''
    else:
        prefix = filename[:index]
        suffix = filename[index:]
    return (prefix, suffix)

def chunks(list, chunk_size):
    for i in xrange(0, len(list), chunk_size):
        yield list[i:i + chunk_size]

def remove_duplicates(seq):
    seen = set()
    return [x for x in seq if not x in seen and not seen.add(x)]

class Idgen(object):

    def __init__(self):
        self.dictionary = {}
        self.next_id = 1

    def id_of(self, key):
        if not key in self.dictionary:
            self.dictionary[key] = self.next_id
            self.next_id += 1
        return self.dictionary[key]

class Counter(object):

    def __init__(self):
        self.dictionary = {}

    def count(self, item, times=1):
        if not item in self.dictionary:
            self.dictionary[item] = 0
        self.dictionary[item] = self.dictionary[item] + times

    def __iter__(self):
        return iter(self.dictionary)

    def __getitem__(self, item):
        return self.dictionary[item]

    def total(self):
        result = 0
        for key in self:
            result += self[key]
        return result

class AbstractMultimap(object):

    """Maps keys to multiple values."""

    def __init__(self):
        self.dictionary = {}

    def add(self, key, value):
        if not key in self.dictionary:
            self.dictionary[key] = self.new_collection()
        self.add_to_collection(self.dictionary[key], value)

    def __getitem__(self, key):
        return self.dictionary[key]

    def __contains__(self, key):
        return key in self.dictionary

class ListMultimap(AbstractMultimap):

    """Multimap where the values for each key are ordered and duplicate values
    are possible."""

    def new_collection(self):
        return []

    def add_to_collection(self, collection, value):
        collection.append(value)

class SetMultimap(AbstractMultimap):

    """Multimap where the values for each key are unique for that key, and
    unordered."""

    def new_collection(self):
        return set()

    def add_to_collection(self, collection, value):
        collection.add(value)

    def all_values(self):
        """Returns the set of all values for all keys."""
        return set.union(*self.dictionary.values())

def count_lines_in_file(path):
    result = 0
    with open(path, 'r') as f:
        for line in f:
            result += 1
    return result

def fst((a, b)):
    return a

def snd((a, b)):
    return b

def column(i, table, default=None):
    for row in table:
        if i < len(row):
            yield row[i]
        else:
            yield default

def prepare_row(row, column_width):
    for i in xrange(len(row)):
        try:
            int(row[i])
            yield lpad(row[i], column_width[i])
        except ValueError:
            yield rpad(row[i], column_width[i])

def render_table(table, big_lines_after=[], small_lines_after=[]):
    result = ''
    column_width = {}
    for i in xrange(max(map(len, table))):
        column_width[i] = max(map(len, map(str, column(i, table, default=''))))
        table_width = sum(column_width.itervalues()) + len(column_width) - 1
    for i in xrange(len(table)):
        row = table[i]
        result += ' '.join(prepare_row(row, column_width))
        result += '\n'
        if i in big_lines_after:
            result += '=' * table_width
            result += '\n'
        if i in small_lines_after:
            result += '-' * table_width
            result += '\n'
    return result

def write_tsv_file(path, rows):
    with codecs.open(path, 'w', encoding='UTF-8') as handle:
        for row in rows:
            handle.write('\t'.join(row))
            handle.write('\n')

def read_utf8(stream=sys.stdin):
    return codecs.getreader('UTF-8')(stream)

def write_utf8(stream=sys.stdout):
    return codecs.getwriter('UTF-8')(stream)

def value_or(dictionary, key, default):
    try:
        return dictionary[key]
    except KeyError:
        return default

def pairwise(iterable):
    """Takes two elements from an iterable at a time and yields them as a
    pair."""
    iterator = iterable.__iter__()
    while True:
        try:
            first = iterator.next()
        except StopIteration:
            break
        second = iterator.next()
        yield (first, second)

def windowwise(iterable, before, after):
    """Maps each item in an iterable to a window containing the specified number
    of items before and after that item, represented as a tuple. Items near the
    beginning and end have their context padded with None values."""
    size = before + 1 + after
    dq = deque([None] * before, size) # start with left padding
    for item in iterable:
        dq.append(item)
        if len(dq) == size: # when deque is full, we have a window to yield
            yield tuple(dq)
    for i in xrange(after):
        dq.append(None) # right padding
        if len(dq) == size:
            yield tuple(dq)

def pmap(f):
    return functools.partial(map, f)

def gzip_read(filename):
    with gzip.open(filename, 'rb') as f:
        return f.read()

def check_tag(element, allowed_tags):
    if not element.tag in allowed_tags:
        raise Exception('%s not in allowed tags: %s' % (element.tag,
                allowed_tags))

def make_group_writable(phile):
    os.chmod(phile, os.stat(phile).st_mode | stat.S_IWGRP)

def lines(phile):
    """
    Reads in a file as a sequence of lines.
    """
    with open(phile) as f:
        for line in f:
            yield line
