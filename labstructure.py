# -- encoding: utf-8 --
class LabStructure(object):
	def __init__(self):
		self.lbrother=None
		self.rbrother=None
		self.father=None
		self.sons=[]
		self.sons_num=0
		self.txt=''
		self.rhythm=''
		self.id=0
		self.index=0

	def __init__(self,lbrother=None,rbrother=None,father=None,sons=[],sons_num=0,txt='',rhythm='',index=0):
		self.lbrother=lbrother
		self.rbrother=rbrother
		self.father=father
		self.sons=sons
		self.sons_num=sons_num
		self.txt=txt
		self.rhythm=rhythm
		self.index=index
	
	def adjust(self):
		def setfather(lab):
			lab.father=self
		map(setfather,self.sons)
		self.sons_num=len(self.sons)
		self.txt='/'.join(son.txt for son in self.sons)
