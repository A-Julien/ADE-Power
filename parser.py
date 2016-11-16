#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-


from	bs4			import	BeautifulSoup
from	datetime	import	*					# gestion des dates


#------ Definition des variables ------#
MIN_activity		=	2

ical_date_start		=	"DTSTART:"
ical_date_end		=	"DTEND:"
ical_title			=	"SUMMARY:"
ical_location		=	"LOCATION:"
ical_description	=	"DESCRIPTION:"


cours_1h			=	["S2107 - Ex supp","S1106 - TDPP dec","RI visite universite Quebec a Chicoutimi","S1101 - AA","S1101 - TP"]
cours_1h30			=	["S1102 - EXAMEN","S1103 - TDMP","S1102 - Examen machine","S1103 - TP","S2105 - TDMP dec","S1107 B - TDMP sx dec","S1103 - AA","S1102 - TDMP 2","S1102 - TDMP",
						"S1102 - TD ATER","S1101 - TDMP","S1102 - TD ATER 2","S1104 - TDMP", "S1202 - TDMP"]
cours_2h 			=	["S1104 - EXAMEN","S1101-EX","S1107 A - TDMP SX","S1201 - TDMP","S2105 - AA","S1107 B - TDMPdec","S1105 - AA","S1107 A - TDMP","S2105 - TDMP sx dec","S1105 - TDMP",
						"S1106 - TP dec","S2107 - TDMP","S2107 - TDMP SX","S1205 - TD 2","S1204 - TD 2",
						"S1107 B - TDMP DEC","S1102 - AA","S1201 - TD 2",
						"S2107 - TDMP sx","S1101 - Anglais-1","S1104 - TDMP - SX", "S2107 - Ex", "S1203 - TDMP"]
cours_3h 			=	["S1201 - TD 2"]
#---------------------------------------#


#------ Ouverture des fichiers --------#
soup 		=	BeautifulSoup(open("/home/pi/public/V2/adePower/utf.html"), "lxml")		# ouvrir le fichier ade.html
calendar	= 	open("/home/pi/public/V2/adePower/cal.ical", "w")						# creer et écrire dans le fichier cal.ical
#--------------------------------------#



# --- Gestion des dates --- #

def jour_semaine(jour_entree):			# indique le nombre de jours qu'il faut ajouter au début de la semaine
	if 		jour_entree == "Lundi":	
		entier = 0
	elif 	jour_entree == "Mardi":
		entier = 1
	elif	jour_entree == "Mercredi":
		entier = 2
	elif 	jour_entree	== "Jeudi":
		entier = 3
	elif	jour_entree == "Vendredi":
		entier = 4
	else:
		entier = 5 
	return entier

def date_debut(date_entree, jour_entree):	# renvoie la date de début d'événement formatée ical	
	delta				=	jour_semaine(jour_entree)
	date_entree			=	datetime.strptime(date_entree, '%d %b. %Y%Hh%M') + timedelta(days=delta, hours=-1)
	event_date_start 	=	date_entree.strftime('%Y%m%dT%H%M%SZ')
	return event_date_start


def duree_cours(code_cours):				# renvoie la durée du cours en fonction de son code
	if 		code_cours in cours_1h 		:
		delta	= 	1
	elif 	code_cours in cours_1h30	:
		delta 	= 	1.5
	elif 	code_cours in cours_2h		:
		delta 	= 	2
	else								:
		print "Le code cours " + code_cours + " n'est pas dans une liste de cours!"
		delta = 1
		
	return delta

def date_fin(date_entree, code_cours, jour_entree):		# renvoie la date de fin de cours en fonction du code cours
	duree				=	duree_cours				(	code_cours						)
	delta				=	jour_semaine			(	jour_entree						)
	date_entree 		=	datetime.strptime		(	date_entree, 	'%d %b. %Y%Hh%M')
	date_fin 			=	date_entree + timedelta	(days=delta,		hours=duree-1	)
	event_date_end 		=	date_fin.strftime		(	'%Y%m%dT%H%M%SZ'				)
	return event_date_end

# --- Fin gestion des dates ---------------------- #







activity	=	soup.find_all('tr')								# recherche chaque ligne du tableau

calendar.write("BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//adePower/airCstnr//ADETOICAL v1.0//FR\n") # introduction du fichier ical

#print activity

for i in range(MIN_activity, len(activity)):

	attribut = activity[i].find_all('td')					# séparation de chaque ligne du tableau

	calendar.write("BEGIN:VEVENT\n")					# début d'un événement ical


	event_location				= 	attribut[8].string
	event_description_ID		=	attribut[0].string
	event_description_group		=	attribut[6].string
	event_date_start			=	date_debut(attribut[1].string+attribut[3].string, 
									attribut[2].string)
	event_date_end				=	date_fin(attribut[1].string+attribut[3].string, 
									event_description_ID, attribut[2].string)

	try:
		event_description_prof	=	attribut[7].string
	except:
		event_description_prof	= 	None
	try:
		event_title				=	attribut[5].string
	except:
		event_title				= 	None


	calendar.write(	ical_date_start		+	event_date_start		+	'\n')
	calendar.write(	ical_date_end		+	event_date_end			+	'\n')
	try:
		calendar.write(	ical_location		+	event_location		+	'\n')
	except:
		calendar.write(	ical_location		+	'Pas de salle'		+	'\n')
	calendar.write(	ical_description	+	event_description_ID	+	'\\n')
	if event_description_prof!=None:
		calendar.write(	"Prof : "		+	event_description_prof	+	'\\n')
	calendar.write(	"Groupe : "			+	event_description_group	+	'\\n')
	calendar.write(	"Exporté le : "		+	str(datetime.today())		+ 	'\n')

	try:
		calendar.write(	ical_title		+	event_title				+	'\n')
	except:
		calendar.write(	ical_title		+	'Sans titre'			+	'\n')

	


	calendar.write("END:VEVENT\n")

#calendar.write("END:VCALENDAR\n")

print ("ICAL file correctly exported !")






# ---- Fermeture des fichiers --- #
calendar.close()
# -------------------------------
