#! /bin/sh

# これ全体で、サーバとして動く。
# システム起動前に、このサーバを立ち上げること
# サーバーとしての常駐は当面保留！！！

cd /Users/deikazuki/T-Palet-Project-Julius/dictation-kit-v4.3.1-osx

# 以下、dnn版（深層学習版）
bin/julius -C main.jconf -C am-dnn.jconf -module $* &
sleep 10

# dnnclientとあるが、DNNでの認識処理
xterm -e python bin/dnnclient.py dnnclient.conf &
sleep 2

# 波形データの処理
xterm -e bin/adintool -in mic -out vecnet -server 127.0.0.1 -paramtype FBANK_D_A_Z -veclen 120 -htkconf model/dnn/config.lmfb.40ch.jnas -port 5532 -cvn -cmnload model/dnn/norm.jnas

kill 0
