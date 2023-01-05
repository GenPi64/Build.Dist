#!/usr/bin/perl
my $ph;
die if (!open($ph, '-|', "git ls-remote --tags https://github.com/raspberrypi/linux.git"));
my %tags;
while (my $line = <$ph>)
{
    $tags{$2} = $1 if ($line =~ /refs\/tags\/(.*\.([0-9]{8}(-1)?))/);
}	
my $latest_tag = $tags{(sort(keys(%tags)))[-1]};
my $header = `curl -s https://raw.githubusercontent.com/raspberrypi/linux/$latest_tag/Makefile | head -4`;
if ($header =~ /VERSION = (\d+)\nPATCHLEVEL = (\d+)\nSUBLEVEL = (\d+)/m)
{
    my $kernel_version = "$1.$2.$3";
    print("$latest_tag is kernel version $kernel_version\n");
}
