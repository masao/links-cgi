#!/usr/local/bin/perl -wT
# -*- CPerl -*-
# $Id$

use strict;
use CGI qw/:cgi/;
use CGI::Cookie;
use CGI::Carp qw/fatalsToBrowser/;
use HTML::Template;
use Text::CSV_XS;
use Digest::MD5 qw/md5_hex/;

$CGI::HEADERS_ONCE = 1;

use lib ".";
require "util.pl";
require "conf.pl";

# 半角英数字のみ
my $PASSWD = '0123';

my %CATEGORY = load_category();

my $CATID = CGI::escapeHTML(param('catid')) || 0;
$CATID = 0 if not defined $CATEGORY{$CATID};

main();
sub main {
    if (my $cookie = has_valid_passwd()) {
	my $stat = 1;
	my $message = "";
	if (my $action = param('action')) {
	    if ($action eq "addcat") {
		$message .= action_addcat();
	    }
	}
	my $tmpl = HTML::Template->new('filename' => 'template/admin.html');
	$tmpl->param('title' => $conf::PARAM{'title'},
		     'catnav' => get_catnav($CATID, %CATEGORY),
		     'catlist' => get_catlist($CATID, %CATEGORY),
		     'cat' => $CATEGORY{$CATID}->{-name},
		     'catid' => $CATID,
		     'script' => url(-path_info => 1));
	print header(-type => "text/html; charset=EUC-JP",
		     -cookie => $cookie);
	print $tmpl->output;
    } else {
	my $tmpl = HTML::Template->new('filename' => 'template/login.html');
        $tmpl->param(%conf::PARAM,
		     'script' => url(-path_info => 1));
	print header(-type => "text/html; charset=EUC-JP");
        print $tmpl->output;
    }
}

sub action_addcat() {
    return "<p class=\"error-message\"カテゴリ名が指定されていません</p>\n"
	unless defined param('name');

    my $newid = max_id(%CATEGORY);
    $CATEGORY{$newid} = { -name => CGI::escapeHTML(param('name')),
			  -desc => CGI::escapeHTML(param('description')),
			  -parent => $CATID,
			  -subcat => "" };

    my @subcat = @{$CATEGORY{$CATID}->{-subcat}};
    push @subcat, $newid;
    $CATEGORY{$CATID}->{-subcat} = [ @subcat ];

    save_category(%CATEGORY);
    return "";
}

# CGI 引数 passwd を検証する
sub has_valid_passwd() {
    my $passwd = param('passwd');
    if (defined $passwd && $passwd eq $PASSWD) {
	my $cookie = new CGI::Cookie(-path => script_name(),
				     -name => 'passwd',
				     -value => md5_hex($PASSWD));
	return $cookie;
    }

    # Use cookie-password:
    my %cookie = fetch CGI::Cookie;
    if (defined $cookie{'passwd'}) {
	$passwd = $cookie{'passwd'}->value;
	if ($passwd eq md5_hex($PASSWD)) {
	    my $cookie = new CGI::Cookie(-path => script_name(),
					 -name => 'passwd',
					 -value => md5_hex($PASSWD));
	    return $cookie;
	}
    }
    return 0;
}

sub max_id(%) {
    my (%category) = @_;
    my @list = sort { $b <=> $a } keys %category;
    return ++$list[0];
}
