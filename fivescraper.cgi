#! /usr/bin/perl -w

# Scrape1.cgi - demonstrate screen-scraping in Perl
# D Provine

use strict;
use CGI;
use WWW::Mechanize;     # This is the object that gets stuff
use HTML::TokeParser;   # This is the object that parses HTML
use Scalar::Util qw(looks_like_number);
# create new web agent and get a page
my $agent = WWW::Mechanize->new();
#code to get div contents
#my $comic_title = $stream->get_trimmed_text("/div");

####################################
# Get SMBC Comic
####################################

$agent->get("http://www.smbc-comics.com/");
# create new HTML parser and get the content from the web agent
my $stream = HTML::TokeParser->new(\$agent->{content});

#SMBC comics do not have a title, so we'll just get the comic
#advance to the img tag for the comic
my $comic = $stream->get_tag("img");
while ((not $comic->[1]{id}) || ($comic->[1]{id} and $comic->[1]{id} ne 'cc-comic')) {
    $comic = $stream->get_tag("img");
}
# get the attributes from the "img" tag:
my $smbc_source = $comic->[1]{'src'};
my $smbc_popup = $comic->[1]{'title'};


####################################
# Get Perry Bible Fellowship
####################################

$agent->get("http://www.pbfcomics.com/");
# create new HTML parser and get the content from the web agent
my $pbf_stream = HTML::TokeParser->new(\$agent->{content});

#pbf's comics are links on the homepage, they are the only <a> sections with names that are numbers
#
my $pbf_comic_tag = $pbf_stream->get_tag("a");
while ((not $pbf_comic_tag->[1]{name}) and (not looks_like_number($pbf_comic_tag->[1]{name}))) {
    $pbf_comic_tag = $pbf_stream->get_tag("a");
}

my $pbf_comic_link = "http://www.pbfcomics.com" . $pbf_comic_tag->[1]{'href'};

#first one with a name that is a number should be the most recent
$agent->get($pbf_comic_link);
$pbf_stream = HTML::TokeParser->new(\$agent->{content});

#SMBC comics do not have a title, so we'll just get the comic
#advance to the img tag for the comic
my $pbf_comic = $pbf_stream->get_tag("img");
while ($pbf_comic->[1]{id} and $pbf_comic->[1]{id} ne 'topimg') {
    $pbf_comic = $pbf_stream->get_tag("img");
}

my $pbf_source = "http://www.pbfcomics.com" . $pbf_comic->[1]{'src'};
#alt tag stores the title of the comic
my $pbf_title = $pbf_comic->[1]{'alt'};

####################################
# Get Penny Arcade
####################################

$agent->get("http://www.penny-arcade.com/comic");
# create new HTML parser and get the content from the web agent
my $pennyarcade_stream = HTML::TokeParser->new(\$agent->{content});
my $pennyarcade_comic_div = $pennyarcade_stream->get_tag("div");
while ($pennyarcade_comic_div->[1]{id} and $pennyarcade_comic_div->[1]{id} ne 'comicFrame') {
    $pennyarcade_comic_div = $stream->get_tag("div");
}
# get the cartoon:
my $pennyarcade_comic = $stream->get_tag("img");

my $pennyarcade_source = $pennyarcade_comic->[1]{'src'};
my $pennyarcade_title = $pennyarcade_comic->[1]{'alt'};

# Generate a bunch of output:
my $cgi = new CGI;

print $cgi->header(-type=>'text/html'),
      $cgi->start_html('Sample Screen Scraper');

print $cgi->h1("SMBC"), "\n";

print $cgi->img({src=>$smbc_source, alt=>$smbc_popup}), "\n\n";

print $cgi->p($smbc_popup), "\n";

print $cgi->h1("Perry Bible Fellowship: $pbf_title");

print $cgi->img({src=>$pbf_source, alt=>$pbf_title}), "\n\n";

print $cgi->p($pbf_comic_link), "\n";

print $cgi->h1("Penny Arcade: $pennyarcade_title");

print $cgi->img({src=>$pennyarcade_source, alt=>$pennyarcade_title}), "\n\n";


# ALL DONE!
print $cgi->end_html, "\n";

# now do "Over the Hedge" (note: same objects re-used, no "new()" )
#$agent->get("http://www.gocomics.com/overthehedge");
#$stream = HTML::TokeParser->new(\$agent->{content});

# HTML is like this:
# <div class="control-nav-newer"><a role='button' href=''
#      class='fa btn btn-outline-default btn-circle fa-caret-right sm disabled'
#      title='' ></a></div>
#    <div class="item-comic-container">
#    <header class="item-title">
#    <h1>
#    <a href="/overthehedge" class="link-blended">
#    Over the Hedge  <small> by T Lewis and Michael Fry</small>
#    </a>
#    </h1>
#    </header>
#
#    <a itemprop="image" class="item-comic-link js-item-comic-link "
#        href="/overthehedge/2017/02/08"
#         title="Over the Hedge for 2017-02-08">
#    <picture class="img-fluid item-comic-image">
#         <img width="900" sizes="100vw"
# srcset="http://assets.amuniversal.com/434e8380c950013441e2005056a9545d 1980w"
#  src="http://assets.amuniversal.com/434e8380c950013441e2005056a9545d" />
# </picture>
#
#    </a>
#    <meta itemprop="isFamilyFriendly" content="true">
#        </div><!-- /.item-comic-container -->
#
# I think we want the "img" tag inside the "picture" tag.

# Advance to the "div" tag we want:
#$tag = $stream->get_tag("picture");

#while ($tag->[1]{class} and $tag->[1]{class} ne 'item-comic-container') {
#    $tag = $stream->get_tag("div");
#}

#    while ($tag->[1]{class} and $tag->[1]{class} ne 'item-expand') {
#        $tag = $stream->get_tag("div");
#    }

# advance to the picture:
#$toon = $stream->get_tag("picture");

# advance to the image:
#$toon = $stream->get_tag("img");

# get the attribute from the tag:
#$source = $toon->[1]{'src'};

# add this to the CGI output

#print $cgi->h1("Over the Hedge");

#print $cgi->img({src=>$source, alt=>'Over the Hedge'}), "\n\n";


# ALL DONE!
#print $cgi->end_html, "\n";
