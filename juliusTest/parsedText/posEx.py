import MeCab

if __name__ == '__name__':
	f = open('parsed.txt', 'r')
	fout = open('mecwords.txt', 'w')
	print(f)
	mecab = MeCab.Tagger()
	n = f.readline()
	while n :
		par = mecab.parseToNode(n)
		while par :
			p = par.feature.split(',')[0] + '	' + par.surface
			fout.write(p)
			fout.write('\n')
			par = par.next
		n = f.readline()
	f.close()
	fout.close()