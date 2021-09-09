#! /bin/sh

# システム起動前に、このサーバを立ち上げること
# julius内で認識の処理を行う

cd /Users/deikazuki/Julius/dictation-kit-v4.3.1-osx

# gmm版
bin/julius -C main.jconf -C am-gmm.jconf -module $*
