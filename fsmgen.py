from lark import Lark, Transformer
import argparse
from jinja2 import Environment, FileSystemLoader

parser = Lark('''
	?start: (block)+
	block: machined
		| inputsize 
		| statedesc
		| statedescmealy 
		| transdesc 
		| transdescmealey
		| name
		| startstate
		| encode_type
	startstate: "START:"i IDENTIFIER _NEWLINE
	name: "NAME:"i IDENTIFIER _NEWLINE
	encodetype: "ENCODING:"i (BIN|GRAY|OHOT|OCOLD) _NEWLINE
	BIN: "BINARY"i
	GRAY: "GRAY"i
	OHOT: "ONEHOT"i
	OCOLD: "ONECOLD"i
	machined: "MACHINE_TYPE:"i (MOORE | MEALEY) _NEWLINE
	MOORE: "MOORE"i
	MEALEY: "MEALY"i
	WHITESPACE: " " | "\\t"
	IDENTIFIER: /[A-Z_a-z]([A-Za-z0-9_])*/
	COMMENT: "#" /[^\\n]*/ _NEWLINE
	_NEWLINE: /[\\n]+/
	%ignore WHITESPACE
	%ignore COMMENT
	statedesc: "STATE_DESC:"i _NEWLINE (state)+
	statedescmealy: "STATE_DESC:"i _NEWLINE (statemealy)+
	statemealy: IDENTIFIER _NEWLINE
	state: IDENTIFIER " gives " NUMBER _NEWLINE
	NUMBER: /[0-9]+/
	inputsize: "INPUT_SIZE:"i NUMBER _NEWLINE
	transdescmealey: "TRANSITION:"i _NEWLINE (transmealey)+
	transmealey: IDENTIFIER " to " IDENTIFIER " on "i NUMBER " gives "i NUMBER _NEWLINE
	transdesc: "TRANSITION:"i _NEWLINE (trans)+
	trans: IDENTIFIER " to " IDENTIFIER " on "i NUMBER _NEWLINE
	
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

    def name(self, match):
        return ('Name', str(match[0]))

    def startstate(self, match):
        return ('Start', str(match[0]))

    def machined(self, match):
        return ("Type", str(match[0]).upper())

    def encodetype(self, match):
        return ('Encoding', str(match[0]).upper())

    def block(self, match):
        return match[0]

    def statedesc(self, matches):
        dct = {}
        for match in matches:
            dct[match[0]] = match[1]
        return ('States', dct)

    def state(self, match):
        return [str(match[0]), int(match[1])]

    def statemealy(self, match):
        return str(match[0])

    def statedescmealy(self, matches):
        dct = []
        for match in matches:
            dct.append(match)
        return ('States', dct)

    def inputsize(self, match):
        return ('Isize', int(match[0]))

    def transdesc(self, matches):
        dct = {}
        for match in matches:
            if match[0] not in dct:
                dct[match[0]] = {}
            dct[match[0]][match[2]] = match[1]
        return ('Transition', dct)

    def trans(self, match):
        return [str(match[0]), str(match[1]), int(match[2])]

    def transdescmealey(self, matches):
        dct = {}
        for match in matches:
            if match[0] not in dct:
                dct[match[0]] = {}
            dct[match[0]][match[2]] = [match[1], match[3]]
        return 'Transition', dct

    def transmealey(self, match):
        return [str(match[0]), str(match[1]), int(match[2]), int(match[3])]


# print(tree)
res = FSMTransfomer().transform(tree)
print(res)


def getifthere(dct, property, default=None):
    return dct[property] if property in dct else default


def binsizer(n):
    return len(bin(n)[2:])


env = Environment(loader=FileSystemLoader('./jtemplates/', followlinks=True))
template_always = env.get_template('always')
template_module = env.get_template('module')
template_case = env.get_template('case')
template_caseinput = env.get_template('caseinput')
template_caseinput_mealy = env.get_template('caseinputmealy')


def file_dump(flname, content):
    with open(flname, 'w') as fl:
        fl.write(content)


def binarytoGray(binary):
    gray = ""
    gray += binary[0]
    for i in range(1, len(binary)):
        gray += str(int(binary[i - 1]) ^ int(binary[i]))
    return gray


def encode(encodi, state_num, nstates):
    encodi = encodi.lower()
    sbi = bin(nstates)[2:]
    bi = bin(state_num)[2:]
    if encodi == 'binary':
        return str(len(sbi)) + "'b" + '0' * (len(sbi) - len(bi)) + bi
    elif encodi == 'gray':
        gi = binarytoGray(bi)
        return str(len(sbi)) + "'b" + '0' * (len(sbi) - len(gi)) + gi
    elif encodi == 'onehot':
        oi = '0' * nstates
        return str(nstates) + "'b" + oi[:nstates - state_num] + '1' + oi[nstates - state_num + 1:]
    elif encodi == 'onecold':
        oi = '1' * nstates
        return str(nstates) + "'b" + oi[:nstates - state_num] + '0' + oi[nstates - state_num + 1:]
    else:
        return


def makeMoore(modname, inp_size, state_output, states, transition_matrix, start, enc):
    parlist = []
    startname = ''
    numstates = len(states)
    # creating parameter list for state encoding
    for i in range(numstates):
        parlist.append((states[i], encode(enc,i,numstates)))
        if states[i] == start:
            parlist.append((states[i] + '_start', i))
            startname = states[i] + '_start'
    max_out = 0
    for i in state_output:
        max_out = max(max_out, state_output[i])
    # print(max_out)
    signallist = ['w', 'clk', 'reset', 'O']
    # signal definations
    sigparams = []
    sigparams.append(('input', ('' if binsizer(inp_size) == 1 else '[' + str(binsizer(inp_size) - 1) + ':0]') + 'w'))
    sigparams.append(('output reg', ('' if binsizer(max_out) == 1 else '[' + str(binsizer(max_out) - 1) + ':0]') + 'O'))
    sigparams.append(('input', 'clk'))
    sigparams.append(('input', 'reset'))
    sigparams.append(
        ('reg', ('' if binsizer(len(states) - 1) == 1 else '[' + str(binsizer(len(states) - 1)) + ':0]') + 'state'))
    sigparams.append(('reg', (
        '' if binsizer(len(states) - 1) == 1 else '[' + str(binsizer(len(states) - 1)) + ':0]') + 'next_state'))
    clockblockcode = '''
		if(reset==1)
			state <= {st};
		else
			state <= next_state;
	'''.format(st=startname)
    clockblockfinal = template_always.render(sensetivity='posedge clk,posedge reset', code=clockblockcode)
    # print(clockblockfinal)
    stateblockmatrix = []
    for i in states:
        stateinputs = transition_matrix[i]
        tci = template_caseinput.render(sig='w', next='next_state',
                                        matrix=list(stateinputs.items()) + [('default', 'state')])
        stateblockmatrix.append((i, tci))
    # print(stateblockmatrix)
    caseblock = template_case.render(sig='state', matrix=stateblockmatrix, defleft='next_state', defright='state')
    # print(caseblock)
    alwaystransition = template_always.render(sensetivity='state,w', code=caseblock)
    # print(alwaystransition)
    output_case = template_caseinput.render(sig='state', next='O',
                                            matrix=list(state_output.items()) + [('default', 'O')])
    output_block = template_always.render(sensetivity='state', code=output_case)
    module = template_module.render(modulename=modname, signals=','.join(signallist), siglist=sigparams,
                                    paralist=parlist, blocks=[clockblockfinal, alwaystransition, output_block])
    file_dump(modname + '.v', module)


def makeMealy(modname, inp_size, transition_matrix, start, enc):
    parlist = []
    startname = ''
    states = list(transition_matrix.keys())
    numstates = len(states)
    # creating parameter list for state encoding
    for i in range(numstates):
        parlist.append((states[i], encode(enc,i,numstates)))
        if states[i] == start:
            parlist.append((states[i] + '_start', i))
            startname = states[i] + '_start'
    max_out = 0
    for i in states:
        val = 0
        for j in transition_matrix[i]:
            val = max(val, transition_matrix[i][j][1])
        max_out = max(max_out, val)
    # print(max_out)
    signallist = ['w', 'clk', 'reset', 'O']
    # signal definitions
    sigparams = []
    sigparams.append(('input', ('' if binsizer(inp_size) == 1 else '[' + str(binsizer(inp_size) - 1) + ':0]') + 'w'))
    sigparams.append(('output reg', ('' if binsizer(max_out) == 1 else '[' + str(binsizer(max_out) - 1) + ':0]') + 'O'))
    sigparams.append(('input', 'clk'))
    sigparams.append(('input', 'reset'))
    sigparams.append(('reg', ('' if binsizer(len(transition_matrix) - 1) == 1 else '[' + str(
        binsizer(len(transition_matrix) - 1) - 1) + ':0]') + 'state'))
    sigparams.append(('reg', ('' if binsizer(len(transition_matrix) - 1) == 1 else '[' + str(
        binsizer(len(transition_matrix) - 1) - 1) + ':0]') + 'next_state'))
    sigparams.append(
        ('reg', ('' if binsizer((max_out) - 1) == 1 else '[' + str(binsizer(max_out) - 1) + ':0]') + 'next_O'))
    clockblockcode = '''
	if(reset==1) begin
		state <= {st};
        O <= 0;
        O
    end
	else begin
		state <= next_state;
        O <= next_O;
    end
	'''.format(st=startname)
    clockblockfinal = template_always.render(sensetivity='posedge clk,posedge reset', code=clockblockcode)
    # print(clockblockfinal)
    stateblockmatrix = []
    for i in states:
        stateinputs = transition_matrix[i]
        tci = template_caseinput_mealy.render(sig='w', next='next_state', next_out='next_O',
                                              matrix=list(stateinputs.items()) + [('default', ['state', 'O'])])
        stateblockmatrix.append((i, tci))
    # print(stateblockmatrix)
    caseblock = template_case.render(sig='state', matrix=stateblockmatrix, defleft='next_state', defright='state')
    # print(caseblock)
    alwaystransition = template_always.render(sensetivity='state,w', code=caseblock)
    # print(alwaystransition)
    module = template_module.render(modulename=modname, signals=','.join(signallist), siglist=sigparams,
                                    paralist=parlist, blocks=[clockblockfinal, alwaystransition])
    file_dump(modname + '.v', module)


def makeFSM(**params):
    modname = getifthere(params, 'Name', 'FSMmodule')
    # print(modname)
    typ = getifthere(params, 'Type', 'MOORE')
    enc = getifthere(params, 'Encoding', 'BINARY')
    if typ == "MOORE":
        inp_size = getifthere(params, 'Isize', 8)
        state_output = params['States']
        states = [i for i in state_output.keys()]
        transition_matrix = params['Transition']
        start = getifthere(params, 'Start', states[0])
        makeMoore(modname, inp_size, state_output, states, transition_matrix, start, enc)
    else:
        inp_size = getifthere(params, 'Isize', 8)
        transition_matrix = params['Transition']
        start = getifthere(params, 'Start', list(transition_matrix.keys())[0])
        makeMealy(modname, inp_size, transition_matrix, start, enc)


makeFSM(**res)
