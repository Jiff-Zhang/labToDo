# -- encoding: utf-8 --
from labformat import load_lab
from reader import SentGator
from os.path import exists,join
from sys import argv,exit
if __name__=='__main__':
	txt_file='/home/willing/Documents/King-TTS-003/data/prosodylabeling/KING_tts001中文单句_100001-101000.txt'
	pos_file='/home/willing/proj/frontend/result/jieba/pos/tts001.txt'
	sfs_dir='/home/willing/Documents/King-TTS-003/data/sfs1/tts001'
	wav_dir='/home/willing/Documents/King-TTS-003/data/wave/channel1/1001'
	lab_dir='/home/willing/proj/frontend/labToDo/lab'
	if len(argv)==6:
		script,txt_file,pos_file,sfs_dir,wav_dir,lab_dir=argv
	elif len(argv)!=1:
		script=argv[0]
		print 'Usage: python',script,'txt_file pos_file sfs_dir wav_dir lab_dir'
		exit(-1)
	print txt_file
	assert exists(txt_file) and exists(pos_file) and exists(sfs_dir) and exists(wav_dir) and exists(lab_dir)
	sent=SentGator(txt_file,pos_file,sfs_dir,wav_dir)
	for words,rhythms,poses,times,phs_type,sent_id in sent:
		# print ' '.join(words)
		# print rhythms
		# print poses
		# print times
		# print phs_type
		# raw_input('>>')
		lab_file=join(lab_dir,sent_id+'.lab')
		with open(lab_file,'w') as lab_file:
			load_lab(words,rhythms,poses,times,phs_type,lab_file=lab_file)
			lab_file.close()
