# -- encoding:utf-8 --
from os.path import exists,join
import re,wave
from sys import argv

class SentGator(object):
	def __init__(self,txt_file,pos_file,sfs_dir,wav_dir):
		assert exists(txt_file)
		assert exists(pos_file)
		assert exists(sfs_dir)
		self.txt_file=txt_file
		self.pos_file=pos_file
		self.sfs_dir=sfs_dir
		self.wav_dir=wav_dir

	def __iter__(self):
		txt_file=open(self.txt_file)
		## 读入文本韵律行
		txt_line=txt_file.readline()
		## 由于文本第一行前会有一段无效信息，所以先去除，具体原因暂不清楚
		txt_line=txt_line[3:]
		pos_file=open(self.pos_file)
		## 读入词性行
		pos_line=pos_file.readline()
		## 由于词性文本第一行前会有一段无效信息，所以先去除，具体原因暂不清楚
		pos_line=pos_line[6:]

		while txt_line:
			## 读入音节行
			syl_line=txt_file.readline()
			
			## 去除文本韵律行、词性行以及音节行前后的无用空白（制表符、换行等）
			txt_line=txt_line.strip()
			syl_line=syl_line.strip()
			pos_line=pos_line.strip()
			
			## 分离文本韵律行的行号
			sent_id,sent=txt_line.split('\t')
			txt_words=re.split('#[1-4]',sent)
			rhythm=re.findall('#[1-4]',sent)
			rhythm.append('#4')
			assert len(rhythm)==len(txt_words)
			pos_words=re.split('\t',pos_line)

			
			rhythms=[]
			words=[]
			poses=[]

			start=0
			total_bit=0
			for pos_word in pos_words:
				txt,pos=pos_word.split('_')
				pre_set_rhythm='#0'
				while start<len(txt_words):
					total_bit+=len(txt_words[start])
					if total_bit>len(txt):
						total_bit-=len(txt)+len(txt_words[start])
						break
					elif total_bit==len(txt):
						total_bit=0
						pre_set_rhythm=rhythm[start]
						start+=1
						break
					pre_set_rhythm=max(pre_set_rhythm,rhythm[start])
					start+=1

				if txt!='《':
					if txt=='》':
						rhythms[-1]=max(pre_set_rhythm,rhythms[-1])
					else:
						rhythms.append(pre_set_rhythm)
						words.append(txt)
						poses.append(pos)

			## sfs 文件处理
			times=[]
			phs_type=[]
			sfs_file=join(self.sfs_dir,sent_id+'.SFS1')
			# print sfs_file
			assert exists(sfs_file)
			with open(sfs_file) as sfs_file:
				for line in sfs_file:
					time,ph_type=line.split()
					times.append(int(float(time)*10e6))
					phs_type.append(ph_type)
				sfs_file.close()

			# assert phs_type[-1]=='s'

			# wav 获取总时长
			wav_file=join(self.wav_dir,sent_id+'.wav')
			assert exists(wav_file)
			wav_file=wave.open(wav_file,'rb')
			params=wav_file.getparams()
			nchannels,sampwidth,framerate,nframes=params[:4]
			times.append(int((nframes*1.0/framerate)*10e6))
			wav_file.close()


			yield words,rhythms,poses,times,phs_type,sent_id

			# print sent_id,'\t',sent
			# print '\t',' '.join(words)
			# print '\t',poses
			# print '\t',rhythms
			# print '\t',syl_line
			# print


			## 读入下一行 
			txt_line=txt_file.readline()
			pos_line=pos_file.readline()

		txt_file.close()
		pos_file.close()




if __name__=='__main__':
	## 存放文本（包含文本、韵律和拼音）
	txt_file='/home/willing/Documents/King-TTS-003/data/prosodylabeling/KING_tts001中文单句_100001-101000.txt'
	## 词性文本（包含文本和词性）
	pos_file='/home/willing/proj/frontend/result/jieba/pos/tts001.txt'
	sfs_dir='/home/willing/Documents/King-TTS-003/data/sfs1/tts001'
	wav_dir='/home/willing/Documents/King-TTS-003/data/wave/channel1/1001'
	if len(argv)==5:
		script,txt_file,pos_file,sfs_dir,wav_dir=argv
	else:
		assert len(argv)==1
	for words,rhythms,poses,times,phs_type,sent_id in SentGator(txt_file,pos_file,sfs_dir,wav_dir):
		print ' '.join(words)
		print rhythms
		print poses
		print times
		print phs_type
