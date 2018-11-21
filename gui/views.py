from lark import Lark, Transformer
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from jinja2 import FileSystemLoader, Environment
from django.core.files.storage import FileSystemStorage
import subprocess

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
        | sigdesc
        | test
	startstate: "START:"i IDENTIFIER _NEWLINE
	name: "NAME:"i IDENTIFIER _NEWLINE
	encode_type: "ENCODING:"i (BIN|GRAY|OHOT|OCOLD) _NEWLINE
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
    IDENTIFIER1: /[A-Z_a-z]([A-Za-z0-9_])*(\\[[0-9]+\\])?/
    sigdesc: "CONSTRAINTS:"i _NEWLINE (sig)+
    sig: "connect" IDENTIFIER1 "with" IDENTIFIER1 _NEWLINE
    IDENTIFIER2: /[0-1]+/
    test: "TESTBENCH:"i _NEWLINE (testing)+ _NEWLINE
    testing: IDENTIFIER2
	
	''')

parser1 = Lark('''
	?start: (sigdesc)+
	sigdesc: "connect" IDENTIFIER "with" IDENTIFIER _NEWLINE
	WHITESPACE: " " | "\\t"
	IDENTIFIER: /[A-Z_a-z]([A-Za-z0-9_])*(\\[[0-9]+\\])?/
	COMMENT: "#" /[^\\n]*/ _NEWLINE
	_NEWLINE: /[\\r\\n]+/
	%ignore WHITESPACE
	%ignore COMMENT

	''')

env = Environment(
    loader=FileSystemLoader('./gui/templates/jtemplates/',
                            followlinks=True))
template_always = env.get_template('always')
template_module = env.get_template('module')
template_case = env.get_template('case')
template_caseinput = env.get_template('caseinput')
template_caseinput_mealy = env.get_template('caseinputmealy')
template_fileinput = env.get_template('input_file')
template_constraint = env.get_template('constraints')
template_build = env.get_template('build')

defination_dict = {"LED0": "U16", "LED1": "E19", "LED2": "U19", "LED3": "V19", "LED4": "W18", "LED5": "U15",
                   "LED6": "U14", "LED7": "V14", "LED8": "V13", "LED9": "V3", "LED10": "W3", "LED11": "U3",
                   "LED12": "P3", "LED13": "N3", "LED14": "P1", "LED15": "L1", "MIDDLE_BUTTON": "U18",
                   "DOWN_BUTTON": "U17", "LEFT_BUTTON": "W19", "RIGHT_BUTTON": "T17", "UP_BUTTON": "T18",
                   "SWITCH0": "V17", "SWITCH1": "V16", "SWITCH2": "W16", "SWITCH3": "W17", "SWITCH4": "W15",
                   "SWITCH5": "V15", "SWITCH6": "W14", "SWITCH7": "W13", "SWITCH8": "V2", "SWITCH9": "T3",
                   "SWITCH10": "T2", "SWITCH11": "R3", "SWITCH12": "W2", "SWITCH13": "U1", "SWITCH14": "T1",
                   "SWITCH15": "R2"}


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

    def encode_type(self, match):
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

    def sigdesc(self, matches):
        dct = {}
        for match in matches:
            dct[match[0]] = match[1]
        return 'Constraints', dct

    def sig(self, match):
        return [str(match[0]), str(match[1])]

    def testing(self, match):
        return str(match[0])

    def test(self, matches):
        dct = ''
        for match in matches:
            dct += match + ' '
        return 'Testing', dct


class FSMTransfomer1(Transformer):
    def start(self, matches):
        dct = {}
        for match in matches:
            dct[match[0]] = match[1]
        return dct

    def sigdesc(self, matches):
        return str(matches[0]), str(matches[1])


def getifthere(dct, property, default=None):
    return dct[property] if property in dct else default


def binarytoGray(binary):
    gray = ""
    gray += binary[0]
    for i in range(1, len(binary)):
        gray += str(int(binary[i - 1]) ^ int(binary[i]))
    return gray


def formtarget(s):
    if ("[" in s):
        print(1)
        return "{" + s + "}"
    else:
        print(2)
        return s


def encode(encodi, state_num, nstates):
    encodi = encodi.lower()
    sbi = bin(nstates - 1)[2:]
    bi = bin(state_num)[2:]
    if encodi == 'binary':
        return str(len(sbi)) + "'b" + '0' * (len(sbi) - len(bi)) + bi
    elif encodi == 'gray':
        gi = binarytoGray(bi)
        return str(len(sbi)) + "'b" + '0' * (len(sbi) - len(gi)) + gi
    elif encodi == 'onehot':
        oi = list('0' * (nstates - 1))
        oi.insert(nstates - state_num - 1, '1')
        ois = ''.join(oi)
        return str(nstates) + "'b" + ois
    elif encodi == 'onecold':
        oi = list('1' * (nstates - 1))
        oi.insert(nstates - state_num - 1, '0')
        ois = ''.join(oi)
        return str(nstates) + "'b" + ois
    else:
        return


def binsizer(n):
    return len(bin(n)[2:])


def file_dump(flname, content):
    with open('files/' + flname, 'w') as fl:
        fl.write(content)


def makeMoore(modname, inp_size, state_output, states, transition_matrix, start, enc):
    parlist = []
    startname = ''
    numstates = len(states)
    # creating parameter list for state encoding
    for i in range(numstates):
        parlist.append((states[i], encode(enc, i, numstates)))
        if states[i] == start:
            startname = states[i]
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
    if enc not in {'ONEHOT', 'ONECOLD'}:
        sigparams.append(
            ('reg',
             ('' if binsizer(len(states) - 1) == 1 else '[' + str(binsizer(len(states) - 1) - 1) + ':0]') + 'state'))
        sigparams.append(('reg', (
            '' if binsizer(len(states) - 1) == 1 else '[' + str(binsizer(len(states) - 1) - 1) + ':0]') + 'next_state'))
    else:
        sigparams.append(
            ('reg', ('' if numstates == 1 else '[' + str(numstates - 1) + ':0]') + 'state'))
        sigparams.append(('reg', (
            '' if numstates == 1 else '[' + str(numstates - 1) + ':0]') + 'next_state'))
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


def makeMealy(modname, inp_size, states, transition_matrix, start, enc):
    parlist = []
    startname = ''
    numstates = len(states)
    # creating parameter list for state encoding
    for i in range(numstates):
        parlist.append((states[i], encode(enc, i, numstates)))
        if states[i] == start:
            startname = states[i]
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
    if enc not in {'ONEHOT', 'ONECOLD'}:
        sigparams.append(('reg', ('' if binsizer(numstates - 1) == 1 else '[' + str(
            binsizer(numstates - 1) - 1) + ':0]') + 'state'))
        sigparams.append(('reg', ('' if binsizer(numstates - 1) == 1 else '[' + str(
            binsizer(numstates - 1) - 1) + ':0]') + 'next_state'))
    else:
        sigparams.append(
            ('reg', ('' if numstates == 1 else '[' + str(numstates - 1) + ':0]') + 'state'))
        sigparams.append(('reg', (
            '' if numstates == 1 else '[' + str(numstates - 1) + ':0]') + 'next_state'))
    sigparams.append(
        ('reg', ('' if binsizer((max_out) - 1) == 1 else '[' + str(binsizer(max_out) - 1) + ':0]') + 'next_O'))
    clockblockcode = '''
	if(reset==1) begin
		state <= {st};
        O <= 0;
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


def makeFSM_gui(params):
    modname = params['modname']
    typ = params['type']
    enc = params['enc']
    inp_size = params['inp_size']
    state_output = params['States']
    states = [i for i in state_output]
    transition_matrix = params['Transition']
    start = params['start_state']
    if typ == "Moore":
        makeMoore(modname, inp_size, state_output, states, transition_matrix, start, enc)
    else:
        makeMealy(modname, inp_size, states, transition_matrix, start, enc)


def makeFSM_file(**params):
    # print(params)
    modname = getifthere(params, 'Name', 'FSMmodule')
    typ = getifthere(params, 'Type', 'MOORE')
    enc = getifthere(params, 'Encoding', 'BINARY')
    constraint = getifthere(params, 'Constraints')
    test_in = getifthere(params, 'Testing')
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
        states = params['States']
        start = getifthere(params, 'Start', list(transition_matrix.keys())[0])
        makeMealy(modname, inp_size, states, transition_matrix, start, enc)
    if test_in:
        testbench(modname, test_in, inp_size)
    if constraint:
        make_constraints(constraint, modname)
        cons = "constraints_" + modname
        build = template_build.render(modname=modname, constraints=cons)
        file_dump("build.tcl", build)
        print('Build running')
        s = subprocess.call(["vivado", "-mode", "batch", "-source", "./files/build.tcl"], shell=True)
        print('Command run')


def make_constraints(res, name):
    s = ""
    s += r"""set_property CLOCK_DEDICATED_ROUTE FALSE [get_nets clk_IBUF]
"""
    for i in res:
        s = s + template_constraint.render(target=defination_dict[res[i]], signame=formtarget(i))
    s += r"""
set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]
set_property BITSTREAM.CONFIG.CONFIGRATE 33 [current_design]
set_property CONFIG_MODE SPIx4 [current_design]
    """
    print(s)
    file_dump('constraints_' + name + '.xdc', s)


def testbench(modname, testin, inpsize):
    code = ''
    code += "`timescale 1ns/1ps\n"
    code += "module tb_" + str(modname) + "();\n"
    code += "reg w,clk,reset;\n"
    code += "wire O;\n"
    code += modname + " m1(w,clk,reset,O);\n"
    code += "initial\n"
    code += "begin\n"
    code += "reset=1;w=0;\n#1 clk=0;\n"
    code += "#9 reset=0;\n"
    code += '''$monitor($time, , ,"clk=%b",clk,,"O=%b",O,,"reset=%b",reset,,"w=%b",w);\n'''
    le = len(testin)
    length = le // (inpsize)
    lis = testin.split()
    for i in lis:
        if len(i) == inpsize:
            code += "#10 w=" + str(inpsize) + '\'b' + i + ";\n"
        elif len(i) > inpsize:
            code += "#10 w=" + str(inpsize) + '\'b' + i[:inpsize] + ";\n"
        else:
            code += "#10 w=" + str(inpsize) + '\'b' + '0' * (inpsize - len(i)) + i + ";\n"
    code += "end\n"
    code += "always\n"
    code += "#5 clk=~clk;\n"
    code += "initial\n"
    code += "#100 $finish ;\n"
    code += "endmodule\n"
    file_dump("tb_" + modname + '.v', code)


def index(request):
    return render(request, 'template_gui/gui.html', {})


@csrf_exempt
def seq_det(request):
    name = request.POST.get("name")
    if name == '':
        name = 'FSMmodule'
    type = request.POST.get("type")
    inp = request.POST.get("input")
    seq_type = request.POST.get("seq_type")
    enc = request.POST.get("enc")
    tb = request.POST.get("tb")
    inp_size = 1
    if type == 'moore':
        d = {}
        le = len(inp)
        for i in range(le + 1):
            st = 's' + str(i)
            d[st] = {}
        for i in range(le):
            st = 's' + str(i)
            d[st][a[i]] = 's' + str(i + 1)
            sn = inp[:i] + '0' if inp[i] == '1' else inp[:i] + '1'
            for j in range(i + 1):
                if inp[:i + 1 - j] == sn[j - i - 1:]:
                    l = i + 1 - j
                    break
            else:
                l = 0
            d[st][sn[-1]] = 's' + str(l)
        if seq_type == 'nonov':
            d['s' + str(le)] = d['s0']
        else:
            for i in range(le):
                stri0 = inp[i + 1:] + '0'
                if stri0 == inp[:le - i]:
                    d['s' + str(le)]['0'] = 's' + str(le - i)
                    break
            else:
                d['s' + str(le)]['0'] = 's0'
            for i in range(le):
                stri1 = inp[i + 1:] + '1'
                if stri1 == inp[:le - i]:
                    d['s' + str(le)]['1'] = 's' + str(le - i)
                    break
            else:
                d['s' + str(le)]['1'] = 's0'
        sd = {}
        for i in range(le):
            sd['s' + str(i)] = 0
        sd['s' + str(le)] = 1
        state_output = sd
        states = list(state_output.keys())
        start = states[0]
        transition_matrix = d
        makeMoore(name, inp_size, state_output, states, transition_matrix, start, enc)
    else:
        le = len(inp)
        d = {}
        for i in range(le):
            d['s' + str(i)] = {}
        for i in range(le - 1):
            d['s' + str(i)][inp[i]] = ['s' + str(i + 1), 0]
        for i in range(le - 1):
            sn = inp[:i] + '0' if inp[i] == '1' else inp[:i] + '1'
            for j in range(i + 1):
                if inp[:i + 1 - j] == sn[j - i - 1:]:
                    l = i + 1 - j
                    break
            else:
                l = 0
            d['s' + str(i)][sn[-1]] = ['s' + str(l), 0]
        st = inp[:-1] + str(0 if int(inp[-1]) else 1)
        li = 0
        for i in range(le):
            if st[i:] == inp[:le - i]:
                li = le - i
                break
        d['s' + str(le - 1)][st[-1]] = ['s' + str(li), 0]
        if type == 'nonov':
            d['s' + str(le - 1)][a[-1]] = ['s0', 1]
        else:
            lr = 0
            for i in range(1, le):
                if inp[i:] == inp[:le - i]:
                    lr = le - i
                    break
            d['s' + str(le - 1)][inp[-1]] = ['s' + str(lr), 1]
        states = list(d.keys())
        transition_matrix = d
        start = states[0]
        makeMealy(name, inp_size, states, transition_matrix, start, enc)
    if tb != '':
        testbench(name, tb, inp_size)
    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def file_upload(request):
    myfile = request.FILES['file']
    # print(myfile, type(myfile))
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    # print(uploaded_file_url)
    with open(uploaded_file_url[1:]) as fl:
        fls = fl.read()
    fls = fls + "\n"  # Adding a newline to prevent parsing error
    tree = parser.parse(fls)
    res = FSMTransfomer().transform(tree)
    print(res)
    makeFSM_file(**res)
    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def submit(request):
    type = request.POST.get('type')
    if (type == 'Moore'):
        name = request.POST.get('name')
        if name == '':
            name = 'FSMmodule'
        input_size = request.POST.get('input_size')
        if input_size == '':
            input_size = 8
        else:
            input_size = int(input_size)
        encoding = request.POST.get('encoding')
        i = 0
        states = {}
        while True:
            s = 'state_name' + str(i)
            so = 'state_output' + str(i)
            state_name = request.POST.get(s)
            state_output = request.POST.get(so)
            if state_name == None or state_output == None:
                break
            states[state_name] = int(state_output)
            i += 1
        start = request.POST.get('start')
        if start == '':
            start = list(states.keys())[0]
        transition = {}
        i = 0
        while True:
            s = 'state' + str(i)
            ns = 'next_state' + str(i)
            inp = 'input' + str(i)
            state = request.POST.get(s)
            next_state = request.POST.get(ns)
            inputi = request.POST.get(inp)
            if state == None or next_state == None or inputi == None:
                break
            if state not in transition:
                transition[state] = {}
            transition[state][inputi] = next_state
            i += 1
    else:
        name = request.POST.get('mname')
        if name == '':
            name = 'FSMmodule'
        input_size = request.POST.get('minput_size')
        if input_size == '':
            input_size = 8
        else:
            input_size = int(input_size)
        encoding = request.POST.get('mencoding')
        i = 0
        states = []
        while True:
            s = 'mstate_name' + str(i)
            state_name = request.POST.get(s)
            if state_name == None:
                break
            states.append(state_name)
            i += 1
        start = request.POST.get('mstart')
        if start == '':
            start = states[0]
        transition = {}
        i = 0
        while True:
            s = 'mstate' + str(i)
            ns = 'mnext_state' + str(i)
            inp = 'minput' + str(i)
            out = 'moutput' + str(i)
            state = request.POST.get(s)
            next_state = request.POST.get(ns)
            inputi = request.POST.get(inp)
            output = request.POST.get(out)
            if state == None or next_state == None or inputi == None or output == None:
                break
            if state not in transition:
                transition[state] = {}
            transition[state][inputi] = [next_state, int(output)]
            i += 1
    params = {'type': type, 'modname': name,
              'inp_size': input_size, 'enc': encoding,
              'States': states, 'Transition': transition,
              'start_state': start,
              }
    print(params)
    myfi = template_fileinput.render(type=type, name=name, input_size=input_size, encoding=encoding, states=states,
                                     transitions=transition)
    fil = open('media/' + name + '.txt', 'w')
    fil.write(myfi)
    fil.close()
    makeFSM_gui(params)
    if type == "Moore":
        test_in = request.POST.get("test_in")
        constraints = request.POST.get("constraints")
    else:
        test_in = request.POST.get("mtest_in")
        constraints = request.POST.get("mconstraints")
    if test_in != "":
        testbench(name, test_in, input_size)
    if constraints != "":
        constraints += '\n'
        tree = parser1.parse(constraints)
        res1 = FSMTransfomer1().transform(tree)
        make_constraints(res1, name)
        cons = "constraints_" + name
        build = template_build.render(modname=name, constraints=cons)
        file_dump("build.tcl", build)
        print('Build running')
        s = subprocess.call(["vivado", "-mode", "tcl", "-batch", "./files/build.tcl"], shell=True)
        print('Command run')
    return redirect(request.META['HTTP_REFERER'])
