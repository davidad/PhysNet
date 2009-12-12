#!/usr/bin/perl -w

use Lingua::EN::Sentence qw( get_sentences );
use File::Slurp;
use Scalar::Util qw( looks_like_number );

my $word = shift;
my $url = "http://en.wikipedia.org/wiki/$word";

system("wget --tries=3 $url -O /tmp/scraped.html -o /dev/null");
system("html2text -ascii /tmp/scraped.html > /tmp/scraped.txt");

my $text = read_file( "/tmp/scraped.txt" );
$text =~ s/\.(\[\d+\])/$1\./g;
my $sentences = get_sentences($text);

%vals = ();

foreach my $sentence (@$sentences) {
  #print "$sentence\n\n===\n\n";
  $sentence =~ s/\n/ /g;
  if ($sentence =~ /([\d,.]+)\s*(lb|kg|pound|kilo|kilogram)s?/) {
    print "Wikipedia says: \"$sentence\"\nFrom this I got the following weights:\n";
    my @sentence_vals = ();
    while ($sentence =~ m/([\d,.]+)\s*(lb|kg|pound|kilogram)s?/g) {
      my $num = $1;
      my $match = $&;
      my $units = "";
      if ($match =~ /(kilo|kilogram|kg)s?/) { $units = "kg"; }
      if ($match =~ /(pound|lb)s?/) { $units = "lb"; }
      $num =~ s/,//g;
      print "    $num $units";
      if ($units =~ /lb/) {
        $kg = 0.453 * $num;
        print " ($kg kg)";
        push(@sentence_vals, $kg);
      } else {
        push(@sentence_vals, $num);
      }
      print "\n";
    }
    print "\n";
    my $valcount = @sentence_vals;
    if($valcount >= 2) {
      for ($i=0; $i<($valcount-1); $i++) {
        if($sentence_vals[$i]) {
          $ratio =$sentence_vals[$i+1]/$sentence_vals[$i];
          if($ratio < 1.1 and $ratio > 0.9) {
            delete $sentence_vals[$i+1];
          }
        }
      }
    }
    foreach my $val (@sentence_vals) {
      if(looks_like_number($val)) {
        $vals{$val} = $sentence;
      }
    }
  }
}

print "\n\nIN SORTED ORDER:\n";
foreach $val (sort {$a <=> $b} (keys(%vals))){
  print "$val\t$vals{$val}\n";
}
