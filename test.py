# -- encoding: utf-8 --
from labformat import load_lab
from reader import SentGator
if __name__=='__main__':
	txt_file='/home/willing/Documents/King-TTS-003/data/prosodylabeling/KING_tts001中文单句_100001-101000.txt'
	pos_file='/home/willing/proj/frontend/result/jieba/pos/tts001.txt'
	sent=SentGator(txt_file,pos_file)
	for words,rhythms,poses in sent:
		print ' '.join(words)
		print rhythms
		print poses
		raw_input('>>')
		load_lab(words,rhythms,poses)
