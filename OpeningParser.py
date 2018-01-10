rfile=open("FICSGames2016.txt","r")
wfile=open("Openings.txt","w")

plylim=20
gamelim=100000

def IsNum(ci):
	if (ci>=ord('0') and ci<=ord('9')):
		return 1
	return 0

class Node:
	def __init__(self,freq,dict):
		self.freq=freq
		self.dict=dict
		
trie=[]
trie.append(Node(0,{}))
	
cttrie=1
ctgame=0
while (ctgame<gamelim):
	s=rfile.readline()
	if (len(s)==0):
		break
	if (s[0]=='1'):
		ctply=0
		curind=0
		for var in s.split():
			if (not IsNum(ord(var[0]))):
				var.replace('+','')
				trie[curind].freq+=1
				if (var in trie[curind].dict):
					curind=trie[curind].dict[var]
				else:
					trie[curind].dict[var]=cttrie
					trie.append(Node(0,{}))
					curind=cttrie
					cttrie+=1
				ctply+=1
				if (ctply==plylim):
					break
		ctgame+=1

for node in trie:
	s=str(node.freq)+' '
	for var in node.dict:
		s+=(var+' ')
		s+=(str(node.dict[var])+' ')
	s+='\n'
	wfile.write(s)

print(cttrie,ctgame)

wfile.close()


















