﻿# Program for adding LACITO markup into plain text vocabulary lists.
# voc2xml.pl 
# Inserts markup in plain-text vocabulary lists, and adds temporal alignment from a 'Regions List' in .txt format. (Exported from SoundForgeTM.)
# Created in 2011 by Alexis Michaud.
# This is version 1 of the script, September 2011.
# COMMANDLINE: perl -w voc2xml.pl
# This script assumes that the vocabulary list is in voc.txt in the same directory, and the file containing the regions list in regions.txt, also in the perl directory.

# The xml output is in a file "xmlout.xml".
# The program treats groups of lines in fixed order: IPA; French; Chinese; English.
# It can handle notes/comments: paragraphs before the French translation and starting with a percent sign % are interpreted as notes concerning the word at issue.
#
# Example: portion of text input: 
# tʰɑ˧-hõ˧
# ne va pas ! (ton lexical: M)
# 别走！
# do not go! (lexical tone: M)

# tʰɑ˧-hwæ˧
# %phonétiquement: proche de : tʰæ˧-hwæ˧
# n'achète pas! (ton lexical: M)
# 别买！
# do not buy! (lexical tone: M)



# Declaration of modules used in this script
use Encode;		# to decode UTF-8
use utf8; 			# UTF-8 coding for Unicode. 
# "UTF-8 treats the first 128 codepoints, 0..127, the same as ASCII. They take only one byte per character. 
# All other characters are encoded as two or more (up to six) bytes using a complex scheme. 
# Fortunately, Perl handles this for us, so we don't have to worry about this."
use strict; 			# All variables must be declared
use warnings; 	

# Declaration of a function: converting from hh::mm::ss,ms (e.g. 00:00:01,160) to seconds. 
sub RegionsToSec {
	my($time) = @_; #value sent in
	$time = reverse($time);
	my $n = 0;
	my $seconds = "";
	my $chrfin = "";
	# milliseconds:
	while ($n<3) {
		$n++;
		$chrfin = chop($time);
		$seconds = "$chrfin$seconds"; 
	}
	# seconds: replacing the full stop by a colon
	$chrfin = chop($time); 
	$seconds = ".$seconds"; 
	# then adding the 2 figures for seconds
	$chrfin = chop($time); 
	$seconds = "$chrfin$seconds"; 
	$chrfin = chop($time); 
	$seconds = "$chrfin$seconds"; 

	# minutes : 
	$chrfin = chop($time); 
	my $mn2 = chop($time);
	my $mn1 = chop($time);
	my $mn = "$mn1$mn2";
	# Conversion from minutes to seconds
	$mn = (60*$mn);

	# Hours: 
	$chrfin = chop($time); 
	my $h2 = chop($time);
	my $h1 = chop($time);
	my $h = "$h1$h2";
	# Conversion from hours to seconds
	$h = (3600*$h);
	# Sum
	$time = ($h + $mn + $seconds);
	# Returning this value
	return($time);
}

# Declaring variables

# my $vocinfile = 'E:\24_naxi\Yongning\F4_LD_AMA\F4_phonemes\crdo-NRU_F4_PalatalizedApicalized.txt'; 
my $vocinfile = 'C:\Documents and Settings\alexis\Mes documents\My Dropbox\na_W\Phonologie_Tonologie\crdo-NRU_F4_AccompPfv.txt';
my $regionsinfile = 'C:\Documents and Settings\alexis\Mes documents\My Dropbox\na_W\Phonologie_Tonologie\crdo-NRU_F4_AccompPfv_REGIONS.txt';
# my $regionsinfile = 'E:\24_naxi\Yongning\F4_LD_AMA\F4_phonemes\crdo-NRU_F4_PalatalizedApicalized_REGIONS.txt'; 

my $textname = my $line = ""; my $nbW = my $Wno = 0; my $nblines = 0; my $glosslineen = ""; my $ortholine = ""; my $glossline= ""; my $glosslinecn = "", my $note = ""; my $regionsline = ""; my $timebegin = ""; my $timeend = "";

open (VOC, "$vocinfile") or die "Can't open $vocinfile: $!";     # open input vocabulary file for reading
open (REGIONS, "$regionsinfile") or die "Can't open $regionsinfile: $!";     # open input time (regions) file for reading

# open (XOUT,">E:\\24_naxi\\Yongning\\F4_LD_AMA\\F4_phonemes\\crdo-NRU_F4_PalatalizedApicalized.xml");

open (XOUT, '>C:\Documents and Settings\alexis\Mes documents\My Dropbox\na_W\Phonologie_Tonologie\crdo-NRU_F4_AccompPfv.xml');


# Selecting whether there are Chinese translations (value: 1) or not (value: 0). 
my $transl_cn = 1;
# Selecting whether there are English translations (value: 1) or not (value: 0).
my $transl_en = 1;

# Reading first line of text, to serve as title.
$textname=<VOC>;
# Keeping count of the number of lines of text read, for ease of reference to input text file
$nblines = 1;
# Removing line break.
chomp ($textname);

# Reading first lines of Regions file: the first 4 lines are a header.
<REGIONS>;
<REGIONS>;
<REGIONS>;
<REGIONS>;

# Writing header of file. The information in the header allows the resulting file to be read locally for checking before it is placed online.
print XOUT "<?xml version=\"1.0\"  encoding=\"utf-8\"?>\n";
print XOUT "<?xml-stylesheet type=\"text/xsl\" href=\"showText3.xsl\"?>\n";
print XOUT "<WORDLIST id=\"crdo-NRU_$textname\" xml:lang=\"nru\">\n";
print XOUT "<url_sound>$textname.wav</url_sound>\n";
print XOUT "<HEADER>\n";
print XOUT "<TITLE xml:lang=\"fr\">$textname</TITLE>\n";
print XOUT "<SOUNDFILE href=\"$textname.wav\"/>\n";
print XOUT "</HEADER>\n";

# Treat vocab data. Count starts at 1.
while ($line=<VOC>) {
		# incrementing counter of lines read in source file
		$nblines++;		
		# incrementing counter of sentences in output file
		$nbW++;
		# formatting glossed-word count
		$Wno = sprintf ("%03u", $nbW);
		$ortholine=$line;		#IPA ("orthography")
		# removing end-of-line at end of input line
		chomp $ortholine;
		# replacing angle brackets < > by the corresponding XML formulas (otherwise they result in messy markup). Note: the g at the end of the expression tells Perl to replace globally (=as many times as there are occurrences of the pattern).
		$ortholine =~ s{<}{&lt;}g;
		$ortholine =~ s{>}{&gt;}g;

		# writing the word into the XML file
		print  XOUT "<S id=\"$textname", "_", "$Wno\">\n\t<FORM>$ortholine</FORM>\n";

		# Dealing with comments, if any	
		my $commentloop = 1;
		while ($commentloop == 1) {
			$glossline=<VOC>;	# French gloss. Also, the program must check whether there are comments.
			$nblines++;	
			my $testnotechr = substr($glossline,0,1);
			if ($testnotechr eq '%') {		 # Condition: if the first character is %.
				# Substracting the first character of that line: the %. This is done inelegantly.
				$note = reverse $glossline;
				chop $note;
				$note=reverse $note;
				# Also, any " symbol in the message must be replaced, otherwise it will count as end of message. The < > symbols must also be replaced.
				chomp ($note);
				$note =~ s{"}{'}g;
				$note =~ s{<}{&lt;}g;
				$note =~ s{>}{&gt;}g;
				# Writing the comment into the XML file. By default it is assumed that the comment is in French (for no better reason than because that is the language in which I write my comments). This can be changed below by changing fr to en or another language code.
				print  XOUT "\t<NOTE xml:lang=\"en\" message = \"$note\"/>\n"; # adding the note
			}
			else {
				$commentloop = 0;
			}
		}
		chomp $glossline;
		print  XOUT "\t<TRANSL xml:lang=\"fr\">$glossline</TRANSL>\n";
				
		# Chinese glosses: only if the variable was set accordingly.
		if ($transl_cn == 1) {
			$glosslinecn=<VOC>;# Chinese glosses
			$nblines++;		
			chomp $glosslinecn;
			print  XOUT "\t<TRANSL xml:lang=\"cn\">$glosslinecn</TRANSL>\n";
		}
		# English gloss: only if the $transl_cn variable was set to 1 above. 
		if ($transl_en == 1) {
			$glosslineen=<VOC>;# English glosses
			$nblines++;		
			chomp $glosslineen;
			print  XOUT "\t<TRANSL xml:lang=\"en\">$glosslineen</TRANSL>\n";
		}
		
		# Adding time alignment
		$regionsline = <REGIONS>;
		#Parsing from the end, and recovering two values. If parsing from beginning: problem with lines whose tags include spaces.
		$regionsline = reverse($regionsline);
		my @regions = split /\s+/, $regionsline;
		$timebegin = $regions[3];
		$timeend = $regions[2];
		
		# Calling function to convert times from Regions List format to seconds
		$timebegin = &RegionsToSec ($timebegin);
		$timeend = &RegionsToSec ($timeend);
		print XOUT "<AUDIO start=\"$timebegin\" end=\"$timeend\"\/>\n";

		# my $tps_en_sec = "$timebegin[6..7].$timebegin[9..11]";
		# print XOUT "temps en secondes avant ajout minutes et heures : $tps_en_sec\n";		

		# $tps_en_sec = $tps_en_sec + (60*$timebegin[4..5]);
		# $tps_en_sec = $tps_en_sec + (3600*$timebegin[1..2]);
		# print XOUT "$tps_en_sec\n";		
		
		# Adding markup for end of word	
		print XOUT "</S>\n";
		$nblines++;	
		
		# Reading extra line from input file, corresponding to empty line. (Addition made in Oct. 2011, to make it visually clearer: entries are separated by blank lines.)
		<VOC>
}
print XOUT "</TEXT>\n";
unlink ("foobar");

close (VOC);
close (REGIONS);
