#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Point import Point
from random import randint

class Snake(object):
	"""
	Clase para representar la serpiente

	Controla el movimiento de la serpiente y la acción de comer para aumentar 
	de tamaño.

	Attributes:
		body: Arreglo de objetos Point para representar la posición del cuerpo.
		direction: String que indica la dirección del movimiento. 
			[UP | DOWN | RIGHT | LEFT]
	"""

	# Dirección inicial hacia donde se moverá.
	direction = "RIGHT"

	def __init__(self, length):
		""" Dibuja una serpiente de longitud length.

		Args:
			length: número entero mayor a 0 y menor a 8. """

		# Se crea un arreglo de puntos, empezando de (0,0),
		# luego se invierte para que la cabeza corresponda al ultimo punto
		self.body = list(reversed([Point(i, 0) for i in xrange(length)]))

	def move(self, direction):
		""" Mueve un paso el cuerpo de la serpiente hacia la dirección que apunte.

		Args:
			direction: string [UP | DOWN | RIGHT | LEFT]

		Returns:
			String con el valor del sentido en el que se avanzó. """

		# Evita que regrese por donde vino
		if (
			(self.direction == 'UP' and direction == 'DOWN') or
			(self.direction == 'DOWN' and direction == 'UP') or
			(self.direction == 'RIGHT' and direction == 'LEFT') or
			(self.direction == 'LEFT' and direction == 'RIGHT')
			):
			new_head = self.forward(self.direction);

		else:
			new_head = self.forward(direction)
			self.direction = direction

		# Aparece del otro lado de la pantalla
		if new_head.x > 7: new_head.x = 0
		if new_head.x < 0: new_head.x = 7
		if new_head.y > 7: new_head.y = 0
		if new_head.y < 0: new_head.y = 7
				
		self.body.insert(0, new_head)
		self.body.pop()

		# Regresa el sentido al que se avanzó
		return self.direction

	def  forward(self, direction):
		""" Calcula y regresa la nueva posición de la cabeza a partir de 
		la dirección del movimiento.

		Args:
			direction: string [UP | DOWN | RIGHT | LEFT] 

		Returns:
			Un objeto Point con las coordenadas resultantes de avanzar 
			en el sentido de la dirección."""

		directions = {
			'UP': Point(self.body[0].x, self.body[0].y + 1),
			'DOWN': Point(self.body[0].x, self.body[0].y - 1),
			'RIGHT': Point(self.body[0].x + 1, self.body[0].y),
			'LEFT':  Point(self.body[0].x - 1, self.body[0].y)
		}
		return directions[direction]

	def eat(self):
		""" Agrega un nuevo punto al final del cuerpo de la serpiente. """
		self.body.append(self.body[-1])

	def show(self):
		""" Muestra en pantalla las coordenadas de cada punto del cuerpo.
		(Usado para debug) """
		for i, point in enumerate(self.body):
			print ("{} - x:{} y:{}".format(i, point.x, point.y))

