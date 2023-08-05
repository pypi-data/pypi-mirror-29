#!/usr/bin/env python
__author__ = "Gao Wang"
__copyright__ = "Copyright 2016, Stephens lab"
__email__ = "gaow@uchicago.edu"
__license__ = "MIT"

'''Handle one line in a DSC file, a customized YAML parser'''

import re, subprocess, collections
from io import StringIO
import tokenize
from .utils import is_null, str2num, cartesian_list, pairwise_list, \
    get_slice, FormatError, do_parentheses_match, find_parens

class YLine:
    '''
    Apply to a YAML line: a string or a list
    '''
    def __init__(self):
        pass

    def __call__(self, value):
        return value

    @staticmethod
    def split(value):
        '''Split value by comma outside (), [] and {}'''
        if not isinstance(value, str):
            if isinstance(value, (int, float, bool)):
                return [value]
            else:
                return value
        counts = {'(': 0,
                  ')': 0,
                  '[': 0,
                  ']': 0,
                  '{': 0,
                  '}': 0}
        res = []
        unit = ''
        for item in list(value):
            if item != ',':
                unit += item
                if item in counts.keys():
                    counts[item] += 1
            else:
                if counts['('] != counts[')'] or \
                  counts['['] != counts[']'] or \
                  counts['{'] != counts['}']:
                    # comma is inside some parenthesis
                    unit += item
                else:
                    # comma is outside any parenthesis, time to split
                    res.append(unit.strip())
                    unit = ''
        res.append(unit.strip())
        return res

    def encodeVar(self, var):
        '''
        Code multi-entry data type to string
          * For string var will add quotes to it: str -> "str"
          * For tuple / list will make it into a string like "[item1, item2 ...]"
        '''
        var = self.split(var)
        if isinstance(var, (list, tuple)):
            if len(var) == 1:
                if isinstance(var[0], str):
                    return '''"{0}"'''.format(var[0])
                else:
                    return '{}'.format(var[0])
            else:
                return '[{}]'.format(', '.join(list(map(str, var))))
        else:
            return var

    def decodeVar(self, var):
        '''
        Try to properly decode str to other data type
        '''
        # Try to convert to number
        var = str2num(var)
        # null type
        if is_null(var):
            return None
        if isinstance(var, str):
            # see if str can be converted to a list or tuple
            # and apply the same procedure to their elements
            if (var.startswith('(') and var.endswith(')') and do_parentheses_match(var[1:-1])) or \
               (var.startswith('[') and var.endswith(']') and do_parentheses_match(var[1:-1], l = '[', r = ']')):
                is_tuple = var.startswith('(')
                var = [self.decodeVar(x.strip()) for x in self.split(re.sub(r'^\(|^\[|\)$|\]$', "", var))]
                if is_tuple:
                    var = tuple(var)
        return var


class Str2List(YLine):
    '''
    Convert string to list via splitting by comma outside of parenthesis
    '''
    def __init__(self):
        YLine.__init__(self)
        self.regex = re.compile(r'(?:[^,(]|\([^)]*\))+')

    def __call__(self, value):
        if isinstance(value, str):
            # This does not work for nested parenthesis
            # return [x.strip() for x in self.regex.findall(value)]
            # Have to do it the hard way ...
            return self.split(value)
        else:
            if not isinstance(value, (collections.Mapping, list, tuple)):
                return [value]
            else:
                return value


class ExpandVars(YLine):
    '''
    Replace DSC variable place holder with actual value

    e.g. $(filename) -> "text.txt"
    '''
    def __init__(self, global_var):
        YLine.__init__(self)
        self.global_var = global_var

    def __call__(self, value):
        if self.global_var is None:
            return value
        for idx, item in enumerate(value):
            if isinstance(item, str):
                # find pattern with slicing first
                pattern = re.compile(r'\$\((.*?)\)\[(.*?)\]')
                for m in re.finditer(pattern, item):
                    tmp = [x.strip() if isinstance(x, str) else str(x) for x in self.split(self.global_var[m.group(1)])]
                    tmp = ', '.join([tmp[i] for i in get_slice('slice[' + m.group(2) + ']')[1]])
                    item = item.replace(m.group(0), '[' + tmp + ']')
                # then pattern without slicing
                pattern = re.compile(r'\$\((.*?)\)')
                for m in re.finditer(pattern, item):
                    item = item.replace(m.group(0), self.encodeVar(self.global_var[m.group(1)]))
                if item != value[idx]:
                    value[idx] = item
        return value


class ExpandActions(YLine):
    '''
    Run action entries and get values.

    Action entries are
      * R(), Python(), Shell()
      * each() and pairs()
    Untouched entries are:
      * file(), temp(), raw()
    because they'll have to be dynamically determined
    '''
    def __init__(self):
        YLine.__init__(self)
        self.method = {
            'R': self.__R,
            'Python': self.__Python,
            'Shell': self.__Shell,
            'each': self.__ForEach,
            'pairs': self.__Pairs
            }

    def __call__(self, value):
        if isinstance(value, str):
            for name in list(self.method.keys()):
                pos = [m.end() - 1 for m in re.finditer(f'{name}\(', value)]
                p_end = 0
                replacements = []
                for p in pos:
                    if p < p_end:
                        raise ValueError(f"Invalid parentheses pattern in ``{value}``")
                    p_end = find_parens(value[p:])[0]
                    replacements.append((f'{name}{value[p:p_end+p+1]}', ','.join(self.method[name](value[p:p_end+p+1]))))
                for r in replacements:
                    value = value.replace(r[0], r[1], 1)
        return value

    def __ForEach(self, value):
        raw_value = value
        value = [self.decodeVar(x) for x in self.split(value)]
        if len(value) == 1:
            raise ValueError('Cannot produce combinations for single value ``{}``! '\
                             ' Please use "," to separate input string to multiple values.'.format(raw_value))
        value = [x if isinstance(x, (list, tuple)) else [x] for x in value]
        return cartesian_list(*value)

    def __Pairs(self, value):
        value = [self.decodeVar(x) for x in self.split(value)]
        value = [x if isinstance(x, (list, tuple)) else [x] for x in value]
        return pairwise_list(*value)

    @staticmethod
    def __R(code):
        return subprocess.check_output(f"R --slave -e 'cat({code})'", \
                                       shell = True).decode('utf8').strip().split()

    @staticmethod
    def __Python(code):
        return list(eval(code))

    @staticmethod
    def __Shell(self, code):
        return subprocess.check_output(code, shell = True).decode('utf8').strip()


class CastData(YLine):
    def __init__(self):
        YLine.__init__(self)

    def __call__(self, value):
        # Recode strings
        for idx, item in enumerate(value):
            value[idx] = self.decodeVar(item)
        # Properly convert lists and tuples
        if len(value) == 1 and isinstance(value[0], list):
            if not is_null(value[0]):
                return list(value[0])
            else:
                return [None]
        else:
            res = []
            for x in value:
                if is_null(x):
                    res.append(None)
                    continue
                if isinstance(x, list):
                    # [[],[]] -> [(),()]
                    res.append(tuple(x))
                else:
                    res.append(x)
            return res


class OperationParser(YLine):
    '''
    Parse DSC sequence variables by expanding them

    Input: a string sequence of 'run'
    '''
    def __init__(self):
        YLine.__init__(self)
        self.operators = ['(', ')', ',', '+', '*']
        self.reset()

    def __str__(self):
        return self.value

    def reset(self):
        self.cache = {}
        self.cache_count = 0
        self.value = ''

    def __call__(self, value):
        if is_null(value):
            return value
        if not isinstance(value, str):
            raise TypeError("Argument must be string but it is %s." % type(value))
        value = value.strip()
        if value[-1] in ['+', '*', ',', '=', '/']:
            raise FormatError('The end of operator ``"{}"`` cannot be operator ``{}``!'.\
                              format(value, value[-1]))
        res = []
        for seq in self.split(value):
            self.reset()
            self.sequence = seq
            #seq = seq.replace(' ', '')
            for a in [self.cache_symbols,
                      self.check_syntax,
                      self.reconstruct]:
                seq = a(seq)
            res.extend(seq)
        self.value = '; '.join([' * '.join(item) if not isinstance(item, str) else item for item in res])
        return res

    def cache_symbols(self, value):
        '''cache all symbols'''
        # split with delimiter kept
        seq = [y.strip() for y in re.split(r'({})'.format("|".join([re.escape(x) for x in self.operators])), value) if y.strip()]
        new_seq = []
        # reconstruct slice wrongfully splitted e.g., sth[2,3,4]
        start_idx = 0
        for idx, item in enumerate(seq):
            if '[' in item and not ']' in item:
                # bad slice found
                new_seq.extend(seq[start_idx:idx])
                tmp = [seq[idx]]
                i = 1
                incomplete_sq = True
                while i < len(seq):
                    tmp.append(seq[idx + i])
                    if ']' in seq[idx + i]:
                        new_seq.append(''.join(tmp))
                        incomplete_sq = False
                        start_idx += idx + i + 1
                        break
                    i += 1
                if incomplete_sq:
                    raise FormatError('Incomplete ``[``/``]`` pair near {}'.format(''.join(tmp)))
        new_seq.extend(seq[start_idx:len(seq)])
        # cache all symbols
        for idx, item in enumerate(new_seq):
            if item and not item in self.operators:
                new_seq[idx] = self.__string_cache(item)
        return ''.join(new_seq)

    def check_syntax(self, value):
        ''' * ensure there are not other symbols than these keyword operators
            * ensure '+' is not connecting between parenthesis
        '''
        for x in value:
            if not x in self.operators and not x.isalnum() and x != '_':
                raise FormatError('Invalid symbol ``{}`` in sequence ``{}``'.format(x, self.sequence))
        if ')+' in value or '+(' in value:
            raise FormatError('Pairs operator ``+`` cannot be used to connect multiple variables ')
        return value

    def reconstruct(self, value):
        from .utils import non_commutative_symexpand
        value = value.replace('+', '_')
        value = value.replace(',', '+')
        res = []
        for x in str(non_commutative_symexpand(value)).split('+'):
            x = x.strip().split('*')
            if '2' in x:
                # error for '**2'
                raise FormatError("Possibly duplicated elements found in sequence {}".\
                                  format(self.sequence))
            # re-construct elements in x
            # complication: the _ operator
            tmp_1 = dict((y if '_' not in y else y.split('_')[0], y) for y in x)
            if len(tmp_1.keys()) < len(x):
                raise FormatError("Possibly duplicated elements found in sequence {}".\
                                  format(self.sequence))
            tmp_2 = []
            for y in tmp_1:
                if '_' in tmp_1[y]:
                    tmp_3 = [self.cache[i] for i in tmp_1[y].split('_')]
                    tmp_2.append('+'.join(tmp_3))
                else:
                    tmp_2.append(self.cache[tmp_1[y]])
            res.append(tuple(tmp_2) if len(tmp_2) > 1 else tmp_2[0])
        return res

    def __string_cache(self, cache):
        # return existing cache_id
        for cache_id in self.cache:
            if self.cache[cache_id] == cache:
                return cache_id
        # add a new cache_id
        self.cache_count += 1
        cache_id = 'X{}'.format(self.cache_count)
        self.cache[cache_id] = cache
        return cache_id


class LogicParser(OperationParser):
    '''
    Parse DSC sequence variables by expanding them

    Input: a string sequence of @FILTER
    '''
    def __init__(self):
        OperationParser.__init__(self)
        self.operators = ['(', ')', '|', '&', '~']

    def reconstruct(self, value):
        from .utils import bool_symexpand
        res = []
        for x in str(bool_symexpand(value)).split('|'):
            x = x.strip().strip('(').strip(')').split('&')
            tmp = [self.cache[y.strip()] if not y.strip().startswith('~') else f'not {self.cache[y.strip()[1:]]}'
                   for y in x]
            res.append(tuple(tmp) if len(tmp) > 1 else tmp[0])
        return res


class EntryFormatter:
    '''
    Run format transformation to DSC entries
    '''
    def __init__(self):
        pass

    def __call__(self, data, variables):
        actions = [ExpandActions(),
                   Str2List(),
                   ExpandVars(variables),
                   CastData()]
        return self.__Transform(data, actions)

    def __Transform(self, cfg, actions):
        '''Apply actions to items'''
        for key, value in list(cfg.items()):
            if isinstance(value, str):
                value = value.strip().strip(',')
            if isinstance(value, collections.Mapping):
                self.__Transform(value, actions)
            else:
                if key != '.FILTER':
                    for a in actions:
                        value = a(value)
                # empty list
                if is_null(value):
                    del cfg[key]
                else:
                    cfg[key] = value
        return cfg

def expand_logic(string):
    '''
    bool logic expander
    '''
    string = string.replace(' or ', '|')
    string = string.replace(' OR ', '|')
    string = string.replace(' and ', '&')
    string = string.replace(' AND ', '&')
    string = string.replace('not', '~')
    string = string.replace('NOT', '~')
    res = []
    op = LogicParser()
    for x in op(string):
        if isinstance(x, str):
            x = (x,)
        res.append(x)
    return res

def parse_filter(condition, groups = {}, dotted = True):
    '''
    parse condition statement
    After expanding, condition is a list of list
    - the outer lists are connected by OR
    - the inner lists are connected by AND
    eg: input 'x in 0 and not (y < x and y > 0)'
    output:
    [('', ['', 'x'], 'in', '0'), ('not', ['', 'y'], '<', 'x')]
    [('', ['', 'x'], 'in', '0'), ('not', ['', 'y'], '>', '0')]
    '''
    # FIXME: check legalize names
    if condition is None:
        return (None, None)
    res = []
    cond_tables = []
    symbols = ['=', '==', '!=', '>', '<', '>=', '<=', 'in']
    for and_list in expand_logic(' and '.join(condition) if isinstance(condition, (list, tuple)) else condition):
        tmp = []
        for value in and_list:
            if value.strip().lower().startswith('not '):
                value = value.strip()[4:]
                is_not = True
            else:
                value = value.strip()
                is_not = False
            tokens = [token[1] for token in tokenize.generate_tokens(StringIO(value.replace('.', '__DSC_DOT__')).readline) if token[1]]
            if not (len(tokens) == 3 and tokens[1] in symbols):
                raise FormatError(f"Condition ``{value}`` is not a supported math expression.\nSupported expressions are ``{symbols}``")
            tokens[0] = tokens[0].replace('__DSC_DOT__', '.').split('.')
            if len(tokens[0]) != 2:
                if dotted:
                    raise FormatError(f"Condition contains invalid module / parameter specification ``{'.'.join(tokens[0])}`` ")
                else:
                    tokens[0] = [''] + tokens[0]
            cond_tables.append((tokens[0][0], tokens[0][1]))
            tokens[2] = tokens[2].replace('__DSC_DOT__', '.')
            if not tokens[0][0] in groups:
                tmp.append(('not' if is_not else '', tokens[0], "==" if tokens[1] == "=" else tokens[1], tokens[2]))
            else:
                # will be connected by OR logic
                tmp.append([('not' if is_not else '', [x, tokens[0][1]], "==" if tokens[1] == "=" else tokens[1], tokens[2])
                            for x in groups[tokens[0][0]]])
        res.append(tmp)
    return res, cond_tables
