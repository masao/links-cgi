# -*- CPerl -*-
# $Id$

use IO::File;

# 汚染されている変数をキレイにする。（CGI::Untaint のローカル実装）
sub untaint {
    my ($tainted, $pattern, $default) = @_;
    # print "\$tainted: $tainted\t\$pattern: $pattern\t\$default:$default\n";
    return $default if !defined $tainted;

    if ($tainted =~ /^($pattern)$/) {
        # print "matched.\n";
        return $1;
    } else {
        return $default;
    }
}

sub load_category() {
    my %cat = ();
    my $fh = fopen("category.txt");
    my $csv = Text::CSV_XS->new({ eol => "\n" });
    while (my $line = <$fh>) {
	$csv->parse($line) || next;
	my @cols = $csv->fields();
	my $id = shift @cols;
	my $name = shift @cols;
	my $desc = shift @cols;
	my $parent = shift @cols;
	next unless defined $id;
	@cols = () if !defined $cols[0] || !length($cols[0]);
	$cat{$id} = { -name => $name,
		      -desc => $desc,
		      -parent => $parent,
		      -subcat => [ @cols ] };
    }
    return %cat;
}

sub save_category(%) {
    my (%category) = @_;
    my $fh = fopen(">category.txt");
    my $csv = Text::CSV_XS->new({ eol => "\n" });
    foreach my $id (sort keys %category) {
	$csv->print($fh,
		    [ $id,
		      $category{$id}->{-name},
		      $category{$id}->{-desc},
		      $category{$id}->{-parent},
		      @{$category{$id}->{-subcat}} ]);
    }
}

sub get_catnav($%) {
    my ($catid, %category) = @_;
    my $str = "<strong class=\"catnav-here\">${$category{$catid}}{-name}</strong>";
    my @catlist = ();
    my $parent = $category{$catid}->{-parent};
    while (defined $parent && length $parent) {
	$str = "<a href=\"links.cgi?catid=$parent\">${$category{$parent}}{-name}</a> &gt; $str";
	$parent = $category{$parent}->{-parent};
    }
    return $str;
}

sub get_catlist($%) {
    my ($catid, %category) = @_;
    my $str = "<ul class=\"catlist\">";
    my $subcat = $category{$catid}->{-subcat};
    foreach my $id (@$subcat) {
	$str .= "<li><span class=\"catitem\"><a href=\"";
	$str .= CGI::escapeHTML(script_name()) ."?catid=$id\">";
	$str .= $category{$id}->{-name} ."</a></span>\n";
    }
    $str .= "</ul>\n";
    return $str;
}

# 効率よくファイルの中身を読み込む。
sub readfile ($) {
    my ($fname) = @_;
    my $fh = fopen($fname);
    my $cont = '';
    my $size = -s $fh;
    read $fh, $cont, $size;
    $fh->close;
    return $cont;
}

sub fopen($) {
    my ($fname) = @_;
    my $fh = new IO::File;
    $fh->open($fname) || die "fopen: $fname: $!";
    return $fh;
}

# For avoiding "used only once: possible typo at ..." warnings.
sub muda {}
1;
