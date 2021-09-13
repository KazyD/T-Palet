class TObject():
    """
    T-Palet法によるセッションで、対象とされるもの
    """
    # 表層
    surf = 'ソレ'
    def __init__(self):
        self.frame = dict([])
        self.surf = 'ソレ'
        return
    def __init__(self,name):
        self.frame = dict([])
        self.surf = name
        self.set('surf',name)
        return

    # 属性を出力
    def print(self):
        print(self.frame)
        return
    # 属性を設定
    def set(self,a,v):
        self.frame.setdefault(a,v)
        self.print()
        return
    # 属性を検索
    def search(self,a):
        try:
           return self.frame[a]
        except KeyError:
            return None
    # 属性を削除
    def delete(self,a):
        return self.frame.pop(a)

    # 対象selfからsuchthatにあう属性を見つけ、属性名を返す
    def findAttr(self,suchthat):
        if suchthat == 'best':
            None
        elif suchthat == 'positive':
            None
        elif suchthat == 'negative':
            None
        else:
            return None
        return None
