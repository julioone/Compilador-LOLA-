# gotype.py
# coding: utf-8
'''
Sistema de Tipos de mini Go
===========================
Este archivo define las clases de representación de tipos.  Esta es una
clase general usada para representar todos los tipos.  Cada tipo es
entonces una instancia singleton de la clase tipo.


El contendo de la clase tipo es enteramente suya.  Sin embargo, será
mínimamente necesario el codificar cierta información sobre:

        a.  Que operaciones son soportadas (+, -, *, etc.).
        b.  El tipo resultante de cada operación
        c.  Valores por defecto para las instancias nuevas de cada tipo
        d.  Métodos para chequeo-tipo de operadores binarios y unarios
        e.  Mantener un registro de tipos (pe. 'int', 'float') para las
            instancias (pe. 'int_type', 'float_type', 'string_type', etc.)

Una vez que se haya definido los tipos incorporado, se deberá segurar
que sean registrados en la tabla de símbolos o código que compruebe
los nombres de tipo en 'gocheck.py'.
'''

class LolaType(object):

	def __init__(self, name, binop , unop):
		self.name = name
		self.binop = binop
		self.unop = unop
Logic_Type = LolaType('LogicValue',
					('+', '-', '*',),
					('~'))

Integer_Type = LolaType('Integer',
					   ('+', '-', '*', '/', 'DIV', 'MOD'),
					   ('↑'))
