#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Clase para controlar una matriz de leds de 8x8.

Controla la visualización de coordenadas (representadas por objetos Point) en una matriz de leds de 8x8.
Implementa un registro de corrimientos 74HC595 para el control individual de cada led en la matriz.
El registro de corrimientos A controla las columnas y el registro B controla los renglones.
Ambos registros son controlados por 3 GPIO c/u en la Raspberry Pi. Éstos son:
SER - A: Pin 11, B: Pin 12.
SRCLK - A: Pin 13, B: Pin 16.
RCLK - A: Pin15, B: Pin 18.
El registro A tiene también:
SRCLR - Pin 7.
"""

import os
import RPi.GPIO as GPIO
from Point import Point
from random import randint
from time import sleep

# Control del registro de corrimiento para los cátodos de la matriz de leds (Registro A)
SER = 11 # Dato de entrada para el siguiente desplazamiento
SRCLK = 13 # Reloj serial. Desplaza los datos en flanco alto
RCLK = 15 # Reloj del registro. Muestra el contenido del registro en flanco alto 
SRCLR = 7 # Bit de reset en flanco bajoo

# Control del registro de corrimiento para los ánodos de la matriz de leds (Registro B)
SER2 = 12
SRCLK2 = 16
RCLK2 = 18

def wait_ns(nanoseconds):
	""" Pone en espera el hilo por los nanosegundos indicados. 

	Args:
		nanoseconds: número decimal positivo de nanosegundos a esperar
	"""
	sleep(miliseconds / 1000000000.0)

class Display(object):
	NUM_COLS = 8
	NUM_ROWS = 8

	def __init__(self):
		""" Inicialización de los registros de salida en la Raspberry Pi. """
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(SER, GPIO.OUT)
		GPIO.setup(SRCLK, GPIO.OUT)
		GPIO.setup(RCLK, GPIO.OUT)
		GPIO.setup(SER2, GPIO.OUT)
		GPIO.setup(SRCLK2, GPIO.OUT)
		GPIO.setup(RCLK2, GPIO.OUT)
		GPIO.setup(SRCLR, GPIO.OUT)
		print "Display inicializado"

	def show(self, array_points):
		""" Muestra en el display un arreglo de puntos.

		Args:
			array_points: arreglo de coordenadas representadas por un objeto Point. """

		# Convierte de arreglo de Point a arreglo de bits
		bits_matrix = self.points_to_bits(array_points)

		# Envía los bits a la matriz de leds
		self.matrix_driver(bits_matrix)

	def points_to_bits(self, array_points):
		""" Método que traduce las coordenadas de un objeto Punto
		a un arreglo de bits (estados on/off) para usar en la matriz de leds.

		Args:
			array_points: arreglo de coordenadas representadas por un objeto Point. 

		Returns:
			Un arreglo de renglones correspondientes a cada renglón de leds en
			la matriz de leds, que a su vez es un arreglo de estados (0:off, 1:on)
			de cada led	en el renglón."""

		# Ordena las columnas
		bits_matrix = []
		for i in xrange(0, self.NUM_COLS):
			# Selecciona sólo las coordenadas que pertenezcan a la misma columna (coord y)
			col_points = filter(lambda p:p.y == i, array_points)

			# Crea una nueva lista sólo con los renglones (coord x) de cada columna
			coord_x = set(map(lambda r:r.x, col_points))

			# Crea un renglón de ceros
			row_bits = [0 for i in xrange(0,8)]

			# Prende los bits necesarios
			for bit in coord_x:
				row_bits[bit] = 1

			bits_matrix.append(row_bits)

		return bits_matrix

	def matrix_driver(self, bits_matrix):
		""" Muestra en la matriz de leds el arreglo de bits.

		Args:
			bits_matrix: arreglo multidimensional de enteros 0 ó 1.
				El primer nivel del arreglo representa los renglones de la matriz,
				y el segundo nivel el estado de los leds (on/off). """

		GPIO.output(RCLK2, GPIO.LOW)
		GPIO.output(SRCLK2, GPIO.LOW)
		GPIO.output(SER2,GPIO.LOW)
		wait_ns(100)

		# Cuando SERCLK pase a estado alto, el registro se desplaza a la derecha
		# y entra como nuevo dato el valor del pin SER.
		# Para mostrar los cambios RCLK debe pasar a estado alto.
		for row in bits_matrix:
			# Deshabilita las salidas del registro A
			GPIO.output(RCLK, GPIO.LOW)
			GPIO.output(SRCLK, GPIO.LOW)
			wait_ns(100)
			GPIO.output(SRCLR, GPIO.HIGH)

			# Llena el registro A con los valores del renglon
			for bit in row:
				GPIO.output(SER, bit);
				wait_ns(10)
				GPIO.output(SRCLK, GPIO.HIGH)
				wait_ns(10)
				GPIO.output(SRCLK, GPIO.LOW)
				wait_ns(10)

			# Habilita las salidas del registro A
			GPIO.output(RCLK, GPIO.HIGH)
			wait_ns(100)
			# Limpia el registro A
			GPIO.output(SRCLR, GPIO.LOW)

			# Borra la salida 
			GPIO.output(RCLK, GPIO.LOW)
			wait_ns(100)	
			GPIO.output(RCLK, GPIO.HIGH)

			GPIO.output(SRCLK2, GPIO.HIGH)
			wait_ns(100)
			GPIO.output(SRCLK2, GPIO.LOW)
			wait_ns(100)
			GPIO.output(RCLK2, GPIO.HIGH)
			wait_ns(100)

			# Avanza al siguiente renglon
			GPIO.output(SER2, GPIO.HIGH)
			wait_ns(100)
			GPIO.output(RCLK2, GPIO.LOW)
			wait_ns(100)
			
	def  clean_screen(self):
		""" Limpia la configuración de los GPIO de la Raspberry Pi."""
		GPIO.cleanup()
		print "GPIO cleared"

