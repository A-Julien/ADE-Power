#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import sys

try:
	cours_unknown= open("./cours/cours_unknown.txt"	,"r")
	cours_1h 	= open("./cours/cours_1h.txt"		,"a")
	cours_1h30 	= open("./cours/cours_1h30.txt"		,"a")
	cours_2h 	= open("./cours/cours_2h.txt"		,"a")
	cours_3h 	= open("./cours/cours_3h.txt"		,"a")
except:
	print("can't open folders")

list = cours_unknown.readlines()

def is_int(x):
  try:
    int(x)
    return True
  except ValueError:
    return False


print ("Ajout de cours dans la base de donnee")
print (" 1-> 1 heure \n 13 -> 1h30 \n 2-> 2h \n 3–> 3h")

for cours in list: 
	choix = 4

	while  is_int(choix) == False or choix > 3:
		try:
			choix = input("le cour " + cours + "fais ? : ")
		except:
			print "/!\ entre un int /!\ "
			
		if choix == 1:
			try:
				cours_1h.write(cours)
			except:
				print "can't save " + cours + "in cours_1h"

		if choix == 13:
			try:
				cours_1h30.write(cours)
			except:
				print "can't save " + cours + "in cours_1h30"

		if choix == 2:
			try:
				cours_2h.write(cours)
			except:
				print "can't save " + cours + "in cours_2h"

		if choix == 3:
			try:
				cours_3h.write(cours) 
			except:
				print "can't save " + cours + "in cours_3h"
		if choix == 0:
			sys.exit(1)
try:	
	cours_1h.close()
	cours_1h30.close()
	cours_2h.close()
	cours_3h.close()
	cours_unknown.close()
except:
	print "can't close folder"
