# -- encoding: utf-8 --
from labstructure import LabStructure
import re,copy
from sys import exit
from txt2pinyin import txt2pinyin

rhythm_map={'ph':'phone','#0':'rhythm0','#1':'rhythm1_2','#2':'rhythm1_2','#3':'rhythm3','#4':'rhythm4'}

def tree_per_word(word,rhythm,tree_init,syllables):
	def get_list(rhythm):
		return tree_init[rhythm_map[rhythm]]
	
	# print get_list('#4')
	assert rhythm in rhythm_map
	rhythm_list=get_list(rhythm)

	if rhythm=='ph':
		newLab=LabStructure(txt=word,index=len(rhythm_list)+1,rhythm=rhythm)

	elif rhythm in ['#0','#1','#2']:
		if rhythm=='#0':
			for syllable in syllables[0:len(word)/3]:
				for phones in syllable:
					tree_per_word(phones,'ph',tree_init,syllables)
			del syllables[0:len(word)/3]
			newLab=LabStructure(sons=get_list('ph'),txt=word,index=len(rhythm_list)+1,rhythm=rhythm)
			tree_init['assist'][rhythm_map['ph']]=get_list('ph')[-1]
			tree_init[rhythm_map['ph']]=[]
			newLab.adjust()
			newLab.txt=word
		else:
			tree_per_word(word,'#0',tree_init,syllables)
			newLab=LabStructure(sons=get_list('#0'),index=len(rhythm_list)+1,rhythm=rhythm)
			tree_init['assist'][rhythm_map['#0']]=get_list('#0')[-1]
			tree_init[rhythm_map['#0']]=[]
			newLab.adjust()

	elif rhythm in ['#3','#4']:
		if rhythm=='#3':
			tree_per_word(word,'#1',tree_init,syllables)
			newLab=LabStructure(sons=get_list('#1'),index=len(rhythm_list)+1,rhythm=rhythm)
			tree_init['assist'][rhythm_map['#1']]=get_list('#1')[-1]
			tree_init[rhythm_map['#1']]=[]
		else:
			tree_per_word(word,'#3',tree_init,syllables)
			newLab=LabStructure(sons=get_list('#3'),index=len(rhythm_list)+1,rhythm=rhythm)
			tree_init['assist'][rhythm_map['#3']]=get_list('#3')[-1]
			tree_init[rhythm_map['#3']]=[]
		newLab.adjust()
	else:
		print 'error rhythm input'
		exit(-1)


	if len(rhythm_list)!=0:
		newLab.lbrother=rhythm_list[-1]
		rhythm_list[-1].rbrother=newLab
		# if rhythm!='ph':
		# 	newLab.sons[0].lbrother=rhythm_list[-1].sons[-1]
		# 	rhythm_list[-1].sons[-1].rbrother=newLab.sons[0]
	elif tree_init['assist'][rhythm_map[rhythm]]:
		newLab.lbrother=tree_init['assist'][rhythm_map[rhythm]]
		tree_init['assist'][rhythm_map[rhythm]].rbrother=newLab
	rhythm_list.append(newLab)
	# tree_init['assist'][rhythm_map[rhythm]]=newLab


def show(tree_list,shift=0):
	for item in tree_list:
		print '|\t'*shift+str(item.index)+'\t'+item.txt+'\t'+item.rhythm+'\t'+str(item.sons_num)
		show(item.sons,shift+1)


def tree(words,rhythms,syllables):
	assert len(words)==len(rhythms)
	assert len(''.join(words))/3==len(syllables)
	tree_init={'assist':{}}
	for key,value in rhythm_map.items():
		tree_init[value]=[]
		tree_init['assist'][value]=None
	# print tree_init
	syllable_copy=copy.deepcopy(syllables)
	for word,rhythm in zip(words,rhythms):
		tree_per_word(word,rhythm,tree_init,syllable_copy)
	# print tree_init['rhythm4']
	# show(tree_init['rhythm4'],0)
	def get_first():
		return tree_init['rhythm4'][0].sons[0].sons[0].sons[0].sons[0]
	return get_first()

def main():
	txt='继续#1把#1建设#2有#1中国#1特色#3社会#1主义#1事业#4推向#1前进'
	words=re.split('#\d',txt)
	# print ' '.join(words)
	syllables=txt2pinyin(''.join(words))
	# print syllables
	rhythms=re.findall('#\d',txt)
	rhythms.append('#4')
	# print ' '.join(rhythms)
	print ' '.join(words)
	print rhythms
	print syllables
	phone=tree(words,rhythms,syllables)
	while phone:
		print phone.txt,
		phone=phone.rbrother
	print
	#print syllables

main()
