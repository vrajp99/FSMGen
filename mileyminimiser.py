
trans_matrix = {'s0': {'1': ['s1', 0], '0': ['s0', 0]}, 's1': {'0': ['s2', 0], '1': ['s1', 0]}, 's2': {'1': ['s3', 0], '0': ['s0', 0]}, 's3': {'0': ['s4', 0], '1': ['s1', 0]}, 's4': {'1': ['s5', 0], '0': ['s0', 0]}, 's5': {'0': ['s6', 0], '1': ['s1', 0]}, 's6': {'1': ['s7', 0], '0': ['s0', 0]}, 's7': {'0': ['s8', 0], '1': ['s1', 0]}, 's8': {'1': ['s9', 0], '0': ['s0', 0]}, 's9': {'0': ['s10', 0], '1': ['s1', 0]}, 's10': {'0': ['s11', 0], '1': ['s9', 0]}, 's11': {'1': ['s12', 0], '0': ['s0', 0]}, 's12': {'1': ['s1', 0], '0': ['s0', 1]}}
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
			if(val[str(j)][0] ==a):
				val[str(j)][0]=b
	return trans_matrix
def rep(a,b,trans_matrix):
	for i in range(len(trans_matrix)):
		val=list(trans_matrix.keys())[i]
		if(val==a):
			val=b
	return trans_matrix

implication_chart=dict()
for i in range(1,len(trans_matrix.keys())):
  for j in range(0,i):
    if (list(trans_matrix.values())[i]==list(trans_matrix.values())[j]):
      pr1=list(trans_matrix.keys())[i]
      pr2=list(trans_matrix.keys())[j]
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
		if(list(trans_matrix.values())[i]==list(trans_matrix.values())[j]):
			x.append(list(trans_matrix.keys())[i])
for i in set(x):
	trans_matrix.pop(i)
	trans_matrix.pop(i)
print(trans_matrix)	
