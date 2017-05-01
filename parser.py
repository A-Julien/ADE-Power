#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-


from	bs4			import	BeautifulSoup
from	datetime	import	*					# gestion des dates
import sys

utf = sys.argv[1]
gr = sys.argv[2]

#------ Definition des variables ------#
MIN_activity		=	2

ical_date_start		=	"DTSTART:"
ical_date_end		=	"DTEND:"
ical_title			=	"SUMMARY:"
ical_location		=	"LOCATION:"
ical_description	=	"DESCRIPTION:"

#------ Ouverture des fichiers --------#
try:
	soup 		=	BeautifulSoup(open(utf), "lxml")		# ouvrir le fichier ade.html
except :
	print ("BeautifulSoup can't open "+utf)

try:
	calendar	= 	open("./cal-"+gr+".ical", "w") # creer et écrire dans le fichier cal.ical
except:
	print ("BeautifulSoup can't open/create cal-"+gr+".ical")

try:
	cours_unknown = open("/home/pi/ADE-Power/cours/cours_unknown.txt", 'r+')
	with open("/home/pi/ADE-Power/cours/cours_1h.txt") as f:
	    cours_1h = f.read().splitlines() 
	with open("/home/pi/ADE-Power/cours/cours_1h30.txt") as f:
	    cours_1h30 = f.read().splitlines() 
	with open("/home/pi/ADE-Power/cours/cours_2h.txt") as f:
	    cours_2h = f.read().splitlines() 
	with open("/home/pi/ADE-Power/cours/cours_3h.txt") as f:
	     cours_3h = f.read().splitlines() 
except:
	print("can't open folders")

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
	date_entree			=	datetime.strptime(date_entree, '%d %b. %Y%Hh%M') + timedelta(days=delta, hours=-2)
	event_date_start 	=	date_entree.strftime('%Y%m%dT%H%M%SZ')
	return event_date_start


def duree_cours(code_cours):				# renvoie la durée du cours en fonction de son code
	if 		code_cours in cours_1h 		:
		delta	= 	1
	elif 	code_cours in cours_1h30	:
		delta 	= 	1.5
	elif 	code_cours in cours_2h		:
		delta 	= 	2
	elif    code_cours in cours_3h      :
                delta   =       3
	elif    code_cours  + "\n" in cours_unknown :
		print "!!!!!!!!le cours est deja inconu"
		delta = 2
	else					:
		print "Le code cours " + code_cours + " n'est pas dans une liste de cours, on le rajoute !"
		cours_unknown.write(code_cours + "\n")
		delta = 2
		

	return delta

def date_fin(date_entree, code_cours, jour_entree):		# renvoie la date de fin de cours en fonction du code cours
	duree				=	duree_cours				(	code_cours						)
	delta				=	jour_semaine			(	jour_entree						)
	date_entree 		=	datetime.strptime		(	date_entree, 	'%d %b. %Y%Hh%M')
	date_fin 			=	date_entree + timedelta	(	days=delta,		hours=duree-2	)
	event_date_end 		=	date_fin.strftime		(	'%Y%m%dT%H%M%SZ'				)
	return event_date_end

# --- Fin gestion des dates ---------------------- #







activity	=	soup.find_all('tr')								# recherche chaque ligne du tableau

calendar.write("BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//adePower//ADETOICAL v2.1//FR\n") # introduction du fichier ical

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

calendar.write("END:VCALENDAR")
print ("ICAL file correctly exported !")
print ("parsing " + gr + " ok")





# ---- Fermeture des fichiers --- #
calendar.close()
cours_unknown.close()
# -------------------------------
