# -- encoding: utf-8 --
from labstructure import LabStructure
ll=LabStructure()
ll.son=3
a=[]
a.append(ll)
print a[0].son
ll.son=8
print a[0].son
