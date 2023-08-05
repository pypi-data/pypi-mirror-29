#!/usr/bin/env python
__author__ = "Gao Wang"
__copyright__ = "Copyright 2016, Stephens lab"
__email__ = "gaow@uchicago.edu"
__license__ = "MIT"
'''
This file defines methods to load and preprocess DSC scripts
'''

import os, re, itertools, copy, subprocess
import collections
from xxhash import xxh32 as xxh
from sos.utils import env
from .utils import FormatError, strip_dict, find_nested_key, merge_lists, flatten_list, uniq_list, \
     try_get_value, dict2str, set_nested_value, update_nested_dict, locate_file, filter_sublist, OrderedDict, \
     yaml
from .addict import Dict as dotdict
from .syntax import *
from .line import OperationParser, EntryFormatter, parse_filter
from .plugin import Plugin
__all__ = ['DSC_Script', 'DSC_Pipeline']


class DSC_Script:
    '''Parse a DSC script
     * provides self.steps, self.runtime that contain all DSC information needed for a run
    '''
    def __init__(self, content, output = None, sequence = None, extern = None):
        self.content = dict()
        if os.path.isfile(content):
            dsc_name = os.path.split(os.path.splitext(content)[0])[-1]
            script_path = os.path.dirname(os.path.expanduser(content))
            content = open(content).readlines()
        else:
            content = [x.rstrip() + '\n' for x in content.split('\n') if x.strip()]
            if len(content) == 0:
                raise IOError(f"Invalid DSC script input!")
            if len(content) == 1:
                raise IOError(f"Cannot find file ``{content[0]}``")
            dsc_name = 'DSCStringIO'
            script_path = None
        res = exe = ''
        for line in content:
            if line.strip().startswith('@'):
                line = line.replace('@', '.', 1)
            if line.strip().startswith('*'):
                line = line.replace('*', '..', 1)
            if not DSC_BLOCK_CONTENT.search(line) and not line.startswith('#'):
                if res and exe:
                    self.update(res, exe)
                    res = exe = ''
                text = line.split(':')
                if len(text) != 2 or (len(text[1].strip()) == 0 and text[0].strip() != 'DSC'):
                    raise FormatError(f'Invalid syntax ``{line}``. '\
                                      'Should be in the format of ``module names: module executables``')
                res += f'{text[0]}:\n'
                exe = text[1].strip()
            else:
                res += line
        self.update(res, exe)
        self.propagate_derived_block()
        global_vars = try_get_value(self.content, ('DSC', 'global'))
        self.set_global_vars(global_vars)
        self.content = EntryFormatter()(self.content, global_vars)
        self.extract_modules()
        self.runtime = DSC_Section(self.content['DSC'], sequence, output, extern)
        if self.runtime.output is None:
            self.runtime.output = dsc_name
        for k in self.runtime.sequence_ordering:
            if k not in self.content:
                raise FormatError(f"Module ``{k}`` is not defined!\nAvailable modules are ``{[x for x in self.content.keys() if x != 'DSC']}``")
        self.modules = dict([(x, DSC_Module(x, self.content[x], self.runtime.options, script_path))
                             for x in self.runtime.sequence_ordering.keys()])
        for m in self.modules.values():
            if m.plugin.name == 'R':
                self.runtime.rlib.append('dscrutils@stephenslab/dsc2/dscrutils (0.2.5+)')
                break
        # FIXME: maybe this should be allowed?
        self.runtime.check_looped_computation()

    def update(self, text, exe):
        try:
            block = yaml.load(''.join(text))
        except Exception as e:
            if type(e).__name__ == 'DuplicateKeyError':
                raise FormatError(f"Duplicate keys found in\n``{''.join(text)}``")
            else:
                raise FormatError(e)
        name = re.sub(re.compile(r'\s+'), '', list(block.keys())[0])
        block[name] = block.pop(list(block.keys())[0])
        if block[name] is None:
            block[name] = dict()
        if exe:
            block[name]['.EXEC'] = exe
        self.content.update(block)

    def set_global_vars(self, gvars):
        if gvars is None:
            return
        for v in gvars:
            for block in self.content:
                keys = list(find_nested_key(v, self.content[block]))
                for k in keys:
                    set_nested_value(self.content[block], k, gvars[v])
        # FIXME: have to decide if we need to set global options, or not?

    def propagate_derived_block(self):
        '''
        Name of derived blocks looks like: "derived(base)"
        This function first figures out sorted block names such that derived block always follows the base block
        Then it propagate self.content derived blocks
        '''
        base = []
        blocks = []
        derived = dict()
        for block in self.content:
            groups = DSC_DERIVED_BLOCK.search(block.strip())
            if groups:
                derived[block] = (groups.group(1).strip(), groups.group(2).strip())
            else:
                base.append(block)
                blocks.append(block)
        if len(derived) == 0:
            return
        # Check looped derivations: x(y) and y(x)
        tmp = [sorted(x) for x in derived.values()]
        for item in ((i, tmp.count(i)) for i in tmp):
            if item[1] > 1:
                raise FormatError(f"Looped block inheritance: {item[0][0]}({item[0][1]}) and {item[0][1]}({item[0][0]})!")
        # Check self-derivation and non-existing base
        tmp = base + [x[0] for x in derived.values()]
        for item in derived.values():
            if item[0] == item[1]:
                raise FormatError(f"Looped block inheritance: {item[0]}({item[0]})!")
            if item[1] not in tmp:
                raise FormatError(f"Base block does not exist: {item[0]}({item[1]})!")
        #
        derived_cycle = itertools.cycle(derived.values())
        while True:
            item = next(derived_cycle)
            if item[1] in base:
                base.append(item[0])
                name = f'{item[0]}({item[1]})'
                if name not in blocks:
                    blocks.append(name)
            if len(blocks) == len(self.content.keys()):
                break
        # propagate data
        for block in blocks:
            if block in derived:
                self.content[derived[block][0]] = update_nested_dict(
                    copy.deepcopy(self.content[derived[block][1]]), self.content[block])
                del self.content[block]
        return

    def extract_modules(self):
        if 'DSC' not in self.content:
            raise FormatError('Cannot find required section ``DSC``!')
        res = dict()
        for block in self.content:
            if block == 'DSC':
                continue
            # expand module executables
            modules = block.split(',')
            if len(modules) != len(self.content[block]['.EXEC']) and len(self.content[block]['.EXEC']) > 1:
                raise FormatError(f"``{len(modules)}`` modules ``{modules}`` does not match ``{len(self.content[block]['.EXEC'])}`` executables ``{self.content[block]['.EXEC']}``. " \
                                 "Please ensure modules and executables match.")
            if len(modules) > 1 and len(self.content[block]['.EXEC']) == 1:
                self.content[block]['.EXEC'] = self.content[block]['.EXEC'] * len(modules)
            # collection module specific parameters
            tmp = dict([(module, dict([('global', dict()), ('local', dict())])) for module in modules])
            for key in self.content[block]:
                if key.startswith('.') and key not in DSC_MODP:
                    # then possibly it is executables
                    # we'll update executable specific information
                    for m in key[1:].split(','):
                        if m.strip() not in modules:
                            raise FormatError(f'Undefined decoration ``@{m.strip()}``.')
                        else:
                            for kk, ii in self.content[block][key].items():
                                if isinstance(ii, collections.Mapping):
                                    if not kk.startswith('.'):
                                        raise FormatError(f'Invalid decoration ``{kk}``. Decorations must start with ``@`` symbol.')
                                    if kk not in DSC_MODP:
                                        raise FormatError(f'Undefined decoration ``@{kk[1:]}``.')
                                    else:
                                        continue
                            tmp[m.strip()]['local'].update(self.content[block][key])
                elif key == '.EXEC':
                    for idx, module in enumerate(modules):
                        tmp[module]['global'][key] = self.content[block][key][idx]
                elif key not in DSC_MODP and isinstance(self.content[block][key], collections.Mapping):
                    raise FormatError(f'Invalid decoration ``{key}``. Decorations must start with ``@`` symbol.')
                else:
                    for module in modules:
                        tmp[module]['global'][key] = self.content[block][key]
            # parse input / output / meta
            # output has $ prefix, meta has . prefix, input has no prefix
            for module in tmp:
                if module in res:
                    raise FormatError(f'Duplicate module definition {module}')
                res[module] = dict([('input', dict()), ('output', dict()), ('meta', dict())])
                for item in ['global', 'local']:
                    for key in tmp[module][item]:
                        if key.startswith('$'):
                            res[module]['output'][key[1:]] = tmp[module][item][key]
                        elif key.startswith('.'):
                            res[module]['meta'][key[1:].lower()] = tmp[module][item][key]
                        else:
                            res[module]['input'][key] = tmp[module][item][key]
        res['DSC'] = self.content['DSC']
        self.content = res

    def get_sos_options(self, name, content):
        # FIXME: should use wait when local host
        out = dotdict()
        out.verbosity = env.verbosity
        # no-wait when extern task
        out.__wait__ = True
        out.__no_wait__ = False
        out.__targets__ = []
        # FIXME: add more options here
        out.__queue__ = 'localhost'
        # FIXME: when remote is used should make it `no_wait`
        # Yet to observe the behavior there
        out.__remote__ = None
        out.dryrun = False
        # FIXME
        out.__dag__ = '.sos/.dsc/{}.dot'.format(name)
        # FIXME: port the entire resume related features
        out.__resume__ = False
        # FIXME: use config info
        out.__config__ = '.sos/.dsc/{}.conf.yml'.format(name)
        if not os.path.isfile(out.__config__):
            with open(out.__config__, 'w') as f:
                f.write('name: dsc')
        out.update(content)
        return out

    def init_dsc(self, args, env):
        os.makedirs('.sos/.dsc', exist_ok = True)
        if os.path.dirname(self.runtime.output):
            os.makedirs(os.path.dirname(self.runtime.output), exist_ok = True)
        if env.verbosity > 2:
            env.logfile = os.path.basename(self.runtime.output) + '.log'
            if os.path.isfile(env.logfile):
                os.remove(env.logfile)
        if os.path.isfile('.sos/transcript.txt'):
            os.remove('.sos/transcript.txt')

    def dump(self):
        res = dict([('Modules', self.modules),
                    ('DSC', dict([("Sequence", self.runtime.sequence),
                                  ("Ordering", [(x, y) for x, y in self.runtime.sequence_ordering.items()])]))])
        return res

    def __str__(self):
        res = '# Modules\n' + '\n'.join([f'## {x}\n```yaml\n{y.dump()}\n```' for x, y in self.modules.items()]) \
              + f'\n# DSC\n```yaml\n{self.runtime}\n```'
        return res

class DSC_Module:
    def __init__(self, name, content, global_options = None, script_path = None):
        # module name
        self.name = name
        # params: alias, value
        self.p = OrderedDict()
        # return variables (to plugin): alias, value
        self.rv = OrderedDict()
        # return files: alias, ext
        self.rf = OrderedDict()
        # exec
        self.exe = None
        # script plugin object
        self.plugin = None
        # runtime variables
        self.workdir = None
        self.is_extern = None
        self.libpath = None
        self.path = None
        # dependencies
        self.depends = []
        # check if it runs in shell
        self.shell_run = None
        # Now init these values
        self.set_options(global_options, try_get_value(content, ('meta', 'conf')))
        self.set_exec(content['meta']['exec'])
        self.set_input(try_get_value(content, 'input'), try_get_value(content, ('meta', 'alias')))
        self.set_output(content['output'])
        self.apply_input_operator()
        # parameter filter:
        self.ft = self.apply_input_filter(try_get_value(content, ('meta', 'filter')))
        self.check_shell()

    def set_exec(self, exec_var):
        # FIXME: need to implement inline eg R()
        exec_var = tuple(exec_var.split())
        self.exe = ' '.join([locate_file(exec_var[0], self.path)] + list(exec_var[1:]))
        self.plugin = Plugin(os.path.splitext(exec_var[0])[1].lstrip('.'), xxh(self.exe).hexdigest())
                        # re.sub(r'^([0-9])(.*?)', r'\2', textMD5(data.command)))

    def check_shell(self):
        # FIXME: check if the exec is meant to be executed from shell
        # True only if command has $ parameters and they exist in parameter list
        # Also this conflicts with self.rv: self.shell_run == True && len(self.rv) == 0
        self.shell_run = False
        if not self.shell_run and len(self.rv) > 0:
            # make it a list in order to readily merge with other self.rf items
            self.rf['DSC_AUTO_OUTPUT_'] = ['rds']

    def set_output(self, return_var):
        '''
        Figure out if output is a variable, file or plugin
        '''
        for key, value in return_var.items():
            if len(value) > 1:
                raise FormatError(f"Output ``{key}`` cannot contain multiple elements ``{value}``")
            value = value[0]
            in_input = try_get_value(self.p, value)
            if in_input:
                # output is found in input
                # and input is potentially a list
                # so have to figure out if a file is involved
                for p in in_input:
                    if not isinstance(p, str):
                        continue
                    groups = DSC_FILE_OP.search(p)
                    if groups:
                        try:
                            self.rf[key].append(groups.group(1))
                        except Exception as e:
                            self.rf[key] = [groups.group(1)]
                # are there remaining values not file()?
                if key in self.rf and len(self.rf[key]) < len(in_input):
                    raise FormatError(f"Return ``{key}`` in ``{in_input}`` cannot be a mixture of file() and module input")
            if key in self.rf:
                continue
            # now decide this new variable is a file or else
            groups = DSC_ASIS_OP.search(value)
            if groups:
                self.rv[key] = groups.group(1)
                continue
            # For file
            groups = DSC_FILE_OP.search(value)
            if groups:
                self.rf[key] = [groups.group(1)]
            else:
                self.rv[key] = value

    def set_options(self, common_option, spec_option):
        # FIXME: have to ensure @CONF is a list
        spec_option = dict([(x.strip() for x in item.split('=', 1)) for item in spec_option]) if spec_option is not None else dict()
        workdir1 = try_get_value(common_option, 'work_dir')
        workdir2 = try_get_value(spec_option, 'work_dir')
        libpath1 = try_get_value(common_option, 'lib_path')
        libpath2 = try_get_value(spec_option, 'lib_path')
        path1 = try_get_value(common_option, 'exec_path')
        path2 = try_get_value(spec_option, 'exec_path')
        extern1 = try_get_value(common_option, 'submit')
        extern2 = try_get_value(spec_option, 'submit')
        self.workdir = workdir2 if workdir2 is not None else workdir1
        self.libpath = libpath2 if libpath2 is not None else libpath1
        self.path = path2 if path2 is not None else path1
        self.is_extern = extern2 if extern2 is not None else extern1

    def set_input(self, params, alias):
        if params is not None:
            self.p.update(params)
        if isinstance(alias, collections.Mapping):
            valid = False
            for module in alias:
                if module == self.name or module == '..':
                    alias = alias[module]
                    valid = True
                    break
            if not valid:
                raise FormatError(f"Cannot find module ``{self.name}`` in @ALIAS specification ``{list(alias.keys())}``.")
        if isinstance(alias, collections.Mapping):
            raise FormatError(f"Invalid @ALIAS format for module ``{self.name}`` (has to be formatted `alias = variable`).")
        alias = dict([(x.strip() for x in item.split('=', 1)) for item in alias]) if alias is not None else dict()
        # Swap parameter key with alias when applicable
        for k1, k2 in list(alias.items()):
            if k2 in self.p:
                self.p[k1] = self.p.pop(k2)
                del alias[k1]
        # Handle special alias
        # Currently it is list() / dict()
        for k1, k2 in list(alias.items()):
            groups = DSC_PACK_OP.search(k2)
            if groups:
                self.plugin.set_container(k1, groups.group(2), self.p)
                del alias[k1]
        if len(alias):
            raise FormatError(f'Invalid @ALIAS for module ``{self.name}``:\n``{dict2str(alias)}``')

    def make_filter_statement(self, ft):
        ft = parse_filter(ft, dotted = False)[0]
        res = []
        variables = uniq_list(flatten_list([[ii[1][1] for ii in i] for i in ft]))
        for i in ft:
            tmp = []
            for ii in i:
                if len(ii[0]):
                    tmp.append(f'{ii[0]} (_{ii[1][1]} {ii[2]} {ii[3] if not ii[3] in variables else "_" + ii[3]})'.strip())
                else:
                    tmp.append(f'_{ii[1][1]} {ii[2]} {ii[3] if not ii[3] in variables else "_" + ii[3]}'.strip())
            res.append(f"({' and '.join(tmp)})")
        return ' or '.join(res)

    def apply_input_filter(self, ft):
        if ft is None or len(ft) == 0:
            return None
        if isinstance(ft, collections.Mapping):
            valid = False
            for module in ft:
                if module == self.name or module == '..':
                    ft = ft[module]
                    valid = True
                    break
            if not valid:
                raise FormatError(f"Cannot find module ``{self.name}`` in @FILTER specification ``{list(ft.keys())}``.")
        if isinstance(ft, collections.Mapping):
            raise FormatError(f"Invalid @FILTER format for module ``{self.name}`` (cannot be a key-value mapping).")
        raw_rule = ft
        ft = self.make_filter_statement(ft)
        # Verify it
        statement = ';'.join([f"{k} = {str(self.p[k])}" for k in self.p])
        value_str = ','.join([f'_{x}' for x in self.p.keys()])
        loop_str = ' '.join([f"for _{x} in {x}" for x in self.p])
        statement += f';print(len([({value_str}) {loop_str} if {ft}]))'
        try:
            ret = subprocess.check_output(f"python -c '''{str(statement)}'''", shell = True).decode('utf-8').strip()
        except:
            raise FormatError(f"Invalid @FILTER: ``{raw_rule}``!")
        if int(ret) == 0:
            raise FormatError(f"No parameter combination satisfies @FILTER ``{raw_rule}``!")
        return ft

    def apply_input_operator(self):
        '''
        Do the following:
        * convert string to raw string, leave alone `$` variables
        * strip off raw() operator
        * Handle file() parameter based on context
        '''
        for k, p in list(self.p.items()):
            values = []
            for p1 in p:
                if isinstance(p1, str):
                    if DSC_ASIS_OP.search(p1):
                        p1 = DSC_ASIS_OP.search(p1).group(1)
                    elif DSC_FILE_OP.search(p1):
                        # p1 is file extension
                        file_ext = DSC_FILE_OP.search(p1).group(1)
                        if k in self.rf:
                            # This file is to be saved as output
                            # FIXME: have to figure out what is the index of the output
                            self.plugin.add_input(k, '${_output:r}')
                            continue
                        else:
                            # This file is a temp file
                            self.plugin.add_tempfile(k, file_ext)
                            continue
                    else:
                        if not p1.startswith('$'):
                            p1 = repr(p1)
                if isinstance(p1, tuple):
                    # FIXME format_tuple has to be defined for shell as well
                    p1 = self.plugin.format_tuple(p1)
                values.append(p1)
            if len(values) == 0:
                del self.p[k]
            else:
                self.p[k] = values

    def __str__(self):
        return dict2str(self.dump())

    def dump(self):
        return strip_dict(dict([('name', self.name),
                                ('dependencies', self.depends), ('command', self.exe),
                                ('input', self.p), ('input_filter', self.ft),
                                ('output_variables', self.rv),
                                ('output_files', self.rf),  ('shell_status', self.shell_run),
                                ('plugin_status', self.plugin.dump()),
                                ('runtime_options', dict([('exec_path', self.path),
                                                          ('workdir', self.workdir),
                                                          ('library_path', self.libpath)]))]),
                          mapping = dict, skip_keys = ['input'])


class DSC_Section:
    def __init__(self, content, sequence, output, extern):
        self.content = content
        if 'run' not in self.content:
            raise FormatError('Missing required ``DSC::run``.')
        if 'output' not in self.content:
            raise FormatError('Missing required ``DSC::output``.')
        self.output = output if output else self.content['output'][0]
        self.OP = OperationParser()
        self.regularize_ensemble()
        # FIXME: check if sequence input is of the right type
        # and are valid modules
        self.groups = dict()
        self.concats = dict()
        self.sequence = self.content['run']
        if sequence is not None:
            self.sequence = sequence
        self.sequence = [(x,) if isinstance(x, str) else x
                         for x in sum([self.OP(self.expand_ensemble(y)) for y in self.sequence], [])]
        self.sequence = filter_sublist(self.sequence)
        # FIXME: check if modules involved in sequence are indeed defined.
        self.sequence_ordering = self.__merge_sequences(self.sequence)
        self.options = dict()
        self.options['work_dir'] = self.content['work_dir'] if 'work_dir' in self.content else './'
        self.options['lib_path'] = self.content['lib_path'] if 'lib_path' in self.content else None
        self.options['exec_path'] = self.content['exec_path'] if 'exec_path' in self.content else None
        if extern:
            self.options['submit'] = True
        else:
            self.options['submit'] = self.content['submit'] if 'submit' in self.content else None
        self.rlib = self.content['R_libs'] if 'R_libs' in self.content else []
        self.pymodule = self.content['python_modules'] if 'python_modules' in self.content else []

    @staticmethod
    def __merge_sequences(input_sequences):
        '''Extract the proper ordering of elements from multiple sequences'''
        # remove slicing
        sequences = [[y.split('[')[0] for y in x] for x in input_sequences]
        values = sequences[0]
        for idx in range(len(sequences) - 1):
            values = merge_lists(values, sequences[idx + 1])
        values = OrderedDict([(x, [-9]) for x in values])
        return values

    def regularize_ensemble(self):
        '''
        For definitions such as:
        ```
        preprocess: method1 * method2
        analyze: preprocess * (method3, method4)
        ```
        we will need to convert `analyze` into:
        analyze: method1 * method2 * (method3, method4)

        we also should handle exceptions here such that after this step,
        everything on the rhs should be whatever we've already have defined
        (but we can check this eventually after sequences have been generated)
        '''
        if 'define' not in self.content:
            return
        replace_list = []
        for lhs, rhs in self.content['define'].items():
            rhs = f"({', '.join(rhs)})"
            for item in reversed(replace_list):
                rhs =  re.sub(r"\b%s\b" % item[0], item[1], rhs)
            self.content['define'][lhs] = rhs
            replace_list.append((lhs, rhs))

    def expand_ensemble(self, value):
        '''
        input
        =====
        define:
            preprocess: filter * (norm1, norm2)
        run: data * preprocess * analyze

        where `define` is in self.content['define']
        `run` is in value

        output
        ======
        data * (filter * (norm1, norm2)) * analyze
        '''
        if 'define' not in self.content:
            return value
        for lhs, rhs in self.content["define"].items():
            if not '*' in rhs:
                # is a valid group
                # that is, only exists alternating modules not concatenate modules
                self.groups[lhs] = rhs.replace(',','').replace(')','').replace('(','').split()
            else:
                self.concats[lhs] = rhs.replace(',','').replace(')','').replace('(','').replace('*').split()
            # http://www.regular-expressions.info/wordboundaries.html
            value = re.sub(r"\b%s\b" % lhs, rhs, value)
        return value

    def check_looped_computation(self):
        # check duplicate modules in the same sequence
        for seq in self.sequence:
            if len(set(seq)) != len(seq):
                raise ValueError(f'Duplicated module found in DSC sequence ``{seq}``. '\
                                 'Iteratively executing modules is not yet supported.')

    # def consolidate_sequences(self):
    #     '''
    #     FIXME: not sure if still needed
    #     For trivial multiple sequences, eg, "step1 * step2[1], step1 * step[2]", should be consolidated to one
    #     This cannot be done with symbolic math logic so we have to do it here
    #     '''
    #     sequences = OrderedDict()
    #     for sequence, idx in self.sequence:
    #         if sequence not in sequences:
    #             sequences[sequence] = idx
    #         else:
    #             for item in idx:
    #                 if item not in sequences[sequence]:
    #                     sequences[sequence].append(item)
    #     self.sequence = [[k, sorted(value)] for k, value in sequences.items()]

    def __str__(self):
        return dict2str(strip_dict(OrderedDict([('sequences to execute', self.sequence),
                                                ('sequence ordering', list(self.sequence_ordering.keys())),
                                                ('R libraries', self.rlib), ( 'Python modules', self.pymodule)]),
                                   mapping = OrderedDict))


class DSC_Pipeline:
    '''
    Analyzes DSC contents to determine dependencies and what exactly should be executed.
    It puts together DSC modules to sequences and continue to propagate computational routines for execution
    The output will be analyzed DSC ready to be translated to pipelines for execution
    '''
    def __init__(self, script_data):
        '''
        script_data comes from DSC_Script, having members:
        * modules
        * runtime (runtime.sequence is relevant)
        * output (output data prefix)
        Because different combinations of modules will lead to different
        I/O settings particularly with plugin status, here for each
        sequence, fresh deep copies of modules will be made from input modules

        Every module in a pipeline is a plugin, whether it be Python, R or Shell.
        When output contain variables the default output file format and method to save variables are
        applied.

        This class provides a member called `pipelines` which contains multiple pipelines
        '''
        self.pipelines = []
        for sequence in script_data.runtime.sequence:
            self.add_pipeline(sequence, script_data.modules, list(script_data.runtime.sequence_ordering.keys()))

    def add_pipeline(self, sequence, data, ordering):
        pipeline = OrderedDict()
        for name in sequence:
            module = copy.deepcopy(data[name])
            file_dependencies = []
            for k, p in list(module.p.items()):
                for p1_idx, p1 in enumerate(p):
                    if isinstance(p1, str):
                        if p1.startswith('$'):
                            id_dependent = self.find_dependent(p1[1:], list(pipeline.values()),
                                                               module.name)
                            if id_dependent[1] not in module.depends:
                                module.depends.append(id_dependent[1])
                            if id_dependent[1][2] == 'var':
                                module.plugin.add_input(k, p1)
                            else:
                                # FIXME: should figure out the index of previous output
                                file_dependencies.append((id_dependent[0], k))
                            # FIXME: should not delete, but rather transform it, when this
                            # can be properly bypassed on scripts
                            # module.p[k][p1_idx] = repr(p1)
                            module.p[k].pop(p1_idx)
                if len(module.p[k]) == 0:
                    del module.p[k]
            module.depends.sort(key = lambda x: ordering.index(x[0]))
            if len(file_dependencies):
                file_dependencies.sort()
                module.plugin.add_input([x[1] for x in file_dependencies], '${_input:r}')
            pipeline[module.name] = module
        # FIXME: ensure this does not happen
        # Otherwise will have to bring this back
        # self.check_duplicate_step(pipeline)
        self.pipelines.append(pipeline)

    @staticmethod
    def find_dependent(variable, pipeline, module_name):
        curr_idx = len(pipeline)
        if curr_idx == 0:
            raise FormatError('Pipeline variable ``$`` is not allowed in the input of the first module of a DSC sequence.')
        curr_idx = curr_idx - 1
        dependent = None
        while curr_idx >= 0:
            # Look up backwards for the corresponding block, looking at the output of the first step
            if variable in [x for x in pipeline[curr_idx].rv]:
                dependent = (pipeline[curr_idx].name, variable, 'var')
            if variable in [x for x in pipeline[curr_idx].rf]:
                if dependent is not None:
                    raise ValueError(f'[BUG]: ``{variable}`` cannot be both a variable and a file!')
                dependent = (pipeline[curr_idx].name, variable, 'file')
            if dependent is not None:
                break
            else:
                curr_idx = curr_idx - 1
        if dependent is None:
            raise FormatError(f'Cannot find output variable for ``${variable}`` in any of its upstream modules.'\
                              f' This variable is required by module ``{module_name}``.')
        return curr_idx, dependent

    # def consolidate_pipelines(self):
    #     '''
          # FIXME: is there a need for it now?
    #     For trivial multiple pipelines, eg, "step1 * step2[1], step1 * step[2]", should be consolidated to one
    #     This cannot be done with symbolic math logic so we have to do it here

    #     First we compare each pipeline (a list of OrderedDict) and get rid of duplicate
    #     Second ... is there a second?
    #     '''
    #     import hashlib
    #     import pickle
    #     def get_md5(data):
    #         return hashlib.md5(pickle.dumps(data)).hexdigest()
    #     pipelines = []
    #     ids = []
    #     for pipeline in self.pipelines:
    #         md5 = get_md5(pipeline)
    #         if md5 not in ids:
    #             ids.append(md5)
    #             pipelines.append(pipeline)
    #     self.pipelines = pipelines


    def __str__(self):
        res = ''
        for idx, modules in enumerate(self.pipelines):
            res += f'# Pipeline {idx + 1}\n'
            res += f'## Modules\n' + '\n'.join(['### {x}\n```yaml\n{y}\n```\n' for x, y in modules.items()])
        return res
