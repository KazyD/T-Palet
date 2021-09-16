import re
import MeCab
import collections
import pykakasi

class preProcessing():

    def __init__(self):
        return

    def cleaning(self):
        """
        @で始まる行を消す
        同じ人の発話を１行にまとめる
        """
        # 先頭の正規表現
        head = '(F|M)(\d+)：'
        wl = '(F|M)(\d+)'
        end = 'ＥＮＤ'
        comp = re.compile(head)
        comp_w = re.compile(wl)
        comp_e = re.compile(end)
        # 1ファイルずつ処理
        for i in range(1,130):
            ln=0
            # print(i)
            fr = open(f'/Users/deikazuki/T-Palet-Project/juliusTest/nuccText/data{i:03d}.txt','r')
            fw = open(f'/Users/deikazuki/T-Palet-Project/juliusTest/cleanText/data{i:03d}.txt','w')
            # 1行ずつ処理
            while True:
                ln += 1
                # print('---',ln)
                line = fr.readline()
                l = fr.tell()
                line = re.sub('\n','',line)
                # %の場合には次に行く
                if line.startswith('％'):
                    continue
                # EOFの場合にループを抜ける
                if not line:
                    break
                # endで終了
                rr = comp_e.match(line)
                if rr:
                    break
                # 先頭が@か判定
                if not line.startswith('＠'):
                    # 先頭がForMで数字が来た後に:があれば採用
                    res = comp.match(line)
                    if res:
                        line_a = re.sub(head, '', line)
                        # line_a = line.lstrip(head)
                        # 次の行を見て、同じ人の発話ならくっつける
                        """
                        while True:
                            line_ = fr.readline()
                            # endで終了
                            rr = comp_e.match(line)
                            if rr:
                                break
                            line_ = re.sub('\n','',line_)
                            if not line:
                                break
                            res_ = comp.match(line_)
                            if res_:
                                fr.seek(l)
                                break
                            else:
                                line_a += line_
                                l = fr.tell()
                                ln+=1
                                print('---',ln)
                                continue
                        """

                        fw.write(line_a)
                        fw.write('\n')
                        continue
                    else:
                        res_w = comp_w.match(line)
                        if res_w:
                            continue
                        fw.write(line)
                        fw.write('\n')
                        continue
                else:
                    continue
        # ファイルのクローズ
        fr.close()
        fw.close()

    def parse(self):
        w = []
        # MeCabインスタンス
        # m = MeCab.Tagger('-Owakati')
        m = MeCab.Tagger ('-Ochasen')
        #
        for i in range(1,130):
            fr = open(f'/Users/deikazuki/T-Palet-Project/juliusTest/cleanText/data{i:03d}.txt','r')
            fw = open(f'/Users/deikazuki/T-Palet-Project/juliusTest/parsedText/data{i:03d}.txt','w')
            # print(fr)
            # print(fw)
            # 1行づつ処理
            text = fr.read()
            node = m.parseToNode(text)
            while node:
                w.append(node.surface)
                node = node.next
            # fw.write(text)
            """
            while True:
                line = fr.readline()
                line = re.sub('\n', '', line)
                print(line)
                # EOFの場合にループを抜ける
                if not line:
                    break
                # 分かち書き
                result = m.parse(line)
                # print(result)
                fw.write(result)
                w.append(result)
            """
            # クローズ
            fr.close()
            fw.close()

            return w

    def split(self):
        fo = open('/Users/deikazuki/T-Palet-Project/juliusTest/mecabed.txt','r')
        word = '(.+)(\s+)(.+)'
        comp = re.compile(word)
        headlist=[]

        line = fo.readline()

        while line:
            m = comp.match(line)
            head = m.group(1)
            headlist.append(head)
            line = fo.readline()

        fo.close()

        return headlist

    def count(self,words):
        word = '(\')(.*)(\')'
        comp = re.compile(word)
        fw = open('/Users/deikazuki/T-Palet-Project/juliusTest/words3.txt','w')
        c = collections.Counter(words)
        # mc = c.most_common(2000)
        w, num  = zip(*c.most_common(2000))

        # 漢字 → 平仮名
        k = pykakasi.kakasi()
        # k.setMode('J', 'H')
        # conv = k.getConverter()

        #result = comp.match(words)
        #print(w)
        #print(type(w))

        for i in range(len(w)):
            wc = k.convert(w[i])
            fw.write(wc[0]['hira'])
            fw.write(' ')

        return


if __name__ == "__main__":
    pp = preProcessing()
    # f = open('/Users/deikazuki/T-Palet-Project/juliusTest/words.txt','w')

    pp.cleaning()

    words = pp.parse()

    #heads = pp.split()

    #for i in range(len(heads)):
        #print(heads[i],end='')
        #print(' ',end='')

    pp.count(words)
    print('finished !')
