#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Point(object):
	"""
	Clase para representar un punto en la matriz

	Attributes:
		x: Coordenada horizontal del punto
		y: Coordenada vertical del punto
	"""

	def __init__(self, x, y):
		""" Crea un objeto Punto con coordenadas x y y.

		Args:
			x: numero entero mayor a 0.
			y: numero entero mayor a 0. """
		self.x = x
		self.y = y
