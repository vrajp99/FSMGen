from jinja2 import Environment, FileSystemLoader

def binsizer(n):
    return len(bin(n)[2:])

def binarytoGray(binary):
    gray = ""
    gray += binary[0]
    for i in range(1, len(binary)):
        gray += str(int(binary[i - 1]) ^ int(binary[i]))
    return gray


def encode(encodi, state_num, nstates):
    encodi = encodi.lower()
    sbi = bin(nstates-1)[2:]
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


env = Environment(loader=FileSystemLoader('./jtemplates/', followlinks=True))
template_always = env.get_template('always')
template_module = env.get_template('module')
template_case = env.get_template('case')
template_caseinput = env.get_template('caseinput')
template_caseinput_mealy = env.get_template('caseinputmealy')

def file_dump(flname, content):
    with open(flname, 'w') as fl:
        fl.write(content)

def makeMoore(modname, inp_size, state_output, states, transition_matrix, start,enc):
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


def makeMealy(modname, inp_size, states, transition_matrix, start,enc):
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

def testbench(modname,testin):
    code = ''
    code += "`timescale 1ns/1ps\n"
    code += "module tb_"+str(modname)+"();\n"
    code += "reg w,clk,reset;\n"
    code += "wire O;\n"
    code += modname+" m1(w,clk,reset,O);\n"
    code += "initial\n"
    code += "begin\n"
    code += "reset=1;w=0;\n#1 clk=0;\n"
    code += "#9 reset=0;\n"
    code += '''$monitor($time, , ,"clk=%b",clk,,"O=%b",O,,"reset=%b",reset,,"w=%b",w);\n'''
    for i in testin:
      code += "#10 w="+i+";\n"
    code += "end\n"
    code += "always\n"
    code += "#5 clk=~clk;\n"
    code += "initial\n"
    code += "#100 $finish ;\n"
    code += "endmodule\n"
    file_dump("tb_"+modname+'.v',code)


def makeFSM():
    print("type either 'moore' or 'mealy' :")
    moore_or_mealy=input()
    #enter moore or mealy
    print("either type 'ov' for overlapping or 'nonov' for nonoverlapping :")
    typ=input()
    #for overlapping type ov else type non ov
    print("type the input sequence (ex : '10101') :")
    a=input()
    #input for sequence ex:10110001
    print('Enter Module name: ')
    modname = input()
    print("Encoding: binary, gray, onehot, oncold -")
    enc = input()
    print("Enter testing sequence: ")
    testin = input()
    inp_size = 1
    if moore_or_mealy=='moore':
      d={}
      le=len(a)
      #le is the length of the input sequence
      for i in range(le+1):
        st='s'+str(i)
        d[st]={}
        #for every state initially an empty dictionary is created
      for i in range(le):
        st='s'+str(i)
        d[st][a[i]]='s'+str(i+1)
        #all trasitons for next adjacent states are mapped
        sn=a[:i]+'0' if a[i]=='1' else a[:i]+'1'
        #reference string with the last bit changed for finding length of maximum matching string
        for j in range(i+1):
          if a[:i+1-j]==sn[j-i-1:]:
            l=i+1-j
            break
            #for every state a loop runs to find the maximum length of matching string untill the current state with the last bit changed and if we find we break
        else:
          l=0
          # if the loop doesnt break it means nothing matched so default length matched would be 0  
        d[st][sn[-1]]='s'+str(l)
        # so all the states are mapped for both the inputs 1 and 0 except the last state
      if typ=='nonov':
        d['s'+str(le)]=d['s0']
        # in the case of non overlapping sequence detector once the correct sequence is detected the last state should point to the initial or the reset state
      else:
        #in the case of overlapping sequence detector we are again finding the maximum matching string length for both the cases 0 and 1 and then map the last state accordingly
        for i in range(le):
          stri0=a[i+1:]+'0'
          if stri0==a[:le-i]:
            d['s'+str(le)]['0']='s'+str(le-i)
            break
            #once it finds the maximum matching length it maps the last state and breaks
        else:
          d['s'+str(le)]['0']='s0'
          # default and base case
        for i in range(le):
          stri1=a[i+1:]+'1'
          if stri1==a[:le-i]:
            d['s'+str(le)]['1']='s'+str(le-i)
            break
            #once it finds the maximum matching length it maps the last state and breaks
        else:
          d['s'+str(le)]['1']='s0'
          # default and base case
      sd={}
      #this is for the state description
      for i in range(le):
        sd['s'+str(i)]=0
      # in moore sequence detectors for both overlapping and non overlapping only last state has 1 as ouput and rest all gve 0 as output
      sd['s'+str(le)]=1
      state_output = sd
      states = list(state_output.keys())
      start = states[0]
      transition_matrix = d
      makeMoore(modname, inp_size, state_output, states, transition_matrix, start,enc)
    else:
      #this is the generalised mealy state diagram generator for sequence detectors
      le=len(a)
      # it is the length of the input
      d={}
      for i in range(le):
        d['s'+str(i)]={}
        #this creates an empty dictionary for every state
      for i in range(le-1):
        d['s'+str(i)][a[i]]=['s'+str(i+1),0]
        #this map every state to the next adjacent state for the current input value
      for i in range(le-1):
        sn=a[:i]+'0' if a[i]=='1' else a[:i]+'1'
        # reference string with the last bit changed in the given sequence upto the length i
        for j in range(i+1):
          if a[:i+1-j]==sn[j-i-1:]:
            l=i+1-j
            break
            #so this is to map every state except the last one for the complementry current inputs, once it finds the maximum matching length it breaks
        else:
          l=0
          # default base case if nothing matched
        d['s'+str(i)][sn[-1]]=['s'+str(l),0]
        # every state is mapped for complementary current state input 
      st=a[:-1]+str(0 if int(a[-1]) else 1)
      # reference string only with last bit changed in the input sequence  
      li=0
      for i in range(le):
        if st[i:]==a[:le-i]:
          li=le-i
          break
      d['s'+str(le-1)][st[-1]]=['s'+str(li),0]
      # for the last state in the state graph if the last input doesnt match in both overlapping and non overlapping cases the state will be mapped to the same above mentioned state with output value as 0
      # but if the last input matches with the last bit of input sequence then there would be a difference in both overlapping and non overlapping cases which is as follows
      if typ=='nonov':
        d['s'+str(le-1)][a[-1]]=['s0',1]
        # in the case of non overlapping when the last input matched with last bit the state is mapped to first state with output value 1
      else:
        lr=0
        for i in range(1,le):
          if a[i:]==a[:le-i]:
            lr=le-i
            break
        d['s'+str(le-1)][a[-1]]=['s'+str(lr),1]
        # whereas in overlapping case again we run a loop for maximum overlapping sequence and map the last state accordingly
      states = list(d.keys())
      transition_matrix = d
      start = states[0]
      #so this prints the state description
      makeMealy(modname, inp_size, states, transition_matrix, start,enc)
    testbench(modname,testin)

makeFSM()