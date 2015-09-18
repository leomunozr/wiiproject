#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Programa principal Snake.

Para salir, presionar botón C del Wii Nunchuck.
"""

from threading import Thread
from time import sleep
from WiiNunchuck import WiiNunchuck
from Snake import Snake
from Food import Food
from Display import Display

class Program(object):
	""" TODO: Mejorar el tiempo de refresco de pantalla """


	# Condición que un hilo debe revisar para terminar su ejecución
	keep_playing = True

	def __init__(self):
		""" Inicialización del juego. """

		self.wii = WiiNunchuck()
		self.snake = Snake(3)
		self.display = Display()
		self.direction = self.snake.direction
		self.food = None

	def read_control(self):
		""" Mientras el juego siga activo, lee el control de Wii y mueve 
		la serpiente o termina el juego. """

		while (self.keep_playing):
			self.wii.read_data()
			self.change_direction()

			if self.wii.data.button_c is True:
				print "Boton C"
				self.game_over(None)

			sleep(0.01)

	def change_direction(self):
		""" Interpreta la dirección del joystick para cambiar la dirección 
		en la que avanza la serpiente. """

		if self.wii.data.joystick_y < 70: #Down arrow
			self.direction = "DOWN"
		elif self.wii.data.joystick_y > 180: #Up arrow
			self.direction = "UP"
		if self.wii.data.joystick_x < 70: #Up arrow
			self.direction = "LEFT"
		elif self.wii.data.joystick_x > 180: #Up arrow
			self.direction = "RIGHT"
	    
	def update_snake(self):
		""" Mientras el juego siga activo, actualiza la posición de la serpiente
		moviéndola hacia adelante cada 0.2 seg y verifica colisiones."""

		while(self.keep_playing):
			self.snake.move(self.direction)
			self.check_collisions()
			sleep(0.2)
		
	def check_collisions(self):
		""" Revisar si la cabeza de la serpiente colisionó con el resto 
		del cuerpo o con comida """

		for p in self.snake.body[2:]:
			if (
				self.snake.body[0].x == p.x and
				self.snake.body[0].y == p.y
				):
				self.game_over(-1)
			if self.food is not None:
				if (
					self.snake.body[0].x == self.food.place.x and
					self.snake.body[0].y == self.food.place.y
					):
					self.snake.eat()
					self.food = None

	def make_food(self):
		""" Mientras el juego siga activo, actualiza la posición del objeto 
		de comida cada 3 seg. """

		while(self.keep_playing):
			self.food = Food()
			sleep(3)

	def update_screen(self):
		""" Mientras el juego siga activo, refresca la pantalla con la posición 
		de la serpiente y de la comida """

		while(self.keep_playing):
			array_points = list(self.snake.body)
			if self.food is not None:
				array_points.append(self.food.place)
			self.display.show(array_points)

	def game_over(self, end_code):
		""" Controla cómo terminará el juego.
		Al perder, espera 3 seg y luego saldrá.

		Args:
			end_code: Un número entero negativo usado para saber
				por qué terminó el juego.
		"""

		if end_code is -1:
			print "You lost."
		print "End of game!"
		self.keep_playing = False
		sleep(3)

	
if __name__ == '__main__':
	# Main function
	program = Program()
	hilos = []
	hilos.append( Thread(target = program.read_control) )
	hilos.append( Thread(target = program.update_snake) )
	hilos.append( Thread(target = program.make_food) )
	hilos.append( Thread(target = program.update_screen) )

	for h in hilos:
		h.daemon = True
		h.start()

	# El hilo 0 espera hasta que se de la señal de salida
	hilos[0].join()
	program.display.clean_screen()
