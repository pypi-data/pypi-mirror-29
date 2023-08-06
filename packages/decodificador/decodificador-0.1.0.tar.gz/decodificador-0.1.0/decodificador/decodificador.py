# -*- coding: utf-8 -*-

"""Main module."""

def ascii_deco(vector):
	cadena=vector.split(',')
	suma=" "
	for i in range (len (cadena)):
		ascci=int(cadena[i])
		caracter=chr(ascci)
		suma=suma+caracter
	print (suma)
