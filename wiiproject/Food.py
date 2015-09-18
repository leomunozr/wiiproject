#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from Point import Point

class Food(object):
	"""
	Clase para crear un objeto de comida.

	Attributes:
		x: Posición horizontal de la comida en la matriz.
		y: Posición vertical de la comida en la matriz.
	"""

	def __init__(self):
		""" Crea comida en posición aleatoria
		Las coordenadas pueden variar de (0,0) a (7,7) """
		x = randint(0,7)
		y = randint(0,7)
		self.place = Point(x,y)
