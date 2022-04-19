#!/usr/bin/perl
#
#
# to run:
#   perl parse_emerge_log.pl >emerge_as_of_`date +'%Y%m%d_%a_%H%M_%Z'`.txt 2>&1
#

use strict;
use warnings;

my $emerge_log = "/home/jlpoole/emerge.log";
$emerge_log = "/home/jlpoole/emerge_as_of_2022_03_19_1720.log";
#$emerge_log = "/home/jlpoole/emerge_202203150814.log";
#
# made a copy so Perl's opening the file does not interfere
# with any pending emerge writes
#

my $content;
{
   local $/;
   open(IN,$emerge_log) or die "could not open $emerge_log";
   $content = <IN>;
   close(IN);
}
#
# get the start time from the first emerge
#
$content =~  /\n(\d+)\:\s+((\>\>\>\s+emerge|\:\:\:\s+completed)\s+\((.*?)\) (\S+) to).*?/s;
my $prior = $1;
=pod

here is a sample section:

1647232142:  >>> emerge (2 of 116) sys-apps/gentoo-functions-0.15 to /
1647232143:  === (2 of 116) Cleaning (sys-apps/gentoo-functions-0.15::/var/db/repos/gentoo/sys-apps/gentoo-functions/gentoo-functions-0.15.ebuild)
1647232143:  === (2 of 116) Compiling/Packaging (sys-apps/gentoo-functions-0.15::/var/db/repos/gentoo/sys-apps/gentoo-functions/gentoo-functions-0.15.ebuild)
1647232218:  === (2 of 116) Merging (sys-apps/gentoo-functions-0.15::/var/db/repos/gentoo/sys-apps/gentoo-functions/gentoo-functions-0.15.ebuild)
1647232243:  >>> AUTOCLEAN: sys-apps/gentoo-functions:0
1647232243:  === Unmerging... (sys-apps/gentoo-functions-0.14)
1647232259:  >>> unmerge success: sys-apps/gentoo-functions-0.14
1647232277:  === (2 of 116) Post-Build Cleaning (sys-apps/gentoo-functions-0.15::/var/db/repos/gentoo/sys-apps/gentoo-functions/gentoo-functions-0.15.ebuild)
1647232277:  ::: completed emerge (2 of 116) sys-apps/gentoo-functions-0.15 to /

=cut
#
# Print to STDERR so it will elude piped sort
#
print STDERR "Secs\tMinute\tCompletion date\tOrder\tPackage\n";

#while ($content =~ /\n(\d+)\:\s+((\>\>\> emerge|\:\:\: completed) \(.*?\) (\S+) to)/sg){
#while ($content =~ /\n(\d+)\:\s+((\>\>\>\s+emerge|\:\:\:\s+completed)\s+\((.*?)\) (\S+) to).*?/sg){
my $total_time = 0;
while ($content =~ /\n(\d+)\:\s+((\:\:\:\s+completed emerge)\s+\((.*?)\) (\S+) to).*?/sg){
     my $timestamp = $1;
     my $delta = $timestamp - $prior;
     $prior = $timestamp;

     my $status = $3;
     my $order = $4;
     my $package = $5;
     my $date = localtime($timestamp);
     my $elapsed_time = &convert_to_minutes($delta);
     $total_time += $delta;
     print "$delta\t$elapsed_time\t$date\t$order\t$package\n";
}
my $total_elapsed_time = &convert_to_minutes($total_time);
my $total_hours = int($total_time/(60*60));
print "Total time: $total_elapsed_time minutes, ~ $total_hours hours\n";
print "Completed $0 at ".localtime."\n";
print "----------------- $0 below -----------------\n\n";
print `cat -n $0`;

#
#  input: seconds
#
sub convert_to_minutes {
   my ($seconds) = @_;
#   if ($seconds < 60){
#     return "$seconds seconds";
#   } else {
     my $minutes = int($seconds/60);
     my $extra_secs = $seconds % 60;
     return ("$minutes min $extra_secs secs");
#   }
}
