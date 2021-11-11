# start
import re


def build_function(f_list):
    f_string = ""
    for line in f_list:
        f_string += line
    function = {}
    exec(f_string, function)
    return function[list(function.keys())[1]], list(function.keys())[1]


def count_leading_s(s):
    value = re.findall(r"^\s+",s)
    c=0
    if value:
        c = value[0].count(r" ")
    return c


def read_further(current_function, lines, index, leading_t):
    while index < len(lines) and count_leading_s(lines[index]) > leading_t:
        current_function.append(lines.pop(index))


def find_nth(string, substring, n):
    if (n == 1):
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
        return name, value

    out_d = {}
    for i in l:
        try:
            name, value = _assignment_filter(i[1])
        except:
            pass
        out_d[name] = value
    return out_d


def sum_lines_up(i, lines):
    block = []
    n_tabs = count_leading_s(lines[i])
    block.append(lines.pop(i))
    read_further(block, lines, i, n_tabs)
    return block


path = './test_script.py'

with open(path) as f:
    lines = f.readlines()

function_list = []
function_index_list = []
constants = []
main = []
i = 0

while i < len(lines):
    if "def" in lines[i]:
        current_function = sum_lines_up(i, lines)
        function_list.append(current_function)
        function_index_list.append(i)
    if '=' in lines[i] and lines[i][lines[i].find('=') + 1] != '=':
        constants.append((i, lines[i]))
    lines[i] = lines[i].replace('print', 'print_to_gui')
    i += 1

#TODO: hier umschreiben der konstanten einfügen

i = 0
while i < len(lines):
    if '__main__' in lines[i]:
        main = sum_lines_up(i, lines)
    i += 1

functions = {}
f, key = build_function(function_list[0])
functions[key] = f
constants = constant_reader(constants)

print(function_list)
print(constants)
print(main)
print(f(constants['CONSTANT1'], constants['CONSTANT3']))

