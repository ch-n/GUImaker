# start
import re


def sum_code_block(l):
    code_block = ''
    for i in l:
        code_block += i
    return code_block


def build_function(f_list):
    f_string = sum_code_block(f_list)
    function = {}
    exec(f_string, function)
    return function[list(function.keys())[1]], list(function.keys())[1]


def count_leading_s(s):
    value = re.findall(r"^\s+", s)
    c=0
    if value:
        c = value[0].count(r" ")
    return c


def read_further(current_function, lines, index, leading_t):
    while index < len(lines) and count_leading_s(lines[index]) > leading_t:
        current_function.append(lines.pop(index))


def find_nth(string, substring, n):
    if n == 1:
        return string.find(substring)
    else:
        return string.find(substring, find_nth(string, substring, n - 1) + 1)


def constant_reader(l):
    def _type_detector(x):
        try:
            xtype = str(eval(f'type({x})'))
            return xtype[xtype.find("'") + 1:find_nth(xtype, "'", 2)]
        except:
            return 'str'

    def _assignment_filter(x):
        name = x[:x.find('=')].replace(' ', '').replace('\n', '')
        value = x[x.find('=') + 1:].replace(' ', '').replace('\n', '')
        vtype = _type_detector(value)
        value = eval(f'{vtype}({value})')
        return name, value, vtype

    out_d = {}
    for i in l:
        try:
            name, value, vtype = _assignment_filter(i[1])
        except:
            pass
        out_d[name] = dict(value=value, type=vtype)
    return out_d


def catch_lines(i, lines):
    line_l = []
    n_tabs = count_leading_s(lines[i])
    line_l.append(lines.pop(i))
    read_further(line_l, lines, i, n_tabs)
    return line_l


def sub_key_words(l, constant_d):
    for ind, line in enumerate(l):
        l[ind] = line.replace('print', 'print_to_gui')
        if '==' not in line:
            const = line.split('=')[0].replace(' ', '')
            if const in constant_d.keys():
                const = f'    {const} = {constant_d[const]["type"]}\n'
                l[ind] = const


path = './test_script.py'

# read script as string
with open(path) as f:
    lines = f.readlines()

# define variables
function_list = []
function_index_list = []
constants = []
main = []
i = 0

# interpret lines
while i < len(lines):
    if "def" in lines[i]:
        current_function = catch_lines(i, lines)
        function_list.append(current_function)
        function_index_list.append(i)
    if '=' in lines[i] and lines[i][lines[i].find('=') + 1] != '=':
        constants.append((i, lines[i]))
    i += 1

#TODO: hier umschreiben der konstanten einfügen

i = 0
while i < len(lines):
    if '__main__' in lines[i]:
        main = catch_lines(i, lines)
    i += 1

# parse constants
constants = constant_reader(constants)

# substitute constants
sub_key_words(main, constants)

# combine main line list to one string
main = sum_code_block(main)

functions = {}
f, key = build_function(function_list[0])
functions[key] = f

print(function_list)
print(constants)
print(main)
print(f(constants['CONSTANT1']['value'], constants['CONSTANT3']['value']))

