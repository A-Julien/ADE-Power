#!/bin/bash
HTML_FILE="$(mktemp)"
COOKIES_FILE="$(mktemp)"
URI_origin='http://www-ade.iut2.upmf-grenoble.fr/ade/custom/modules/plannings/direct_planning.jsp?'

uri_login='login='
uri_pwd='password='
uri_project='projectId='
uri_rsc='resources='
uri_and='&'
uri_weeks='weeks=19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37'

LONGIN='WebINFO'
PW='MPINFO'

RESOURCESA2='483'
RESOURCESA1='482'
PROJECTID='15'

date
echo "----------------- Downloading ADE.html ------------------ "

#A1
echo "|---------------|"
echo "|projectId =  "$PROJECTID"|"
echo "|resources A1 = "$RESOURCESA1"|"
echo "|---------------|"

URIA1=$URI_origin$uri_login$LONGIN$uri_and$uri_pwd$PW$uri_and$uri_project$PROJECTID$uri_and$uri_weeks$uri_and$uri_rsc$RESOURCESA1
echo "Download in process from " $URIA1
wget -q --save-cookies $COOKIES_FILE --keep-session-cookies -O $HTML_FILE "$URIA1"
wget -q --load-cookies $COOKIES_FILE -O ./ade-a1.html "http://www-ade.iut2.upmf-grenoble.fr/ade/custom/modules/plannings/info.jsp"

#A2
echo "|---------------|"
echo "|projectId =  "$PROJECTID"|"
echo "|resources A2 = "$RESOURCESA2"|"
echo "|---------------|"


URIA2=$URI_origin$uri_login$LONGIN$uri_and$uri_pwd$PW$uri_and$uri_project$PROJECTID$uri_and$uri_weeks$uri_and$uri_rsc$RESOURCESA2

#echo $URI
echo "Download in process from " $URIA2
wget -q --save-cookies $COOKIES_FILE --keep-session-cookies -O $HTML_FILE "$URIA2" 
wget -q --load-cookies $COOKIES_FILE -O ./ade-a2.html "http://www-ade.iut2.upmf-grenoble.fr/ade/custom/modules/plannings/info.jsp"



echo "------ Converting ADE.html to utf-8 ------ "
# remplacement des caracteres speciaux problematiques

#A1
iconv -f Windows-1252 -t UTF-8 ./ade-a1.html > ./utf-a1.html 


sed -i 's/é/e/g' ./utf-a1.html
sed -i 's/è/e/g' ./utf-a1.html
sed -i 's/à/a/g' ./utf-a1.html
sed -i 's/fevr/feb/g' ./utf-a1.html
sed -i 's/mars/mar./g' ./utf-a1.html
sed -i 's/avr/apr/g' ./utf-a1.html
sed -i 's/mai/may./g' ./utf-a1.html
sed -i 's/janv/jan/g' ./utf-a1.html


#A2
iconv -f Windows-1252 -t UTF-8 ./ade-a2.html > ./utf-a2.html

sed -i 's/é/e/g' ./utf-a2.html
sed -i 's/è/e/g' ./utf-a2.html
sed -i 's/à/a/g' ./utf-a2.html
sed -i 's/janv/jan/g' ./utf-a2.html
sed -i 's/fevr/feb/g' ./utf-a2.html
sed -i 's/mars/mar./g' ./utf-a2.html
sed -i 's/avr/apr/g' ./utf-a2.html
sed -i 's/mai/may./g' ./utf-a2.html

echo "----------------- Parsing ------------------ "

/home/pi/adepower/parser.py utf-a1.html a1
#echo "Parsing a1 ok"

/home/pi/adepower/parser.py utf-a2.html a2
#echo "Parsing a2 ok"


echo "----------- Copy ON Web Server ------------- "
#A2
cp ./ade-a1.html /var/www/html/logade/html-a1.log
cp ./cal-a1.ical /var/www/html/
cp ./cal-a1.ical /var/www/html/cal-a1.ics

#A1
cp ./ade-a2.html /var/www/html/logade/html-a2.log
cp ./cal-a2.ical /var/www/html/
cp ./cal-a2.ical /var/www/html/cal-a2.ics


mv ade-a1.html ade-a2.html utf-a2.html utf-a1.html /var/log/ade

echo "Done"




#echo "BEGIN:VEVENT" >> ./cal.ical
#echo "DTSTART:20161201T050000Z" >> ./cal.ical
#echo "DTEND:20161201T053000Z" >> ./cal.ical
#echo "SUMMARY:ADEPower Debug Event" >> ./cal.ical
#echo "DESCRIPTION:" `date` >> ./cal.ical
#echo "END:VEVENT" >> ./cal.icalecho "END:VCALENDAR" >> ./cal.ical



