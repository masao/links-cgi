#!/usr/local/bin/perl -w
# $Id$

package conf;

# データを保持するディレクトリ: `chmod a+rwx dir` しておく。
$DATADIR = 'data';

%PARAM = ();
$PARAM{'title'} = 'リンク集';
$PARAM{'email'} = 'webmaster@domain.name';
$PARAM{'name'} = 'だれそれ';
$PARAM{'home_url'} = 'http://domain.name/';
$PARAM{'home_title'} = 'ホーム';
