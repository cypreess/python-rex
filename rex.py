import re
import operator
from six.moves import reduce
import six

REX_CACHE = {}


class RexMatch(dict):
    """
    Dummy defaultdict implementation of matched strings. Returns `None`
    for unknown keys.
    """

    def __getitem__(self, y):
        try:
            return super(RexMatch, self).__getitem__(y)
        except KeyError:
            return None

    def get(self, k, d=None):
        ret = super(RexMatch, self).get(k, d)
        return d if ret is None else ret

    def __str__(self):
        return str(self[0]) if self[0] else ''

    def __unicode__(self):
        return six.u(self[0]) if self[0] else u''


class Rex(object):
    FLAGS = {
        'd': re.DEBUG,
        'i': re.IGNORECASE,
        'l': re.LOCALE,
        'm': re.MULTILINE,
        's': re.DOTALL,
        'u': re.UNICODE,
        'x': re.VERBOSE,
    }

    def __init__(self, action, pattern, replacement='', flags=0):
        self.action = action
        self.pattern = pattern
        self.flags = flags
        self.replacement = replacement
        self.re = re.compile(self.pattern, self.flags)

    def __process(self, text):
        if self.action == 'm':
            result = RexMatch()
            match = self.re.search(text)
            if match is not None:
                rex.group = result
                result[0] = match.group()
                result.update(enumerate(match.groups(), start=1))
                result.update(match.groupdict())
            return result
        elif self.action == 's':
            return self.re.sub(self.replacement, text, self.flags)

    def __eq__(self, other):
        return self.__process(other)

    def __call__(self, text):
        return self.__process(text)


def rex(expression, text=None, cache=True):
    rex_obj = REX_CACHE.get(expression, None)
    if cache and rex_obj:

        if text is not None:
            return text == rex_obj
        else:
            return rex_obj

    action = 'm'
    start = 0
    if expression[start] in 'ms':
        action = expression[start]
        start = 1

    delimiter = expression[start]
    end = expression.rfind(delimiter)
    if end in (-1, start):
        raise ValueError('Regular expression syntax error.')
    pattern = expression[start + 1:end]
    replacement = ''
    if action == 's':
        index = pattern.rfind(delimiter)
        if index in (-1, 0):
            raise ValueError('Regular expression syntax error.')
        replacement = pattern[index + 1:]
        pattern = pattern[:index]

    try:
        re_flags = [Rex.FLAGS[f] for f in expression[end + 1:]]
    except KeyError:
        raise ValueError('Bad flags')

    rex_obj = Rex(action, pattern, replacement, reduce(operator.or_, re_flags, 0))
    if cache:
        REX_CACHE[expression] = rex_obj

    if text is not None:
        return text == rex_obj
    else:
        return rex_obj
rex.group = RexMatch()


def rex_clear_cache():
    global REX_CACHE
    REX_CACHE = {}
