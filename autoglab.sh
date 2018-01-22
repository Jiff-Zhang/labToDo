#/bin/bash
for x in `ls ../result/jieba/pos/`
do
	python test.py ~/Documents/King-TTS-003/data/prosodylabeling/KING_${x/.txt/}* ../result/jieba/pos/$x ~/Documents/King-TTS-003/data/sfs1/${x/.txt/} ~/Documents/King-TTS-003/data/wave/channel1/1001/ lab/
done
