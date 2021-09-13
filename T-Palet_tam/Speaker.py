from MyException import MyException
import sys
import re
# sys.path.append('/usr/local/lib/python3.7/site-packages')
import MeCab
# sys.path.append('/usr/local/lib/python3.6/site-packages')
# import CaboCha
import Julius as jls
import re
import PtnList as ptn
import os
import time
import Client as w

# 大域変数
#parser = None
julius = None
win = None
# 属性に関する質問のパターン
avPtn = []
# 聞き返しの上限
lim = 3

# ローカルな関数群

# yes/noを問う。lは聞き返しの上限
def yesNo(obj,msg,l):
    if l == 0:
        obj.speak('ちょっと、何言っているのか分かりません！')
        return 'giveup'
    # メッセージの出力
    obj.speak(msg)
    rep = julius.input()
    # noを調べる
    for w in ptn.noList:
        if w in rep:
            return 'no'
    # yesを調べる
    for w in ptn.yesList:
        if w in rep:
            return 'yes'
    # 聞き返し
    return yesNo(obj,'もう一度お願いします。',l-1)

# 「終わり」の検出
def isEnd(rep):
    for w in ptn.endList:
        if w in rep:
            return True
    return False

# カボチャ
"""
# 応答の整形
# synonymの対応、あるいは特定文字列の変換
def reform(text):
    l = sent2morph(text)
    print(l)
    for w in l:
        if w in ptn.stop:
            # 中断？
            raise MyException('exit1')
    return text

# カボチャ
def sent2morph(sent):
    m = parser.parse(sent)
    size = m.size()
    ret = []
    for i in range(size):
        token = m.token(i)
        # 表層を返すケース。下記と、どちらかを選択すべし
        ret.append(token.surface)
        # 基本形を返すケース
        # features = token.feature
        # pos, ctype, cform, form, read, phonetic = extFeature(features)
        # ret.append(form)
    return ret

# featureの処理他
def extFeature(features):
    pos = ctype = cform = form = read = phonetic = ''
    pattern = '(\S+),(\S+),(\S+),(\S+),(\S+),(\S+),([^,]+),([^,]+),([^,]+)'
    result = re.match(pattern,features)
    if result:
        pos = result.group(1)
        pos += '-' + result.group(2)
        pos += '-' + result.group(3)
        pos += '-' + result.group(4)
        ctype = result.group(5)
        cform = result.group(6)
        form = result.group(7)
        read = result.group(8)
        phonetic = result.group(9)
    return pos, ctype, cform, form,read, phonetic
"""

class Speaker():

# メソッド
    def __init__(self):
        #global parser,julius
        global julius,avPtn
        # カボチャを起動
        # parser = CaboCha.Parser('-n1')
        # Juliusを起動
        julius = jls.Julius()
        time.sleep(5)
        # 応答の正規表現のパターンのリスト
        for p in ptn.avList:
            avPtn.append(re.compile(p))
        # 表示用windowの立ち上げ
        #os.execl('/Users/tam/prog/T-Palet/displayProcess.sh','displayProcess.sh')    
        w.com_send('\n\n\n')
        w.com_send('        ******開始******')
        return

    # 将来いいメッセージの表示を考える
    def display(self,s):
        #print(s)
        w.com_send(s)
        return

    # 単に話す
    def speak(self,s):
        if s == None:
            self.display('???')
            return
        self.display(s)
        return

    # 質問、応答。応答の情報をDBにストア
    def askAndSet(self,ref,atr,sent):
        # sentを発言し、応答をrefのatrにセット
        # 属性の確認
        self.speak(sent)
        # 仮
        #self.speak('Add Q,A,O at the head of sentence to indicate the type')
        # カボチャを使うとき
        # text = input()
        # val = reform(text)
        # Juliusを使うとき
        val = julius.input()
        ref.set(atr,val)
        #print(val)
        return "None"

    # 質問して、応答にある、属性、値を返す
    def askAtrVal(self,q,l):
        global lim
        # どうしても聞き取れない。
        if l == 0:
            self.speak('ちょっと、何言っているのか分からないので、諦めます。')
            return 'end'
        #
        global avPtn
        self.speak(q)
        # Juliusを使う
        rep = julius.input()
        if isEnd(rep):
            return 'end'
        # 「(.+) (は|が) (.+) です 」のバリエーションを試す
        for p in avPtn:
            result = p.match(rep)
            if result:
                # 確認する
                yesno = yesNo(self,result.group(1)+'の値が'+result.group(3)+'で、いいですか？',lim)
                if yesno == 'yes':
                    return result.group(1),result.group(3)
                elif yesno == 'no':
                    return self.askAtrVal(self,q + 'について、もう一度お願いします。',l-1)
        return self.askAtrVal('もう一度お願いします。',l-1)

    # close
    def close(self):
        julius.close()
        return
"""
    # 単純な質問、応答を返す
    def ask(self,q):
        self.speak(q)
        # カボチャを使うときは、単純に以下の２行のみ
        text = input()
        val = reform(text)
        return val
"""