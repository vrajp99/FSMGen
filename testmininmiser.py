def comp(t1,t2):
	if(t1[0]==t2[0] and t1[1]==t2[1]):
		return 1
	if(t1[0]==t2[1] and t1[1]==t2[0]):
		return 1
	return 0
def replce(a,b,trans_matrix):
	for i in range(len(trans_matrix)):
		val=list(trans_matrix.values())[i]
		for j in range(len(val)):
			if(val[str(j)]==a):
				val[str(j)]=b
	return trans_matrix
def rep(a,b,out_dict):
	for i in range(len(out_dict)):
		val=list(out_dict.keys())[i]
		if(val==a):
			val=b
	return out_dict

out_dict={'s0': 0, 's1': 0, 's2': 0, 's3': 0, 's4': 0, 's5': 0, 's6': 0, 's7': 0, 's8': 0, 's9': 0, 's10': 0, 's11': 0, 's12': 0, 's13': 0, 's14': 0, 's15': 0, 's16': 0, 's17': 0, 's18': 0, 's19': 0, 's20': 0, 's21': 0, 's22': 0, 's23': 1}  
trans_matrix = {'s0': {'1': 's1', '0': 's0'}, 's1': {'0': 's2', '1': 's1'}, 's2': {'1': 's3', '0': 's0'}, 's3': {'0': 's4', '1': 's1'}, 's4': {'1': 's5', '0': 's0'}, 's5': {'0': 's6', '1': 's1'}, 's6': {'0': 's7', '1': 's5'}, 's7': {'1': 's8', '0': 's0'}, 's8': {'0': 's9', '1': 's1'}, 's9': {'1': 's10', '0': 's0'}, 's10': {'0': 's11', '1': 's1'}, 's11': {'1': 's12', '0': 's0'}, 's12': {'0': 's13', '1': 's1'}, 's13': {'1': 's14', '0': 's7'}, 's14': {'0': 's15', '1': 's1'}, 's15': {'0': 's16', '1': 's5'}, 's16': {'1': 's17', '0': 's0'}, 's17': {'0': 's18', '1': 's1'}, 's18': {'1': 's19', '0': 's0'}, 's19': {'0': 's20', '1': 's1'}, 's20': {'1': 's21', '0': 's0'}, 's21': {'1': 's22', '0': 's13'}, 's22': {'0': 's23', '1': 's1'}, 's23': {'1': 's1', '0': 's0'}}
implication_chart=dict()
for i in range(1,len(out_dict.keys())):
  for j in range(0,i):
    if (list(out_dict.values())[i]==list(out_dict.values())[j]):
      pr1=list(out_dict.keys())[i]
      pr2=list(out_dict.keys())[j]
      tmp_dict=dict()
      for thi in range(len(trans_matrix[pr1])):
      	tmp_dict[list(trans_matrix[pr1].keys())[thi]]=(list(trans_matrix[pr1].values())[thi],list(trans_matrix[pr2].values())[thi])
      #implication_chart[(pr1,pr2)]={0:(trans_matrix[pr1][0],trans_matrix[pr2][0]),1:(trans_matrix[pr1][1],trans_matrix[pr2][1])}
      implication_chart[(pr1,pr2)]=tmp_dict

l=len(implication_chart)

minimised=[]
for i in range(l):
	t1=list(implication_chart.keys())[i]
	t2=implication_chart[t1]['0']
	t3=implication_chart[t1]['1']
	if comp(t1,t2):
		minimised.append(t2)
	if comp(t1,t3):
		minimised.append(t3)
for i in range(len(minimised)):
	trans_matrix = replce(minimised[i][0],minimised[i][1],trans_matrix)
x=[]
for i in range(len(list(trans_matrix.values()))):
	for j in range(i+1,len(list(trans_matrix.values()))):
		if(list(trans_matrix.values())[i]==list(trans_matrix.values())[j] and list(out_dict.values())[i] == list(out_dict.values())[j]):
			x.append(list(trans_matrix.keys())[i])
for i in set(x):
	trans_matrix.pop(i)
	out_dict.pop(i)
print(trans_matrix)
print(out_dict)			