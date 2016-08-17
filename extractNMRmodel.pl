#!/usr/bin/perl
use strict;

my $file = $ARGV[0];
open(IN, "<", $file);

my @indata = <IN>;
my $i = 0;
my $base = $1 if $file =~ m/(\w+)\.pdb/;
my $header = '';

if ($ARGV[1] eq 'all') {
    foreach my $line (@indata) {
        if($line =~ /^MODEL/) {
            $i++;
            my $fnam="$base"."_"."$i.pdb";
            open(OUT, ">", $fnam);
            print OUT "$header";
            next;
        } elsif ($i == 0) {
            $header .= $line;
        }
        next if $line =~ /^ENDMDL/;
        if($line =~ /^ATOM/ || $line =~ /^HETATM/) {
            print OUT "$line";
        }
    }
} else {
    foreach my $line (@indata) {
        if($line =~ /^MODEL/) {
            $i++;
            print "$header" if $i == $ARGV[1];
            next;
        } elsif ($i == 0) {
            $header .= $line;
        }
        next if $line =~ /^ENDMDL/;
        if($ARGV[1] == $i and ($line =~ /^ATOM/ || $line =~ /^HETATM/)) {
            print "$line";
        }
    }
}


