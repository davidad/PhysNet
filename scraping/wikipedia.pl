#!/usr/bin/perl -w

use Lingua::EN::Sentence qw( get_sentences );
use File::Slurp;

my $word = shift;
my $url = "http://en.wikipedia.org/wiki/$word";

system("wget --tries=3 $url -O /tmp/scraped.html -o /dev/null");
system("html2text -ascii /tmp/scraped.html > /tmp/scraped.txt");

my $text = read_file( "/tmp/scraped.txt" );
$text =~ s/\.(\[\d+\])/\1\./g;
my $sentences = get_sentences($text);

foreach my $sentence (@$sentences) {
  #print "$sentence\n\n===\n\n";
  $sentence =~ s/\n/ /g;
  if ($sentence =~ /([\d,.]+)\s*(lb|kg|pound|kilo|kilogram)s?/) {
    print "Wikipedia says: \"$sentence\"\nFrom this I got the following weights:\n";
    while ($sentence =~ m/([\d,.]+)\s*(lb|kg|pound|kilogram)s?/g) {
      my $num = $1;
      my $match = $&;
      my $units = "";
      if ($match =~ /(pound|lb)s?/) { $units = "lb"; }
      if ($match =~ /(kilo|kilogram|kg)s?/) { $units = "kg"; }
      $num =~ s/,//g;
      print "    $num $units\n";
    }
    print "\n";
  }
}

