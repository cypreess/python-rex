from collections import defaultdict
import re
import operator

REX_CACHE = {}

class RexMatch(defaultdict):
    def __str__(self):
        return str(self[0])

    def __unicode__(self):
        return unicode(self[0])


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
            result = RexMatch(lambda: None)
            match = self.re.search(text)
            if match is not None:
                result[0] = match.group()
                for i, m in enumerate(match.groups()):
                    result[i + 1] = m
                result.update(match.groupdict())
            return result
        elif self.action == 's':
            return self.re.sub(self.replacement, text, self.flags)

    def __eq__(self, other):
        return self.__process(other)


def rex(expression, cache=True):
    rex_obj = REX_CACHE.get(expression, None)
    if cache and rex_obj:
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
        re_flags = map(lambda f: Rex.FLAGS[f], expression[end + 1:])
    except KeyError:
        raise ValueError('Bad flags')

    rex_obj = Rex(action, pattern, replacement, reduce(operator.or_, re_flags, 0))
    if cache:
        REX_CACHE[expression] = rex_obj
    return rex_obj


def rex_clear_cache():
    global REX_CACHE
    REX_CACHE = {}