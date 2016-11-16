#!/bin/bash
HTML_FILE="$(mktemp)"
COOKIES_FILE="$(mktemp)"
URI_origin='http://www-ade.iut2.upmf-grenoble.fr/ade/custom/modules/plannings/direct_planning.jsp?'

uri_login='login='
uri_pwd='password='
uri_project='projectId='
uri_rsc='resources='
uri_and='&'
uri_weeks='weeks=12,13,14,15,16,17'
#weeks='10,11,12,13,14,15,16,17,18,19,20'
#uri_weeks = $uri_weeks$weeks

LONGIN='WebINFO'
PW='MPINFO'

RESOURCES='483'
PROJECTID='15'

date
echo "----------------- Downloading ADE.html ------------------ "

echo "|---------------|"
echo "|projectId =  "$PROJECTID"|"
echo "|resources = "$RESOURCES"|"
echo "|---------------|"


URI=$URI_origin$uri_login$LONGIN$uri_and$uri_pwd$PW$uri_and$uri_project$PROJECTID$uri_and$uri_weeks$uri_and$uri_rsc$RESOURCES

#echo $URI
echo "Download in process from " $URI
wget -q --save-cookies $COOKIES_FILE --keep-session-cookies -O $HTML_FILE "$URI" 
wget -q --load-cookies $COOKIES_FILE -O /home/pi/public/V2/adePower/ade.html "http://www-ade.iut2.upmf-grenoble.fr/ade/custom/modules/plannings/info.jsp"

echo "----------------- Converting ADE.html to UTF-8 ----------------- "

iconv -f Windows-1252 -t UTF-8 /home/pi/public/V2/adePower/ade.html > /home/pi/public/V2/adePower/utf.html

#yes, it's mess, but it's work dude !!
sed -i 's/é/e/g' /home/pi/public/V2/adePower/utf.html
sed -i 's/è/e/g' /home/pi/public/V2/adePower/utf.html
sed -i 's/à/a/g' /home/pi/public/V2/adePower/utf.html
sed -i 's/janv/jan/g' /home/pi/public/V2/adePower/utf.html

echo "----------------- ADE.html converted UTF-8 ----------------- "

echo "----------------- HEY ! WE'RE MAKING THE SOUP ------------------ "
echo "Keep calm and wait for ade"
/home/pi/public/V2/adePower/parser.py

echo "BEGIN:VEVENT" >> /home/pi/public/V2/adePower/cal.ical
echo "DTSTART:20161201T050000Z" >> /home/pi/public/V2/adePower/cal.ical
echo "DTEND:20161201T053000Z" >> /home/pi/public/V2/adePower/cal.ical
echo "SUMMARY:ADEPower Debug Event" >> /home/pi/public/V2/adePower/cal.ical
echo "DESCRIPTION:" `date` >> /home/pi/public/V2/adePower/cal.ical
echo "END:VEVENT" >> /home/pi/public/V2/adePower/cal.ical
echo "END:VCALENDAR" >> /home/pi/public/V2/adePower/cal.ical


cp /home/pi/public/V2/adePower/ade.html /var/www/html/html.log
cp /home/pi/public/V2/adePower/cal.ical /var/www/html/
cp /var/www/html/cal.ical /var/www/html/cal.ics
echo "--------------------- Done dude ! -------------------- "
