#!/usr/bin/perl

use URI;
use Web::Scraper::LibXML;
use Encode;
use Data::Dumper;
use XML::LibXML;
use LWP::Simple qw($ua head);
use DateTime;

my $first_url = "https://br.answers.yahoo.com/question/index?qid=20150405131318AA7bENi";

my $yahoo_prefixe = "https://br.answers.yahoo.com";

my @user_list;
my @list_of_urls;
my @urls_bkp;
my $folder = "";

#file to hold the backuplist with profils urls
open my $bkp_list, '>>', $folder."profil_bkp_list.txt";

#create log_file
open my $log, '>>', $folder."log.txt";


@user_list = CreateNewXMLFile($first_url,1,0);

while (2==2){
	
	#prepare to write the log
	my $dt = DateTime->now;
	
	if (open $log, '>>', $folder."log.txt"){
	
	foreach $user_item (@user_list){
				
		#writing log
		print $log "# start scrape user's profile ".$yahoo_prefixe.$user_item." ".$dt->hms." ".$dt->ymd."\n";
		
		my @list_of_urls;
		if(defined $user_item){
			@list_of_urls = ScrapeUsersProfil($user_item);			
		}		
		
		my $array_size = @list_of_urls;
		
		#writing log
		print $log "* scraping done - list of urls - ".$array_size." items-".$dt->hms." ".$dt->ymd."\n" or last;
				
		if(@list_of_urls){
			
			foreach $url (@list_of_urls){
				
				if(defined $url){
					
					#if check varial is set 0, the url hasn`t been crawled
					my $check_url = 0;
					my $line="";
					#verify if the url hasn`t been already crawled 
					open (IN, $folder."url_list.txt");	  	
 					while ($line = <IN>) {
 						chomp($line);
 						#if url is on the url list, set check_url to 1	 	
	  					if($line eq $yahoo_prefixe.$url){
	  						$check_url = 1;
	  					}	  					
 					}
	 				
	 				#if check_url is set 0, the url hasn`t been crawled, so we call CreateNewXMLFile()
	 				if($check_url == 0){	 					
	 					@urls_bkp = CreateNewXMLFile($yahoo_prefixe.$url,1,0);			
						#chek if the array is not empty obs->[Use of defined on aggregates (hashes and arrays) is deprecated];
	 				} else {
	 					next;
	 				}				
				}		
					
				
				if (@urls_bkp){	
								
					#file to hold the backuplist with profils urls
					open my $bkp_list, '>>', $folder."profil_bkp_list.txt" or last;
							
					#writing log
					print $log "# saving backup list".$dt->hms." ".$dt->ymd."\n";
										
					#saving urls in the backup list								
					foreach $url_bkp (@urls_bkp){
						
						#verify if the url is not empty
						if(defined $url_bkp){
																			
							print $bkp_list $url_bkp."\n";								
						}													
					}
					close($bkp_list);					
				} 		
			}		
		}
		(shift @user_list);		
	}
		
	close($log);	
	ReadBackupList();
	print "READING BACKUP LIST \n";
	my $dt = DateTime->now;
	print $dt->hms." ".$dt->ymd."\n";
				
	
	};		
}

#### relançar o programa aqui!!!!!

#======================================== SUBROUTINES =============================================
#              HERE WE CAN FIND ALL THE METHODS USED BY THE PROGRAM
#
#==================================================================================================

#================================== CreateNewXMLFile() =================================================
#                THIS METHODE EXECUTES ALL THE TASKS TO SCRAPE THE PAGE WITH THE QUESTIONS 
#	CreateNewXMLFile([url],[count_page],[check_scrape_question]) --- RETURN @user_list OR undef
#
#	this method takes 3 arguments: 
#   [url] - to be scraped. it passed to method ScrapePage() 
#	[count_page] - controls the number questions pages scraped.  it's passed to ScrapePage()
#	[check_scrape_question] - check if question tags has already been scrape. it's passed to ScrapePage()

sub CreateNewXMLFile{

#url with a page of questions to be scraped.
my $url = $_[0];

#check if the $url exists before start. it returns 1 in the end
if (head($url)) {
	
	my @user_list;
	
	#variable to hold the xml sctructure returned from ScrapePage()
	my $doc; 
	
	#controls the number questions pages scraped.
	my $count_page=$_[1];
	
	#check if the question has already been scrape. if $done == 1 (true), the program doesnt scraped the question.
	my $question_scraped_done = $_[2];
		
	#extract question id from the url to create the xml name file
	$url =~ /[=]([a-z\d]+)/ig;
	my $xml_file = $1;
	
	#output parameters to create the xml file
	open my $out, '>', $folder.$xml_file.".xml"  or return;
	
	#create list of url crawled
	open my $url_list, '>>', "url_list.txt" or return;
	print $url_list $url."\n";
	
	#writing log
	my $dt = DateTime->now;
	open $log, '>>', $folder."log.txt" or return;
	print $log "# writing file ".$xml_file.".xml ".$dt->hms." ".$dt->ymd."\n";
	close($log);
		
	#call subroutine to scrape the page
	($doc, @user_list) = ScrapePage($url,$question_scraped_done,$count_page);
	
	if(defined $doc) {
		#save the xml structure in a file
		print $out $doc;
		close($out);
	}
	
	my $array_size = @user_list - 2;
	
	#writing log
	my $dt = DateTime->now;
	open $log, '>>', $folder."log.txt" or return;
	print $log "# ".$xml_file.".xml done - user's list - ".$array_size."items".$dt->hms." ".$dt->ymd."\n";
	close($log);
	
	#eliminate the first url which doesn't contain a valid adress!
	(shift @user_list);
	return @user_list;
		
} else {
	
	return;
}	

}
#================================ END CreateNewXMLFile() ====================================



#================================== ScrapePages() =================================================
#                THIS METHODE EXECUTES ALL THE TASKS TO SCRAPE THE PAGE WITH THE QUESTIONS 
# ScrapePage([url],[check_scrape_questio],[count_page]) --- RETURN $doc, @user_list OR undef
#
# This subroutine takes 3 arguments: 
# [url] - to be scraped. it passed to method ScrapePage() 	
# [check_scrape_question] - check if question tags has already been scrape. [1 true, 0 false]
# [count_page] - controls the number questions pages scraped.

sub ScrapePage {
	# to be scraped		
	my $url_questions = $_[0];
	
	#check it the next page exists	
	if (head($url_questions)) {
		
		#array to hold the users' urls
		my @user_list;		
		
		#check if question tags has already been scrape. If it's 0, the questions' tags are scraped
		my $question_scraped_done = $_[1];
		
		#controls the number questions pages scraped.
		my $count_page=$_[2];		
		
		my ($doc, $root);			
		
		#create the xml sctructure
		$doc = XML::LibXML::Document->new('1.0', 'utf-8');
	
		#create root tag for xml file
		$root = $doc->createElement("thread");
		
		#prepare to write the log
		my $dt = DateTime->now;
			
		#writing log
		print $log "** Scrape started ".$dt->hms." ".$dt->ymd."\n";
			
		#check the url to verify if the question information has already been scraped, if $question_scraped_done is 0, the block is executed
		if (!($question_scraped_done == 1)){
			
			#parameters to scrape questions
			my $question = scraper {
			    process '//*[@class="Fz-24 Fw-300 Mb-10"]', question => 'TEXT';
			    process '//span[@class="ya-q-text"]', continuation => 'TEXT';    
			    process '//*[@class="profileImage Wpx-45 Hpx-45 Bdrs-25 Bdx-1g"]/@alt', nom_question => 'TEXT';
			    process '//*[@class="profileImage Wpx-45 Hpx-45 Bdrs-25 Bdx-1g"]/@data-id', ID => 'TEXT';
			    process '//*[@class="Clr-88"]', date => 'TEXT';
			  	process '//*[@class="Clr-b"]', theme => 'TEXT';			  	
			};
			
			
		#writing log
		print $log "** Scrape done ".$dt->hms." ".$dt->ymd."\n";
						
			#scrape answers
			my $question_scraped = $question->scrape(URI->new($url_questions)) or return;
						
			#convert $question_scraped into an hash
			my %question_info = %{$question_scraped};
			
			#declare variables to hold questions' information
			my ($enonce_question, $continuation, $nom_question, $id_question, $date, $themes);
			
			#reading questions' information from the hash
			$enonce_question = $question_info{'question'};
			$continuation = $question_info{'continuation'};
			$nom_question = $question_info{'nom_question'};
			$id_question = $question_info{'ID'};
			$date = $question_info{'date'};
			$themes = $question_info{'theme'};
			
			push(@user_list, "/question/index?qid=".$id_question);							
								
								
			#create tag question
			my $question_tag = $doc->createElement('question');
			$question_tag->setAttribute('date'=> $date);
			$question_tag->setAttribute('url'=>$url_questions);
			$question_tag->appendTextNode($enonce_question);
			
						
			#create tag the 'nom'
			my $nom_tag = $doc->createElement('nom');
			
			#appending information to 'nom'
			$nom_tag->appendTextNode($nom_question);
			$nom_tag->setAttribute('id'=>"/question/index?qid=".$id_question);		
			
			my $theme_tag = $doc->createElement('theme');
			
			$theme_tag->appendTextNode($themes);
			$question_tag->appendChild($theme_tag);	
			
			#append tag question
			$root->appendChild($question_tag);				
		
		#end question scrape	
		}
				
		
		#varibles used to scrape the answers pages
		my ($reponses, $answers_scraped);
		
		#parameters to scrape answers.
		$reponses = scraper {
			#scrape to verify pages
		    process '//*[@class="Pstart-75 Bgc-w Lh-16 Bdstart-1g Bdend-1g Py-20"]/a[@aria-pressed="true"]/div', page => 'TEXT';  
    		process '//*[@data-ya-type="answer"]', 'reponse[]' => scraper{
		    process '//*[@class="uname Clr-b"]', nom => 'TEXT';
		    process '//*[@class="ya-q-full-text"]', contribution => 'TEXT';
		    process '//*[@class="uname Clr-b"]/@href', ID => 'TEXT';
		    process '//*[@class="Clr-88"]', date => 'TEXT';			    
		    }     
		 };
	
		#scrape answers
		$answers_scraped = $reponses->scrape(URI->new($url_questions)) or return;
			
		#convert $answers_scraped into an hash
		my %answers_info = %{$answers_scraped};
		
		
		my $check_page = "";
		
		#this variable is used to verify if we are not scraping twice the same page
		$check_page = $answers_info{page};
		
		#reading answers' information
		my @tableau_des_donnees = @{$answers_info{'reponse'}};
		
		my $reponses_tag = $doc->createElement('reponses');
		
		if(defined $_[3]){
			#using 'reponses' passed in the cases where the method is called recursively			
			$reponses_tag = $_[3];
		}
		
		
		
		my $reponse_tag = $doc->createElement('reponse');	
		
		#variables to hold hmtl scraped data of answers
		my ($nom, $date, $contribution, $id_question);
					
		foreach my $val (@tableau_des_donnees) {
		
			$nom = Encode::encode("utf8", $val->{nom});				
			$date = Encode::encode("utf8", $val->{date});
			$contribution = Encode::encode("utf8", $val->{contribution});
			$id_question = Encode::encode("utf8", $val->{ID});
			push(@user_list, $id_question);		
		
						
			#create tag the 'nom'
			my $nom_tag = $doc->createElement('nom');
			
			#appending information to 'nom'
			$nom_tag->appendTextNode($nom);
			$nom_tag->setAttribute('id'=>$id_question);
			
			#appending 'nom' to 'reponse'
			$reponse_tag->appendChild($nom_tag);
			
			#create tag 'contribution'	
			my $contribution_tag = $doc->createElement('constribution');
			$contribution_tag->appendTextNode($contribution);
			$contribution_tag->setAttribute('date'=>$date);
			
			#appending 'contribution' to 'reponse'
			$reponse_tag->appendChild($contribution_tag);	
			$reponses_tag->appendChild($reponse_tag);										
		}		
		
			
		#time to sleep
		sleep(10);
			
		my $next_page;		
						
		#verify there are more answers to the same question
		while (($count_page eq $check_page) && !($check_page eq "")){
			
			#insert the url to have '&page= at the end
			if($count_page == 1){
				$count_page++;
				$next_page = $url_questions."&page=".$count_page;
				ScrapePage($next_page,1,$count_page,$reponses_tag);
			} else {					
				#$next_page = $url_questions =~ s/page=\d*/page=$count_page/g;
				my @personal = split(/page=/, $url_questions);
				$count_page++;
				my $new_url = $personal[0]."page=".$count_page;
								
				ScrapePage($new_url,1,$count_page,$reponses_tag);
									
			}
			
		}
		
		$root->appendChild($reponses_tag);
		#assembly the xml document	
		$doc->setDocumentElement($root);		
				
		#url exists scraped without erros					
		return ($doc, @user_list);
	
	} else {
		#return 0, if the url doesn't exist
		return;
	}		

}
#==============================END ScrapePage() ===============================================



#================================== ScrapeUsersProfil() =================================================
#                THIS SUBROUTINE SCRAPES THE USER'S PROFILE TO GET ANSWERS AND QUESTION CREATED BY THE USER  
# ScrapeUsersProfil([USER_ID])
#
# This subroutine takes 1 argument: 
# [USER_ID] - the variable with the user's ID to build the url profile	
# 

sub ScrapeUsersProfil{
	
	#create user's profile with the ID argument
	my $users_question_url =$yahoo_prefixe.$_[0];
		
	my @questions_urls = ScrapeUsers_A_Q($users_question_url,0);
	my @answers_urls = ScrapeUsers_A_Q($users_question_url,1);
	
	#array to hold urls
	my @all_urls;
	
	if(@questions_urls){
		#assembling ulrs in on list
		foreach $item(@questions_urls){
		
			push(@all_urls, $item);
			
		}
	}
		
	if(@answers_urls){
		#assembling ulrs in on list
		foreach $item(@answers_urls){
		
			push(@all_urls, $item);
		}		
	}		
	
			
	if(@all_urls){
				
		return @all_urls;	
					
	} else {
		
		return;
	}
	
}

#================================== ScrapeUsers_A_Q() =================================================
#                THIS SUBROUTINE SCRAPES THE ANSWERS OR QUESTION SECTIONS ACCORDING WITH THE OPTION PASSED BY SECOND ARGUMENT
# ScrapeUsers_A_Q([URL],[OPTION_A_Q]) -- RETURN--> @list_of_urls OR undef
#
# This subroutine takes 2 arguments: 
# [URL] - url to be scraped
# [OPTION_A_Q] - option with we want scrap the answers 1, or the questioins 0.	
#
# it returns an array with questions URLs
#
sub ScrapeUsers_A_Q{			
	
	my $users_profile = $_[0];
	
	my $scrape_answers = $_[1];
	
	if($scrape_answers == 1){
		#adjust url to get the profile with user's answers
		$user_profile = s/questions\?show/answers\?show/;
	 }
			
	#check it the next page exists	
	if (head($users_profile)) {
			
		#parameters to scrape questions.
		my $user_questions = scraper {	  		
			process '//*[@data-ylk="slk:qtitle"]/@href', 'user_questions[]' => 'TEXT';
		 };         
			
		#scrape profile
		my $user_questions_scraped = $user_questions->scrape(URI->new($users_profile)) or return;
		
		#convertion data to put it in an array
		my %url_question = %{$user_questions_scraped};
		my @list_of_urls = @{$url_question{user_questions}};
				
		return @list_of_urls;
		
	} else {
		
		return;
		
	}
	
}

#================================== ReadBackupList() =================================================
#                THIS SUBROUTINE READS THE BACKULIST AND CREATES A NEW ONE EMPTY
# ReadBackupList()
#

sub ReadBackupList{
	  	open (IN, $folder."profil_bkp_list.txt");
	  	
 		while ($line = <IN>) {
	 	
	  		push (@user_list, $line);
	  		  		  	
	  	}
	  	chomp(@user_list);
	  	close(IN);
	  	
	  	#creating log
		my $dt = DateTime->now;
		open $log, '>>', $folder."log.txt";
		print $log "### reading backup list ".$dt->hms." ".$dt->ymd."\n";
	  	close($log);
	  		  	
  		#create a new backup list empty
		open my $new_bkp_list, '>', $folder."profil_bkp_list.txt";
		print $new_bkp_list "";
		close($new_bkp_list);
}

