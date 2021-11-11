# Skript Erkennung
# Konstanten
import re

skript_input = './test_script.py'

tab = '    '
func = False
func_ind = 0
functions = {}
constants = []

with open(skript_input) as skript:
    skript_read = skript.readlines()
    for ind, line in enumerate(skript_read):
        if '=' in line and line[line.find('=')+1] != '=':
            constants.append((ind, line))
        if 'def' in line:
            func = True
            func_ind += 1
            functions[func_ind] = [line]
        elif func and '    ' in line:
            functions[func_ind].append(line)
        elif func and '    ' not in line:
            func = False
        skript_read[ind] = line.replace('print', 'print_to_gui')


def find_nth(string, substring, n):
   if (n == 1):
       return string.find(substring)
   else:
       return string.find(substring, find_nth(string, substring, n - 1) + 1)


def type_detector(x):
    try:
        xtype = str(eval(f'type({x})'))
        return xtype[xtype.find("'")+1:find_nth(xtype, "'", 2)]
    except:
        return 'str'


def assignment_filter(x):
    name = x[:x.find('=')].replace(' ', '').replace('\n', '')
    value = x[x.find('=')+1:].replace(' ', '').replace('\n', '')
    vtype = type_detector(value)
    value = eval(f'{vtype}({value})')
    return name, value, vtype


def remover(l):
    for ind, x in enumerate(l):
        try:
            vtype = assignment_filter(x[1])[2]
            if vtype not in ['int', 'float', 'str']:
                l.remove(x)
                return True
        except:
            l.remove(x)
            return True
    return False


false_element = True
while false_element:
    false_element = remover(constants)
for ind, x in enumerate(constants):
    constants[ind] = (x[0], *assignment_filter(x[1]))

print(functions)
print(constants)

print(skript_read)



