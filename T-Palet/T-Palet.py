#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
改訂計画
1．出力する文言をSpeakerに集める
2. ランダム性
3. 人の時「さん」をつける
4. 音声入力
5. 割り込みの対話。復帰
"""
#from _typeshed import ReadableBuffer
import sys
import re

sys.path.append('/Users/deikazuki/T-Palet-Project/T-Palet')
import TObject as t
import Speaker as s
import MyException

# 大域変数
# 話題スタック
stk = []
# 4つの対象
ideal = None
current = None
refA = None
refB = None
# 発話エージェント
sp = s.Speaker()
# 話題スタックの深さ
l = 3
# 聞き返しの上限
lim = 3

# ローカルな関数群
# 話題とする一つの対象を決める
def select(ex,st):
    # 最初の要素を返す（暫定版）
    for e in st:
        if e is ex:
            continue
        return e
    return None

# 二つのオブジェクトについて属性atrの値を入れ替える
def exchange(ref1,ref2,atr):
    v1 = ref1.search(atr)
    ref1.delete(atr)
    v2 = ref2.search(atr)
    ref2.delete(atr)
    ref1.set(atr,v2)
    ref2.set(atr,v1)
    return

# 話題のスタックの操作
def push(e):
    stk.append(e)
    if len(stk) >= l:
        stk.pop(0)
    return
def pop():
    if empty():
        return None
    return stk.pop()
def empty():
    return stk == []

# 新しい話題
def newTopic():
    # ここにDBから不足の情報を見つけ、それをトピックにする機能を実装
    line = sp.askAndSet(ideal.surf+'、'+current.surf+'、'+refA.surf+'、'+refB.surf+'について、何か補足はありますか？')
    return 'End',None,None,None

# 最後の出力
def output():
    ideal.print()
    current.print()
    refA.print()
    refB.print()
    return

# ラダーリングのための4つの関数
def pairEvaluation(ref1,ref2):
    """
    Pair Evaluation: 対象ref1とref2を対比較する
    ref1, ref2:比較したい対象二つ
    返却値: 優位対象、下位対象、比較した属性

    目的：ref1 v.s. ref2 2組を対比較して情報収集
    発話意図：「対の比較」
    発話プラン
    1. 発話(質問, similarity(ref1, ref2))
    2. 発話(質問, difference(ref1, ref2))
    3. 発話(質問, その違いは重要？)
    3. 発話(質問, 上位を聞く)
    4. 発話(質問, reason of similarity)
    5. 発話(質問, which(ref1, ref2, ‘better’))
    6. Ladder print(ref1.surf)UpをnextToSay queueに入れておく
        手続き：仮にいい方をref1とすると
        手続き：Ladder Up(ref1, ref2)をnextToSay stackに入れておく
        手続き：仮に劣る方をref2とすると
        手続き：Ladder Down(ref2, ref1)をnextToSay stackに入れておく
    """
    try:
        print('PE('+ref1.surf+','+ref2.surf+')')
        # まず、似ているところを聞く
        sp.askAndSet(ref1,'similarTo'+ref2.surf,ref1.surf+'と'+ref2.surf+'との類似点は何ですか？')
        # 同じ属性をref2にもセット
        v = ref1.search('similarTo'+ref2.surf)
        ref2.set('similarTo'+ref1.surf,v)
        # 違いを聞いてみる。仮にref1が優位とする。
        sp.askAndSet(ref1,'advantageTo'+ref2.surf,ref1.surf+'と'+ref2.surf+'を比較して、違いはなんですか？')
        # lowerにもコピー（ただし'disadvantage'）
        v = ref1.search('advantageTo'+ref2.surf)
        ref2.set('disadvantageTo'+ref1.surf,v)
        # その違いは重要？
        sp.askAndSet(ref1,'reasonOfAdvantage','なぜ、その違いが重要なのですか？')
        # which is better?
        upper = ref1
        lower = ref2
        atr = v
        who = sp.ask('その違いについて、どちらが優れていますか？')
        # 逆なら入れ替え
        if who is ref2:
            for a in {'advantageTo'+ref2.surf,
                      'disadvantageTo'+ref1.surf,
                      'reasonOfAdvantage'} :
                exchange(ref1,ref2,a)
            upper = ref2
            lower = ref1
        # いつか、どこかでLadder UPする
        push(('LadderUp',upper,lower,v))
        # いつか、どこかでLadder Downする
        push(('LadderDown',lower,upper,v))
        #
        return upper,lower,atr
    except Exception as ex:
        if ex.code == 'exit1':
            sp.speak('途中ですが、終わります')
            exit()
        else:
            sp.speak('質問を変えます')
            return
#
def soloEvaluation(ref,atr,suchthat):
    """
    Solo Evaluation: 対象（ref）を単独で評価する
    ref: 調べる対象TObject
    atr: 焦点となった属性
    suchthat: 条件
    返却値：対象、話題の属性

    目的：指定の対象についての不足情報収集
    発話意図：対象について情報収集すること
    発話プラン：
    1. 手続き：知識蓄積ベース中でsuchthatに合う属性atrを見つける
    2. 質問：その属性の値を問う
    　　または、なぜその属性を選んだのかを問う
    3. 手続き：一つの対象(ref2)を決める
    4. 手続き：refとref2の違いを求める(attr2)
    5. 手続き：PariEvaluation(ref, ref2, attr2, suchthat2)をnextToSay stackに入れる
    """
    try:
        print('SE('+ref.surf+',atr:'+atr+',suchthat:'+suchthat+')')
        a = None
        # 属性指定がないとき
        if atr == None:
            # まずsuchthatにあう属性を調べる
            a = ref.findAttr(suchthat)
            if a == None:
            # どの様な観点を重視するか
                sp.askAndSet(ref,'priority','どの様な観点を重視しますか？')
                a = ref.search('priority')
                if a == None:
                    return ref,None
                sp.askAndSet(ref,a,a+'について、もう少し詳しく話して下さい')
            else:
            # 属性aのことを説明してもらう
                sp.askAndSet(ref,a,a+'について、もう少し詳しく話して下さい')
        else:
            sp.askAndSet(ref,atr,atr+'について、もう少し詳しく話して下さい')
            a = atr
        # 後でPair Evalするために、一つの対象を決める
        refTmp = select(ref,{ideal,current,refA,refB})
        # 話題がないときに、refとrefTmpを対評価するためにスタックにpush
        push(('PairEvaluation',ref,refTmp,'dummy'))
        return ref,a
    except Exception as ex:
        if ex.code == 'exit1':
            sp.speak('途中ですが、終わります')
            exit()
        else:
            sp.speak('質問を変えます')
            return
#
def ladderUp(ref,ref1,atr):
    """
    Ladder Up: ラダー・アップする
    ref: 調べる対象TObject
    ref1: 参照TObject
    atr: 焦点の属性
    返却値：対象、属性

    目的：優位対象(upper)について、優れた要素(atr)を探し、評価の観点（理由）を求める
    発話意図：優れたとされた理由を求めること
    発話プラン：
    1. 手続きSoloEvaluation(ref,atr,suchthat:良い理由)
    1に失敗した場合：
    　　手続きPairEvaluation(ref, ref1, atr, suchthat(is(ref, atr, Val1) &
            is(ref1,atr, Val2) & Val1 > Val2))
    2. 発話(確認, is(upper, atr, ‘high’))
    3. 発話(質問, why(is(upper, atr, ‘high’)))
    """
    try:
        print('LU('+ref.surf+',atr:'+atr+',ref1:'+ref1.surf+')')
        # まず、いい理由を確認
        _,atr1 = soloEvaluation(ref,atr,'reason')
        if atr1 == None:
            atr1 = findAttr(ref,ref1)
            if atr1 == None:
                return ref, None
        sp.speak(ref,ref.surf + 'は' + atr1 + 'の評価が高いですね')
        sp.askAndSet(ref,'reasonOf'+atr1,'それは、なぜですか？')
        return ref, atr1
    except Exception as ex:
        if ex.code == 'exit1':
            sp.speak('途中ですが、終わります')
            exit()
        else:
            sp.speak('質問を変えます')
            return
#
def ladderDown(ref,ref1,atr):
    """
    Ladder Down: ラダー・ダウンする
    ref: 調べる対象TObject
    ref1: 参照TObject
    atr: 焦点の属性
    返却値：対象、属性

    目的：下位対象(lower)について、negative要素(atr)を探し、具体的な改善方法を問う
    発話意図：negative要素の改善策、例の提示
    発話プラン：
    1. 手続きSoloEvaluation(lower, attr, suchthat(is(lower, attr, ‘low’)))
    or 手続きSoloEvaluation(lower, attr, suchthat(is(lower, attr, ‘negative’)))
    1に失敗した場合：
        手続きPairEvaluation(lower, ref, attr, suchthat(is(lower, attr, Val1) & is(ref,attr,Val2) & Val1<Val2)))
    2. 発話(確認, is(lower, attr, ‘low’))
    3. 発話(質問, howmuch(lower, attr, Var))
    4. 発話(依頼, example(is (lower, attr, Var)))
    """
    try:
        print('LD('+ref.surf+',atr:'+atr+',ref1:'+ref1.surf+')')
        # lowな属性を探す
        _, atr1 = soloEvaluation(ref,'None','low')
        if atr1 == None:
            _, atr1 = soloEvaluation(ref,None,'negative')
            if atr1 == None:
                sp.askAndSet(ref,'negative',ref.surf + 'の何が悪かったのですか？')
        # atr1がまずい
        sp.speak(ref.surf+'の'+atr1+'が悪かったのですね')
        sp.askAndSet(ref,atr1+'How',atr1+'がどの様に悪かったのですか')
        sp.askAndSet(ref,atr1+'improve',atr1 + 'を改善する方法、あるいはその例をあげて下さい')
        return ref, atr1
    except Exception as ex:
        if ex.code == 'exit1':
            sp.speak('途中ですが、終わります')
            exit()
        else:
            sp.speak('質問を変えます')
            return

# 初期化（質問省略版）
def initA():
    global ideal,current,refA,refB
    # 理想
    ideal = t.TObject('完治')
    ideal.set('level',9)
    # 現状
    current = t.TObject('凡太')
    current.set('level',6)
    # 参照1
    refA = t.TObject('良夫')
    refA.set('level',7)
    # 参照2
    refB = t.TObject('良子')
    refB.set('level',4)
    return

# 初期化。会話により入力
def initB():
    global ideal,current,refA,refB
    global sp
    # 理想の人の入力
    name = sp.ask('理想の人の名前を教えてください？')
    ideal = t.TObject(name)
    level = sp.ask(name+'さんのレベルはいくつですか（1〜10）？')
    ideal.set('level',level)
    ideal.print()
    # 現状（自分）の入力
    name = sp.ask('あなたの名前を教えてください？')
    current = t.TObject(name)
    level = sp.ask(name+'さんのレベルはいくつですか（1〜10）？')
    current.set('level',level)
    # 参照1の入力
    name = sp.ask('参考人の名前を教えてください？')
    refA = t.TObject(name)
    level = sp.ask(name+'さんのレベルはいくつですか（1〜10）？')
    refA.set('level',level)
    # 参照2の入力
    name = sp.ask('もう一人の参考人の名前を教えてください（1〜10）？')
    refB = t.TObject(name)
    level = sp.ask(name+'さんのレベルはいくつですか（1〜10）？')
    refB.set('level',level)
    return

# プロフィールつくり
def profile(ref):
    global sp
    global lim
    #
    sp.speak(ref.surf+'さんについて、教えてください。例えば、「身長は170ｃｍです」みたいに。')
    rep = sp.askAtrVal('「終わり」で終了です。',lim)
    while True:
        if rep == 'end':
            break
        elif rep == 'giveup':
            sp.speak('ちょっと聞き取れませんでした。')
            return
            break
        else:
            atr,val = rep
            ref.set(atr,val)
            rep = sp.askAtrVal('他にはありますか？',lim)
    sp.speak(ref.surf + 'さんについて、属性が入力されました。ありがとうございました。')
    return
"""
    while True:
        rep = sp.ask(q)
        if rep == 'end':
            break
        for p in avPtn:
            result = p.match(rep)
            if result:
                yesNo = sp.ask(ref.surf+'さんの'+result.group(1)+'は'+result.group(3)+'で、いいですか？')
                ref.set(result.group(1),result.group(3))
                break
        else:
            sp.speak('よく分かりません。「身長は170ｃｍです」の様に答えてください')
"""

# メインプログラム
if __name__ == '__main__':

    try:
        # 初期値 initA()かinitB()のどちらかを選ぶ
        # 以下は仮の値の設定
        initA()
        # 初期化。会話により入力
        #initB()

        # ここから会話のスタート
        # まず、4人のプロフィールについて
        # sp.speak('まず、'+ideal.surf+'さんについて教えてください')
        profile(ideal)
        # sp.speak('次に、'+current.surf+'さんについて教えてください')
        # profile(current)
        # sp.speak('ついでに、'+refA.surf+'さんについて教えてください')
        # profile(refA)
        # sp.speak('おまけで、'+refB.surf+'さんについて教えてください')
        # profile(refB)
        # はじまり
        # idealとcurrentを比較してみよう（とりあえずこれは動かす）
        # pairEvaluation(ideal,current)
    # ここでの例外＝「終了」
    except Exception as ex:
        if ex.code == 'exit1':
            sp.speak('途中ですが、終わります')
            exit()
        else:
            pass

    # スタック（積み残しの話題）と、新しい話題の取り込み付
    while False:
        if not empty():
            type,ref1,ref2,atr = pop()
            if type == 'PairEvaluation':
                pairEvaluation(ref1,ref2)
                continue
            elif type == 'LadderUp':
                ladderUp(ref1,ref2,atr)
                continue
            elif type == 'LadderDown':
                ladderDown(ref1,ref2,atr)
                continue
            elif type == 'SoloEvaluation':
                soloEvaluation(ref1,atr,None)
                continue
        # スタックが空になった（＝新しい話題が必要）
        type,ref1,ref2,atr = newTopic()
        if type == 'PairEvaluation':
            pairEvaluation(ref1,ref2)
            continue
        elif type == 'LadderUp':
            ladderUp(ref1,ref2,atr)
            continue
        elif type == 'LadderDown':
            ladderDown(ref1,ref2,atr)
            continue
        elif type == 'SoloEvaluation':
            soloEvaluation(ref1,atr,None)
            continue
        elif type == 'End':
            break
    # おしまい
    print("---"*10)
    output()
    sp.speak('終わります。\n\n\n')
    sp.close()
