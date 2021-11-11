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
    while count_leading_s(lines[index])> leading_t and index <= len(lines):
        current_function.append(lines.pop(index))
    return index


path = r"C:\Users\acecross\PycharmProjects\GUImaker\test_script.py"

with open(path) as f:
    lines = f.readlines()

function_list = []
i=0
function_index_list = []
while i < len(lines):
    if "def" in lines[i]:
        current_function = []
        n_tabs = count_leading_s(lines[i])
        current_function.append(lines.pop(i))
        i = read_further(current_function, lines, i, n_tabs)
        function_list.append(current_function)
        function_index_list.append(i)
    i += 1
functions = {}
f,key = build_function(function_list[0])
functions[key] = f
print(f(2,3))

