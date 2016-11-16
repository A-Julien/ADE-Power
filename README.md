# ADE-Power

<center> 
	![ade logo](http://adepower.ddns.net/Ade-power.PNG)
</center> 
##Intro
Ade-Power is a converter from ***ADE expert*** calandar to ical and ics format. Coding with ***python 2.7*** .

## 1 - Get Table in BASH SCRIPT

#### Specification :
*	1. Execute "chmod 700 ade-dl.sh"
*	2. You need to change few things :
	* ```URI_origin='yourURLadelogin'```	
	* ```uri_weeks='weeks=thenbofweeks, thenbofweeks, thenbofweeks,etc..'```
	* ```LONGIN='youradelogin'```
	* ```PW='youradepassword'```
	* ```RESOURCES='youraderesource'```
	* ```PROJECTID='youradeprojectid'```
	
###  /!\ You need to change all /YOURPATH/  /!\

## 2 - Parse Html with Beautiful Soup in PYTHON
#### You need install Beautiful Soup with pip :
 ```pip install beautifulsoup4```

## 3 - Automate the converter

To automate the converter you can use crontab :
```sudo crontab -e```

and write :
```*/2 * * * * sudo /YOURPATH/ade-dl.sh > /var/log/ade/ade.log 2>&1```
This ligne execute the converter every two minutes.

You can use a cron generator : <http://www.crontab-generator.org>

## 4 - Export .ical to your own calandar

Use the lastligne of ```ade-dl.sh``` to copie the files to your web server.
