# mecabの出力フォーマットから単語、品詞、読みを抜き出す
# ex) ./getYomi.pl 000.txt(in) xxx.txt(out)

use strict;
use warnings;

# ファイルオープン
my $input = '/Users/deikazuki/T-Palet-Project/juliusTest/parsedText/parsed.txt';
my $output = '/Users/deikazuki/T-Palet-Project/juliusTest/parsedTest/yomi.txt';
# open (INFILE,'>','parsed.txt');
open (IN, "<$input") or die ('error');
#open (OUTFILE,'>', $output);

# print 'Hello World!';
# my $f = <IN>;
# print $f;

while (<IN>) {
    chomp;
    print 'Hello World!!';
    print $_;
    my $head;
    my $tail;
    ($head, $tail) = split(/\s+/, $_);
    $tail =~ /(.+),(.+),(.+),(.+),(.+),(.+),(.+)/;
    my $pos = $1;
    my $yomi = $7;
    print "$1 $head $7\n";
}

close(IN);
# close(OUT);
