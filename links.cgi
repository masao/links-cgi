#!/usr/local/bin/perl -wT
# -*- CPerl -*-
# $Id$

use strict;
use CGI qw/:cgi/;
use CGI::Carp qw/fatalsToBrowser/;
use HTML::Template;
use IO::File;
use Text::CSV_XS;

$CGI::HEADERS_ONCE = 1;

use lib ".";
require "util.pl";
require "conf.pl";

my $catid = CGI::escapeHTML(param('catid')) || 0;

my %CATEGORY = load_category();

main();
sub main {
    print header("text/html; charset=EUC-JP");

    my $message = "";
    unless (defined $CATEGORY{$catid}) {
	$message .= "<p class=\"error-message\">そのカテゴリはありません。</p>";
    }
    my $tmpl = HTML::Template->new('filename' => 'template/links.html');
    $tmpl->param(%conf::PARAM,
		 'catnav' => get_catnav($catid, %CATEGORY),
		 'catlist' => get_catlist($catid, %CATEGORY),
		 'cat' => $CATEGORY{$catid}->{-name});
    print $tmpl->output;
}
