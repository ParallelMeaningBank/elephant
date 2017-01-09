import sys


def blocks(lines):
    """
    Divides the contents of a text file into a sequence of "blocks" separated
    by empty lines and returns each block as a list of lines.
    """
    current_block = []
    for line in lines:
        if not line.rstrip():
            yield current_block
            current_block = []
        else:
            current_block.append(line)
    # In case there is no empty line at the end:
    if current_block:
        yield current_block


def list_union(lists):
    result = []
    seen = set()
    for l in lists:
        for element in l:
            if not element in seen:
                result.append(element)
                seen.add(element)
    return result


def isnumber(x):
    return isinstance(x, (int, long, float, complex))


def out(string):
    sys.stdout.write('%s' % string)


def nl():
    out('\n')
