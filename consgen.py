from lark import Lark, Transformer
import argparse
from jinja2 import Environment, FileSystemLoader

parser = Lark('''
	?start: (sigdesc)+
	sigdesc: "connect" IDENTIFIER "with" IDENTIFIER _NEWLINE
	WHITESPACE: " " | "\\t"
	IDENTIFIER: /[A-Z_a-z]([A-Za-z0-9_])*(\\[[0-9]+\\])?/
	COMMENT: "#" /[^\\n]*/ _NEWLINE
	_NEWLINE: /[\\n]+/
	%ignore WHITESPACE
	%ignore COMMENT
	
	''')

cmdparser = argparse.ArgumentParser(description='This is a Verilog FSM Code Generator')
cmdparser.add_argument('file', help='Filename')
args = cmdparser.parse_args()

filename = args.file
with open(filename) as fl:
    fls = fl.read()
fls = fls + "\n"  # Adding a newline to prevent parsing error
tree = parser.parse(fls)


class FSMTransfomer(Transformer):
    def start(self, matches):
        dct = {}
        for match in matches:
            dct[match[0]] = match[1]
        return dct

    def sigdesc(self, matches):
        return matches


# print(tree)
res = FSMTransfomer().transform(tree)
print(res)


def getifthere(dct, property, default=None):
    return dct[property] if property in dct else default


def binsizer(n):
    return len(bin(n)[2:])


env = Environment(loader=FileSystemLoader('./jtemplates/', followlinks=True))
template_constraint = env.get_template('constraint')


def file_dump(flname, content):
    with open(flname, 'w') as fl:
        fl.write(content)

def formtarget(s):
    if ("[" in s):
        return "{" + s + "}"
    else:
        return s

defination_dict = {"LED0":"U16","LED1":"E19","LED2":"U19","LED3":"V19","LED4":"W18","LED5":"U15","LED6":"U14","LED7":"V14","LED8":"V13","LED9":"V3","LED10":"W3","LED11":"U3","LED12":"P3","LED13":"N3","LED14":"P1","LED15":"L1","MIDDLE_BUTTON":"U18","DOWN_BUTTON":"U17","LEFT_BUTTON":"W19","RIGHT_BUTTON":"T17","UP_BUTTON":"T18"}
def make_constraints(res):
    s = ""
    for i in res:
       s = s + template_constraint.render(target = formtarget(defination_dict[res[i]]),signame = i) 
    file_dump(s)

make_constrains(res)