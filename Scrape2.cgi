#! /usr/bin/perl -w

# Scrape2.cgi - demonstrate screen-scraping in Perl
#               this one follows a link
#
# THIS IS NOT A FINISHED VERSION.  IT USES NO LOOPS OR FUNCTIONS.
# This is a "demonstration of concept" only.
#
# D Provine

use strict;
use CGI;
use WWW::Mechanize;
use HTML::TokeParser;
use DateTime;


# To get a week's worth of cartoons, we make a link to last
# Sunday and then follow the "next" links.  (Note: this program
# does not use a loop, but if you were doing the whole week you
# should.)

# find last Sunday
my $date = DateTime->now;

while ( $date->day_of_week != 7 ) {
    $date->subtract( days => 1 );
}

# URLs look like: http://www.tinasgroove.com/comics/march-2-2012/
# format the date the way the URL needs to look:

my @MonthName = qw( nomonth january february march april may june
                 july august september october november december );

# strftime() here is like the C version; see strftime(3)
my $displaydate = $date->strftime('%A, %e %B %Y');

# This is a roll-your-own because strftime() wants to make a
# two-digit day (either leading zero or space) and capitalises
# the monthname.
my $target = sprintf("%s-%d-%04d", $MonthName[$date->month()],
                      $date->day(), $date->year() );

# fetch the data:
my $agent = WWW::Mechanize->new();

my $url = 'http://www.tinasgroove.com/comics/' . $target;

$agent->get($url);
my $stream = HTML::TokeParser->new(\$agent->{content});
  
# First, get the cartoon:


# grab first div, and skip all divs that either do not have a
# class, or which class is not "entry-content"

my $tag = $stream->get_tag("div");

while (! $tag->[1]{class} or
         ( $tag->[1]{class} and $tag->[1]{class} ne 'entry-content') ) {
    $tag = $stream->get_tag("div");
}

# cartoon is next image
my $toon = $stream->get_tag("img");

# get attribute:
my $source = $toon->[1]{'src'};




# create CGI object and generate HTML:
my $cgi = new CGI;

print $cgi->header(-type=>'text/html'),
      $cgi->start_html("Tina's Groove Screen Scrape");

print $cgi->h1($displaydate);

print "<br />permalink: ";
print "<a href=\"$url\">";
print "$url";
print "</a>";

print $cgi->img({src=>$source}), "\n\n";


# There are other ways to fetch a cartoon, such as looking
# for the "li" tag which has an "a" in it and fetching the
# href.  You may need to do this if the "next" link has no
# text on it, or something.


# The text on the link arrow is "next  &raquo;", but
# that makes for trouble fetching, so we use a regex:
$agent->follow_link( text_regex => qr/next/ );
$stream = HTML::TokeParser->new(\$agent->{content});

# Re-parse this page same as up above:
# (The "grab a cartoon" thing should be in a function which
#  is called from a loop.  This is proof of concept only.)


$tag = $stream->get_tag("div");

while (! $tag->[1]{class} or
         ( $tag->[1]{class} and $tag->[1]{class} ne 'entry-content') ) {
    $tag = $stream->get_tag("div");
}

# cartoon is next image

print $cgi->h1("Monday");

$toon = $stream->get_tag("img");

# get attribute:
$source = $toon->[1]{'src'};
print $cgi->br(), "\n";

print $cgi->img({src=> $source}), "\n\n";


# ALL DONE!

print $cgi->end_html, "\n";

