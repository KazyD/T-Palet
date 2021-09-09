# 例外（主に会話の逸脱による）しょり
class MyException(Exception):
    code = 5
    def __init__(self,code):
        self.code = code
        if code == 'exit1':
            print("XXX")
        else:
            print("YYY")
        return
