#!/usr/bin/env python
# -*- coding: utf-8 -*-

from smbus import SMBus
from time import sleep
from WiiData import WiiData

class WiiNunchuck(object):
	"""
	Clase para leer los sensores y botones del Wii Nunchuck

	Inicializa y controla la lectura del Wii Nunchuck.
	Requiere del uso del puerto I2C, por lo que éste debió ser 
	previamente configurado ejecutando el script configuration.sh.

	Attributes:
		port_i2c: Número del puerto I2C. Para versiones de Raspberry Pi superiores 
			a la versión de 512M el número del puerto I2C es el 1.

		dir_i2c: Dirección I2C del dispositivo Wii Nunchuck. Por default es 0x52.
	"""

	# Usar el puerto I2C 1 para Raspberry Pi 512M
	port_i2c = 1

	# Dirección I2C del Wii Nunchuck
	dir_i2c = 0x52

	def __init__(self):
		""" Inicializa el Wii Nunchuck para que atienda solicitudes de lectura. """

		print "Inicializando Wii Nunchuck..."
		self.bus = SMBus(self.port_i2c)
		self.wii_init()

	def wii_init(self):
		""" Envía la secuencia de inicialización al Wii Nunchuck por I2C para que atienda solicitudes de lectura.
		En caso de no encontrar el dispositivo en la dirección 0x52, arroja una excepción. """

		try:
			# Secuencia para inicializar Nunckuck
			# Escribe el dato 0x00 en el registro 0x40
			self.bus.write_byte_data(self.dir_i2c, 0x40, 0x00)
			print "Inicializado con éxito."
		except Exception as e:
			print "Error Inicializando."
			print e

	def read_data(self):
		""" Lee los valores de los sensores y botones del Wii Nunchuck.
		En caso de no encontrar el dispositivo en la dirección 0x52, arroja una excepción. """
		
		self.wii_init()
		sleep(0.01)
		# Para leer del Nunchuck primero se debe enviar un comando 0x00
		# y después leer 6 bytes de información
		#
		# La información recibida debe ser decodificada realizando
		# XOR con 0x17 y después sumando 0x17
		try:	
			self.bus.write_byte(self.dir_i2c, 0x00)
			sleep(0.005)
			data_raw = [((self.bus.read_byte(self.dir_i2c) ^ 0x17) + 0x17) for i in xrange(6)]
			if data_raw[0] < 255:
				self.data = WiiData(data_raw)
		except Exception:
			pass

