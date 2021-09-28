import neologdn
import pandas as pd
import MeCab
import re
import sys

def normalize(self,c):
    return neologdn.normalize(c)

def extracter(self,n):
    # <笑い>を消す
    e1 = re.sub('<.+>','',n)
    # (うん)などを消す
    e2 = re.sub('\(.+\)','',e1)
    return e2

def analiseMorph(self,e):
    # 辞書指定
    tagger = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    # 分かち書き
    parse = tagger.parse(e)
    """
    for row in parse.split('\n'):
        w = row.split('\t')[0]
        if word == "EOS":
            break
    """
    print(parse)

    return

def main():
    path = '/Users/deikazuki/T-Palet-Project/juliusTest/cleanText/data019.txt'

    f = open(path,"w")

    print(f)
    print("アイウエオ")

    content = f.read()

    # テキストの正規化
    n = normalize(content)

    # <○○>の除去
    e = extracter(n)

    # 分かち書き
    analiseMorph(e)

    f.close()


if __name__ == '__name__':
    print("あいうえお")
    main()
