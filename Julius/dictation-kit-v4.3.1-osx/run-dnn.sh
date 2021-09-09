#! /bin/sh

# サーバとしては、この設定で動いているようです。
# これ全体で、サーバとして動く。
# dnn版
/Users/tam/prog/dictation-kit-v4.3.1-osx/bin/julius -C main.jconf -C am-dnn.jconf -module $* &
# gmm版
#/Users/tam/prog/dictation-kit-v4.3.1-osx/bin/julius -C main.jconf -C am-gmm.jconf -module $* &
sleep 10
# dnnclientとあるが、何のための処理か不明。
xterm -e python /Users/tam/prog/dictation-kit-v4.3.1-osx/bin/dnnclient.py dnnclient.conf &
sleep 2

xterm -e /Users/tam/prog/dictation-kit-v4.3.1-osx/bin/adintool -in mic -out vecnet -server 127.0.0.1 -paramtype FBANK_D_A_Z -veclen 120 -htkconf model/dnn/config.lmfb.40ch.jnas -port 5532 -cvn -cmnload model/dnn/norm.jnas

kill 0
