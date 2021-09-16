# mecabフォーマットを変形したファイルからvoca辞書を作る

# ファイルを開く
open(FH,'<',$ARGV[0]);
open(FD,'>',$ARGV[1]);

#各行を読んでいき、品詞ごと単語を取っていく
while (<FH>) {
    $_ =~ /^(.+)(\s)(.+)(\s)(.+)$/;
    my $w = $2;
    print FD "$w ";
}

close(FH);
close(FD);
