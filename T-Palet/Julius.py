import socket
import os
import time

HOST = '127.0.0.1'   # IPアドレス
PORT = 10500         # Juliusとの通信用ポート番号
DATESIZE = 1024      # 受信データバイト数

class Julius():
    pid = 0

    def __init__(self):
        try:
            # ソケットのオープン
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST,PORT))
            return
        except ConnectionRefusedError:
            # Juliusサーバが立ち上がってない
            print('Please wait for 10 sec.')
            self.pid = os.fork()
            if self.pid != 0:
                os.execl('/Users/deikazuki/Julius/T-Palet/JuliusServerDnn.sh','JuliusServerDnn.sh')
                time.sleep(5)
                os.wait()

            else:
                time.sleep(5)
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect((HOST,PORT))
            return

    def input(self):
        try:
            data = ''
            while True:
                if '</RECOGOUT>' in data:
                    recog_text = ''
                    for line in data.split('\n'):
                        index = line.find('WORD="')
                        if index != -1:
                            line = line[index+6:line.find('"',index+6)]
                            recog_text = recog_text + ' ' + line
                    print("認識結果： "+recog_text)
                    data = ''
                    return recog_text
                else:
                    data += str(self.client.recv(1024).decode('utf-8'))
                    # print("data : ",data)
        except KeyboardInterrupt:
            print('finished')
            #self.client.send('DIE'.encode('utf-8'))
            #self.client.close()
            return 'キーボード割り込みで終わり'

if __name__ == "__main__":

    julius = Julius()
    while True:
        text = julius.input()
        print(text)
        if '終わり' in text:
            julius.client.send('DIE'.encode('utf-8'))
            julius.client.close()
            break

