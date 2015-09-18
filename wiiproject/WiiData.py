#!/usr/bin/env python
# -*- coding: utf-8 -*-

class WiiData(object):
	"""
	Clase envoltorio para los datos leídos del Wii Nunchuck

	Envoltorio que representa los datos del Wii Nunchuck

	Attributes:
		joystick_x: Movimiento horizontal del joystick. Número entero de 0 a 255.
		joystick_y: Movimiento vertical del joystick. Número entero de 0 a 255.
		button_c: Botón C presionado. 0: no presionado, 1: presionado.
		button_z: Botón Z presionado. 0: no presionado, 1: presionado.
		raw: Datos en "crudo". Arreglo de 6 valores: 
			[ joystick_x, joystick_y, acc_x, acc_y, acc_z, buttons ]

	(En la práctica, los valores del joystick en los límites nunca llegan a ser 0 ó 255.)
	"""

	#Valores en posición central y botones no presionados
	joystick_x = None
	joystick_y = None
	button_c = None
	button_z = None

	def __init__(self, data):
		""" Inicializa las propiedades de la clase según una cadena de datos en "crudo" 

		Args:
			data: Arreglo de datos en crudo: 
				[ joystick_x, joystick_y, acc_x, acc_y, acc_z, buttons ]"""

		self.raw = data
		self.joystick_x = data[0]
		self.joystick_y = data[1]
		self.button_c = not bool(data[5] & 0x02)
		self.button_z = not bool(data[5] & 0x01)
		self.z_axis = data[4]

	def show_data(self):
		""" Muestra en pantalla los valores de las propiedades.
		(Usada para debugging.) """

		print ('Joystick X: {}\n'
			'Joystick Y: {}\n'
			'Button C: {}\n'
			'Button Z: {}\n'
			'Z axis: {}').format(self.joystick_x, self.joystick_y, 
				self.button_c, self.button_z, self.z_axis)
	
	def show_raw_data(self):
		""" Muestra en pantalla el arreglo de los valores en "crudo".
		(Usada para debugging.) """

		print self.raw
