import socket
# import time

HOST = '127.0.0.1'   # juliusサーバーのIPアドレス
PORT = 10500         # juliusサーバーの待ち受けポート
DATESIZE = 1024      # 受信データバイト数

# このクライアントを起動する前に、
# JuliusServerGmm.sh（普通のJulius）、またはJuliusServerDnn.sh（DNN）を立ち上げること

class Julius:

    def __init__(self):

        self.sock = None

    def run(self):

        # socket通信でjuliusサーバーに接続
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sock:
            self.sock.connect((HOST, PORT))

            strTemp = "" # 話した言葉を格納する変数
            fin_flag = False # 話終わりフラグ

            while True:

                # juliusサーバからデータ受信
                data = self.sock.recv(DATESIZE).decode('utf-8')

                for line in data.split('\n'):
                    # 受信データから、<WORD>の後に書かれている言葉を抽出して変数に格納する。
                    print('line= '+line)
                    # <WORD>の後に、話した言葉が記載されている。
                    index = line.find('WORD="')
                    if index != -1:
                        # strTempに話した言葉を格納
                        strTemp = strTemp + line[index+6:line.find('"',index+6)]
                        
                    # 受信データに</RECOGOUT>'があれば、話終わり ⇒ フラグをTrue
                    if '</RECOGOUT>' in line:
                        fin_flag = True

                # 話した言葉毎に、print文を実行
                if fin_flag == True:
                    if '晴れ' in strTemp:
                        print("今の天気は晴れ")
                    elif '雨' in strTemp:
                        print("今の天気は雨")
                    elif '曇' in strTemp:
                        print("今の天気は曇り")
                    elif '終わり' in strTemp:
                        exit(0)
                    else:
                        print("話した言葉：" + strTemp)
                    
                    fin_flag = False
                    strTemp = ""

if __name__ == "__main__":

    julius = Julius()
    julius.run()
    
