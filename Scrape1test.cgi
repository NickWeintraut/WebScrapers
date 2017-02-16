#! /usr/bin/perl -w

# Scrape1.cgi - demonstrate screen-scraping in Perl
# D Provine

use strict;
use CGI;
use WWW::Mechanize;     # This is the object that gets stuff
use HTML::TokeParser;   # This is the object that parses HTML

# create new web agent and get a page
my $agent = WWW::Mechanize->new();
$agent->get("http://www.xkcd.com/");

# create new HTML parser and get the content from the web agent
my $stream = HTML::TokeParser->new(\$agent->{content});


# First, get the title:
# HTML is like this: <div id="ctitle">Enlightenment</div>

# get the first "div" tag to setup the loop...
my $tag = $stream->get_tag("div");

while ($tag->[1]{id} and $tag->[1]{id} ne 'ctitle') {
    $tag = $stream->get_tag("div");
}

# get the text of that tag:
my $comic_title = $stream->get_trimmed_text("/div");


# advance to the div with the cartoon:
while ($tag->[1]{id} and $tag->[1]{id} ne 'comic') {
    $tag = $stream->get_tag("div");
}

# get the cartoon:
my $toon = $stream->get_tag("img");

# get the attributes from the "img" tag:
my $source = $toon->[1]{'src'};
my $popup = $toon->[1]{'title'};
my $caption = $toon->[1]{'alt'};


# Generate a bunch of output:
my $cgi = new CGI;

print $cgi->header(-type=>'text/html'),
      $cgi->start_html('Sample Screen Scraper');

print $cgi->h1("XKCD: $comic_title"), "\n";

print $cgi->p($caption), "\n";

print $cgi->img({src=>$source, alt=>$caption}), "\n\n";

print $cgi->p('<i>(' . $popup . ')</i>');



# now do "Over the Hedge" (note: same objects re-used, no "new()" )
$agent->get("http://www.gocomics.com/overthehedge");
$stream = HTML::TokeParser->new(\$agent->{content});

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
$tag = $stream->get_tag("picture");

while ($tag->[1]{class} and $tag->[1]{class} ne 'item-comic-container') {
    $tag = $stream->get_tag("div");
}

#    while ($tag->[1]{class} and $tag->[1]{class} ne 'item-expand') {
#        $tag = $stream->get_tag("div");
#    }

# advance to the picture:
$toon = $stream->get_tag("picture");

# advance to the image:
$toon = $stream->get_tag("img");

# get the attribute from the tag:
$source = $toon->[1]{'src'};

# add this to the CGI output

print $cgi->h1("Over the Hedge");

print $cgi->img({src=>$source, alt=>'Over the Hedge'}), "\n\n";


# ALL DONE!
print $cgi->end_html, "\n";

