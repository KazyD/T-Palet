import os
import sys
import socket
import signal

HOST = '127.0.0.1'   # juliusサーバーのIPアドレス
PORT = 10500         # juliusサーバーの待ち受けポート
DATESIZE = 1024      # 受信データバイト数
No = 1		     # サーバーの個数
julius = '/Users/tam/prog/dictation-kit-v4.3.1-osx/JuliusServerDnn.sh'
#julius = '/Users/tam/prog/dictation-kit-v4.3.1-osx/JuliusServerGmm.sh'

child_processes = []

def main(host, port, children):
    signal.signal(signal.SIGTERM, accept_sigterm)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)

    # fork
    for i in range(children):
        pid = os.fork()
        if pid != 0:
            # parent
            print('child process: pid=%d, getpid=%d\n' % (pid, os.getpid()))
            child_processes.append(pid)
        else:
            # child
            break
        break

    if pid != 0:
        # wait for child
        os.wait()
    else:
        # accept
        while True:
            conn, addr = s.accept()
            print(julius + '  started')
            os.execl(julius,julius)
        conn.close()

def accept_sigterm(sig, status):
    for pid in child_processes:
        os.kill(pid, signal.SIGTERM)
    sys.exit(0)

if __name__ == '__main__':
    main(HOST, PORT, No)
