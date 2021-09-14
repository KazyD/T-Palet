#!/usr/bin/perl

# 辞書（dict2.csv）から単語を抽出して、voca形式の辞書を作る。
# 例）　./extract.pl 'いす 済む いそ いじり やし'  dict2.csv
# ex) ./extract.pl wordsFreq.txt dict2.csv
#

#if (@ARGV != 2) {
    #print "Usage extract.pl \"はい　そう　うん\" dict.csv\n";
    #exit;
#}

# get pattern
$pf = 'wordsFreq.txt';
open(PT, '<', $pf);
@list = ();
while (<PT>){
    chomp;
    our @list = split(/\s+/, $_)
}


# open dict file
$dictfile = 'dict2.csv';
open(DF, "<", $dictfile);

#-----------ここまでok-------------


# open output file
$outputfile = 'freq.voca';
open(OF, ">", $outputfile);

#-----------多分ok(freqがひらけてるかどうかの確認ができない)--------

# まず、listにある語を抽出
@ex = ();
while (my $df = <DF>) {
    chomp;
    foreach $w (@list) {
      # print $w;
	    #	if (/^($w),(.+),\"(.+)\"$/) {
	    if (/^($w),\s(.+),\s"(.+)"$/) {
	       push(@ex,"$1,$2,$3");
         # print @ex;
	    }
      # print 2;
    }
}

#-----------動く-------------

# カテゴリ順にsort
@exsorted = sort byCat @ex;

# カテゴリ毎に出力
# foreachの中に入ってない
$cat = '?';
print @exsorted;
foreach $w (@exsorted) {
    print 2;
    $w =~ /^(.+),(.+),(.+)$/;
    # それまでのカテゴリと異なっていたらカテゴリ名を出力
    if ($cat ne $2) {
	     $cat = $2;
	      print "% $2\n";
    }
    # 要素の出力
    print "$1\t$3\n";
}


# おしまい
close (PT);
close (DF);
close (OF);
exit;

# カテゴリのところ（2個目）で順序づけ
sub byCat {
    $a =~ /^.+,(.+),/;
    $w1 = $1;
    $b =~ /^.+,(.+),/;
    $w2 = $1;
    # 文字列の比較
    return $w1 cmp $w2;
}
