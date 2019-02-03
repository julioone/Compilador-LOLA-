

from sly import Lexer

class Lolalexer(Lexer):
	fileName=""

	reserved_words = { 'BEGIN',
	 'CONST',
	  'END', 'IN', 'INOUT', 'MODULE',
	   'OUT', 'REG', 'TS', 'OC', 'BIT',
	    'TYPE', 'VAR', 'DIV', 'MOD', 'MUX',
		 'LATCH', 'SR', 'IF', 'THEN', 'ELSE','ELSIF', 'FOR', 'DO', 'POS'}#, 'WHILE', 'RETURN'

	tokens = {
		'ID', 'INTEGER', 'LOGICVALUE',
		'DOSPUNTOSIGUAL', 'MENORIGUAL', 'MAYORIGUAL', 'DOBLEPUNTO', 'FLECHAARRIBA',
		*reserved_words,
	}
	ignore = ' \t'


	literals = { '+', '-', '*', '/', '=', '^', '~', '&', '|', '#', '<', '>', '(', ')', '[', ']', '{', '}', '.', ',', ';', ':' , "'", '!'}

	@_(r"[a-zA-Z][a-zA-Z0-9]*'?")
	def ID(self, t):

		if t.value.upper() in self.reserved_words:
			t.type = t.value.upper()
		return t

	@_(r'\d+')#expresión regular que trabaja [0-9]
	def INTEGER(self, t):
		t.value = int(t.value)
		return t

	@_(r"'[0-1]")
	def LOGICVALUE(self, t):
		t.value = bool(int(t.value[1]))
		return t

	#Tokens - simbolos compuestos, operadores
	DOBLEPUNTO = r'\.\.'#r'[.][.]'
	#FLECHADERECHA = r'->'
	MAYORIGUAL = r'>='
	MENORIGUAL = r'<='
	DOSPUNTOSIGUAL = r'\:\='
	FLECHAARRIBA=r'↑'

	@_(r'\n+')
	def ignore_NEWLINE(self, t):
		self.lineno += t.value.count('\n')

	#r'\(\*([^*)]|\*[^*]\).*)*\*\)' expresion mejorada
	ignore_COMMENT=r'\(\*([^*]|\*[^)])*\*\)'#\(\*[^*)\n]*\*\) sin saltos de linea, anterior \(\*[^*)]*\*\),

	#error control (\(\*([^*]|\*[^)])*)|(.*\*\))
	@_(r'\(\*([^*]|\*[^)])*')
	def error_COMMENTRIGTH(self, t):
		print('File "{}" Line {} Colum {}'.format(self.fileName, t.lineno, self.getColumn(t)))
		print(t.value)
		print("ERROR - No terminó comentario")
		print("Se esperaba un *)")

	@_(r'(?!.*\(\*).*\*\)')
	def error_COMMENTLEFT(self, t):
		print('File "{}" Line {} Colum {}'.format(self.fileName, t.lineno, self.getColumn(t)))
		print(t.value)
		print("ERROR - No terminó comentario")
		print("Se esperaba un (*")

	def error(self, value):
		print("Illegal character {}".format(value[0]))
		self.index += 1

	#metodos funcionales
	# Compute column.
	#     input is the input text string
	#     token is a token instance

	def getColumn(self, token):
		last_cr = self.text.rfind('\n', 0, token.index)+1
		#print("last_cr {}".format(last_cr))#verificando valor de indexados previos
		if last_cr < 0:
			last_cr = 0
		column = (token.index - last_cr) + 1
		return column

if __name__ == '__main__':
	import sys
	lexer = Lolalexer()
	if(len(sys.argv)!=2):
		sys.stderr.write('Usage: "{}" "filename"\n'.format(sys.argv[0]))
		raise SystemExit(1)
	file= open(sys.argv[1]).read()
	maxLenthLine=0
	for linea in open(sys.argv[1]):
		if(maxLenthLine<len(linea)):
			maxLenthLine=len(linea)#verifica la columna maxima para el formato de centrado (visual en los print)
			print("malen",maxLenthLine)
	print("{:{align}{width}}".format("Archivo recibido - contenido inicio", align="^", width=maxLenthLine))
	print("-"*maxLenthLine)
	print(file)
	print("-"*maxLenthLine)
	print("{:{align}{width}}".format("Archivo recibido - contenido fin", align="^", width=maxLenthLine))

	#print("aplicando tokenize")
	lexer.fileName=sys.argv[1]
	for tok in lexer.tokenize(file):
		print("Linea {}, columna {}, indexado {}".format(tok.lineno, lexer.getColumn(tok), tok.index))
		print('tipo {} valor {}'.format(tok.type, tok.value))
