#!/usr/bin/perl

# 辞書（dict2.csv）から単語を抽出して、voca形式の辞書を作る。
# 例）　./extract.pl 'いす 済む いそ いじり やし'  dict2.csv
#
#

if (@ARGV != 2) {
    print "Usage extract.pl \"はい　そう　うん\" dict.csv\n";
    exit;
}

# get pattern
$_ = $ARGV[0];
my @list = split;

# open dict file
open(f,$ARGV[1]);

# まず、listにある語を抽出
@ex = ();
while (<f>) {
    chomp;
    foreach $w (@list) {
	#	if (/^($w),(.+),\"(.+)\"$/) {
	if (/^($w),\s(.+),\s"(.+)"$/) {
	    push(@ex,"$1,$2,$3");
	}
    }
}

# カテゴリ順にsort
@exsorted = sort byCat @ex;

# カテゴリ毎に出力
$cat = '?';
foreach $w (@exsorted) {
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
    

