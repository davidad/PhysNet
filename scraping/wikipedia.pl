#!/usr/bin/perl -w

use utf8;
use Lingua::EN::Sentence qw( get_sentences );
use HTML::Parse;
use HTML::FormatText;
use Scalar::Util qw( looks_like_number );
use JSON;

sub sigfigs {
  my $num = shift;
  if($num =~ s/([^0-9]|0(?![0.,]*[1-9]))//g) {
    return length($num);
  }
  return 0;
}

my $word = shift;
my $url = "http://en.wikipedia.org/wiki/$word";

system("wget --tries=3 $url -O /tmp/scraped.html -o /dev/null");
my $html = parse_htmlfile( "/tmp/scraped.html");
$formatter = HTML::FormatText->new(leftmargin =>0, rightmargin => 2048);
$text = $formatter->format($html);
$text =~ s/.//g;
$text =~ s/\."?((.\d+.)+)(?=\s+)/$1\. /g;
my $sentences = get_sentences($text);

%vals = ();

foreach my $sentence (@$sentences) {
  #print "$sentence\n\n===\n\n";
  $sentence =~ s/\n/ /g;
  if ($sentence =~ /([\d,.]+)\s*(lb|kg|pound|kilo|kilogram)s?/) {
    #print "Wikipedia says: \"$sentence\"\nFrom this I got the following weights:\n";
    my @sentence_vals = ();
    #while ($sentence =~ m/(?<min>[\d,.]+)?\s*(to|and|between|-|–)?\s*([\d,.]+)\s*(lb|kg|pound|kilogram)s?/g) {
    while ($sentence =~ m/(?<num>[\d,.]+)(?=(\s*(to|between|and|-|–)\s*([\d,.]+))?\s*(?<units>lb|kg|pound|kilogram)s?)/g) {
      my $num = $+{'num'};
      my $match = $&;
      my $units = $+{'units'};
      if    ($units =~ /(kilo|kilogram|kg)s?/) { $units = "kg"; }
      elsif ($units =~ /(pound|lb)s?/) { $units = "lb"; }
      $num =~ s/,//g;
      #print "    $num $units";
      if ($units =~ /lb/) {
        $kg = 0.453 * $num;
        #print " ($kg kg)";
        push(@sentence_vals, $kg);
      } else {
        push(@sentence_vals, $num);
      }
      #print "\n";
    }
    #print "\n";
    @sentence_vals = sort {$a <=> $b} @sentence_vals;
    my $valcount = @sentence_vals;
    if($valcount >= 2) {
      for ($i=0; $i<($valcount-1); $i++) {
        if($sentence_vals[$i]) {
          $ratio =$sentence_vals[$i+1]/$sentence_vals[$i];
          if($ratio < 1.1 and $ratio > 0.9) {
            if(sigfigs($sentence_vals[$i]) > sigfigs($sentence_vals[$i+1])) {
              delete $sentence_vals[$i];
            } else {
              delete $sentence_vals[$i+1];
            }
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

#print "\n\nIN SORTED ORDER:\n";
#foreach $val (sort {$a <=> $b} (keys(%vals))){
#  print "$val\t$vals{$val}\n";
#}

print to_json(\%vals, {pretty => 1});
