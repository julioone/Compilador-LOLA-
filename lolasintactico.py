from sly import Parser
from lolalex import Lolalexer
from lolaast import *
from loladot import *
from lolacode import *
from lolacheck import *
class LolaParser(Parser):
	debugfile='parser.out'#control de depuración
	tokens = Lolalexer.tokens
	start = 'modulo'

	def __init__(self):
		self.errorStatus=False




	@_('tipoBasico')
	def tipoSimple(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoSimpleBasico(p.tipoBasico)#valor constante

	@_('ID "(" listaExpresiones ")"')
	def tipoSimple(self, p):
		if(self.errorStatus):
			return
		else:
			node=TipoSimpleIDListaExpresion(p.ID, p.listaExpresiones)
			node.lineno=p.lineno
			return node

	@_('ID')
	def tipoSimple(self, p):
		if(self.errorStatus):
			return
		else:
			node=TipoSimpleID(p.ID)
			node.lineno=p.lineno
			return node

	'''
	tipoBasico : 'BIT'
		| 'TS'
		| 'OC'
		;
	'''
	@_('BIT',
	'TS',
	'OC')
	def tipoBasico(self, p):
		if(self.errorStatus):
			return
		else:
			return p[0]#valor constante

	'''
	listaExpresiones : listaExpresiones "," expresion
		| expresion
		;
	'''
	@_('listaExpresiones "," expresion')
	def listaExpresiones(self, p):
		if(self.errorStatus or p.listaExpresiones is None):
			return
		else:
			p.listaExpresiones.append(p.expresion)
			return p.listaExpresiones

	@_('expresion')
	def listaExpresiones(self, p):
		if(self.errorStatus):
			return
		else:
			return ListaExpresiones([p.expresion])

	'''
	tipo : tipoExpresiones tipoSimple
	;
	'''
	@_('tipoExpresiones tipoSimple')
	def tipo(self, p):
		if(self.errorStatus):
			return
		else:
			return Tipo(p.tipoExpresiones, p.tipoSimple)

	'''
	tipoExpresiones : tipoExpresionesR
	|	empty
	;
	'''
	@_('tipoExpresionesR')
	def tipoExpresiones(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoExpresiones(p.tipoExpresionesR)

	@_('empty')
	def tipoExpresiones(self, p):
		return None

	'''
	tipoExpresionesR : tipoExpresionesR "[" expresion "]"
	|	"[" expresion "]"
	;
	'''
	@_('tipoExpresionesR "[" expresion "]"')
	def tipoExpresionesR(self, p):
		if(self.errorStatus or p.tipoExpresionesR is None):
			return
		else:
			p.tipoExpresionesR.append(p.expresion)
			return p.tipoExpresionesR

	@_('"[" expresion "]"')
	def tipoExpresionesR(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoExpresionesR([p.expresion])

	'''
	declaracionConstante : ID DOSPUNTOSIGUAL expresion ";"'
	;
	'''
	@_('ID DOSPUNTOSIGUAL expresion ";"')
	def declaracionConstante(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionConstante(p.ID, p.expresion)

	'''
	declaracionVariable : listaId ":" tipo ";"
	;
	'''
	@_('listaId ":" tipo ";"')
	def declaracionVariable(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionVariable(p.listaId, p.tipo)

	'''
	listaId : listaId "," ID
		|	ID
		;
	'''
	@_('listaId "," ID')
	def listaId(self, p):
		if(self.errorStatus or p.listaId is None):
			return
		else:
			p.listaId.append(p.ID)
			return p.listaId

	@_('ID')
	def listaId(self, p):
		if(self.errorStatus):
			return
		else:
			return ListaId([p.ID])

	'''
	selector : selectorR
	|	empty
	;
	'''

	@_('selectorR')
	def selector(self, p):
		if(self.errorStatus):
			return
		else:
			return Selector(p.selectorR)

	@_('empty')
	def selector(self, p):
		return None

	'''
	selectoR : selectorR selectorRR
	|	selectorRR
	;
	'''
	@_('selectorR selectorRR')
	def selectorR(self, p):
		if(self.errorStatus or p.selectorR is None):
			return
		else:
			p.selectorR.append(p.selectorRR)
			return p.selectorR

	@_('selectorRR')
	def selectorR(self, p):
		if(self.errorStatus):
			return
		else:
			return SelectorR([p.selectorRR])

	'''
	selectorRR : "." ID
	|	"." INTEGER
	|	"[" expresion "]"
	;
	'''
	@_('"." ID')
	def selectorRR(self, p):
		if(self.errorStatus):
			return
		else:
			return SelectorRR(p[1], None, None)

	@_('"." INTEGER')
	def selectorRR(self, p):
		if(self.errorStatus):
			return
		else:
			return SelectorRR(None, p[1], None)

	@_('"[" expresion "]"')
	def selectorRR(self, p):
		if(self.errorStatus):
			return
		else:
			return SelectorRR(None, None, p[1])


	@_('ID selector')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorSelector(p.ID, p.selector)


	@_('LOGICVALUE')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorValor(p.LOGICVALUE)

	@_('INTEGER')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorValor(p.INTEGER)

	@_('FLECHAARRIBA factor')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorSimbolo(p.FLECHAARRIBA, p.factor)

	@_('"~" factor')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorSimbolo(p[0], p.factor)

	@_('"(" expresion ")"')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorDeclaracion((p[0], p[2]), [p.expresion])

	@_('MUX "(" expresion ":" expresion "," expresion ")"')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorDeclaracion(p.MUX, [p.expresion0, p.expresion1, p.expresion2])

	@_('MUX "(" expresion "," expresion ":" expresion "," expresion "," expresion "," expresion ")"')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorDeclaracion(p.MUX, [p.expresion0, p.expresion1, p.expresion2, p.expresion3, p.expresion4, p.expresion5])

	@_('REG "(" expresion ")"')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorDeclaracion(p.REG, [p.expresion])

	@_('REG "(" expresion "," expresion ")"')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorDeclaracion(p.MUX, [p.expresion0, p.expresion1])

	@_('LATCH "(" expresion "," expresion ")"')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorDeclaracion(p.LATCH, [p.expresion0, p.expresion1])

	@_('SR "(" expresion , expresion ")"')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorDeclaracion(p.SR, p.expresion0, p.expresion1)

	'''
	termino : termino simbolosProd factor
	|	factor
	;
	'''
	@_('termino "*" factor', 'termino "/" factor', 'termino DIV factor', 'termino MOD factor')
	def termino(self, p):
		if(self.errorStatus or p.termino is None):
			return
		else:
			p[0].append(p[1], p[2])
			return p[0]

	@_('factor')
	def termino(self, p):
		if(self.errorStatus):
			return
		else:
			return Termino([None],[p.factor])



	'''
	expresion : expresion "+" termino
	|	expresion "-" termino
	|	termino
	;
	'''
	@_('expresion "+" termino',
	'expresion "-" termino')
	def expresion(self, p):
		if(self.errorStatus or p[0] is None):
			return
		else:
			p[0].append(p[1], p[2])
			return p[0]

	@_('termino')
	def expresion(self, p):
		if(self.errorStatus):
			return
		else:
			return Expresion([None], [p.termino])

	'''
	asignacion : ID selector DOSPUNTOSIGUAL expresion
	|	ID selector DOSPUNTOSIGUAL condicion "|" expresion
	;
	'''
	@_('ID selector DOSPUNTOSIGUAL expresion')
	def asignacion(self, p):
		if(self.errorStatus):
			return
		else:
			return Asignacion(p.ID, p.selector, p.expresion)

	@_('ID selector DOSPUNTOSIGUAL condicion "|" expresion')
	def asignacion(self, p):
		if(self.errorStatus):
			return
		else:
			return AsignacionCondicion(p.ID, p.selector, p.condicion, p.expresion)

	'''
	condicion : expresion
	;
	'''
	@_('expresion')
	def condicion(self, p):
		if(self.errorStatus):
			return
		else:
			return Condicion(p.expresion)

	'''
	relacion : expresion "=" expresion
	|	expresion "#" expresion
	|	expresion "<" expresion
	|	expresion MENORIGUAL expresion
	|	expresion ">" expresion
	|	expresion MAYORIGUAL expresion
	;
	'''
	@_('expresion "=" expresion',
	'expresion "#" expresion',
	'expresion "<" expresion',
	'expresion MENORIGUAL expresion',
	'expresion ">" expresion',
	'expresion MAYORIGUAL expresion')
	def relacion(self, p):
		if(self.errorStatus):
			return
		else:
			return Relacion(p[0], p[1], p[2])

	'''
	sentenciaSi : "IF" relacion "THEN" sentenciaSecuencia sentenciaSiSino sentenciaSiEntonces "END"
	;
	'''
	@_('IF relacion THEN sentenciaSecuencia sentenciaSiSino sentenciaSiEntonces END')
	def sentenciaSi(self, p):
		if(self.errorStatus):
			return
		else:
			return SentenciaSi(p.relacion, p.sentenciaSecuencia, p.sentenciaSiSino, p.sentenciaSiEntonces)

	'''
	sentenciaSiSino : sentenciaSiSinoR
	|	empty
	;
	'''
	@_('sentenciaSiSinoR')
	def sentenciaSiSino(self, p):
		if(self.errorStatus):
			return
		else:
			return SentenciaSiSino(p.sentenciaSiSinoR)

	@_('empty')
	def sentenciaSiSino(self, p):
		return None

	'''
	sentenciaSiSinoR : sentenciaSiSinoR "ELSIF" relacion "THEN" sentenciaSecuencia
	|	"ELSIF" relacion "THEN" sentenciaSecuencia
	;
	'''

	@_('sentenciaSiSinoR ELSIF relacion THEN sentenciaSecuencia')
	def sentenciaSiSinoR(self, p):
		if(self.errorStatus or p.sentenciaSiSinoR):
			return
		else:
			p.sentenciaSiSinoR.append(p.relacion, p.sentenciaSecuencia)
			return p.sentenciaSiSinoR

	@_('ELSIF relacion THEN sentenciaSecuencia')
	def sentenciaSiSinoR(self, p):
		if(self.errorStatus):
			return
		else:
			return SentenciaSiSinoR([p.relacion], [p.sentenciaSecuencia])

	'''
	sentenciaSiEntonces : "ELSE" sentenciaSecuencia
	|	empty
	;
	'''
	@_('ELSE sentenciaSecuencia')
	def sentenciaSiEntonces(self, p):
		if(self.errorStatus):
			return
		else:
			return SentenciaSiEntonces(p.sentenciaSecuencia)

	@_('empty')
	def sentenciaSiEntonces(self, p):
		return None

	'''
	sentenciaPara : "FOR" ID ":=" expresion DOBLEPUNTO expresion "DO" sentenciaSecuencia "END"
	;
	'''
	@_('FOR ID DOSPUNTOSIGUAL expresion DOBLEPUNTO expresion DO sentenciaSecuencia END')
	def sentenciaPara(self, p):
		if(self.errorStatus):
			return
		else:
			return SentenciaPara(p.ID, p.expresion0, p.expresion1, p.sentenciaSecuencia)

	'''
	sentencia : asignacion
	|	asignacionUnidad
	|	sentenciaSi
	|	sentenciaPara
	|	empty
	;
	'''
	@_('asignacion',
	'asignacionUnidad',
	'sentenciaSi',
	'sentenciaPara')
	def sentencia(self, p):
		if(self.errorStatus):
			return
		else:
			return Sentencia(p[0])

	@_('empty')
	def sentencia(self, p):
		return None

	'''
	sentenciaSecuencia : sentenciaSecuencia ";" sentencia
	|	sentencia
	;
	'''
	@_('sentenciaSecuencia ";" sentencia')
	def sentenciaSecuencia(self, p):
		if(self.errorStatus or p.sentenciaSecuencia is None):
			return
		else:
			p.sentenciaSecuencia.append(p.sentencia)
			return p.sentenciaSecuencia

	@_('sentencia')
	def sentenciaSecuencia(self, p):
		if(self.errorStatus):
			return
		else:
			return SentenciaSecuencia([p.sentencia])


	@_('MODULE ID ";" declaracionTipoPuntoComa declaracionConstanteCONST declaracionVariableIN declaracionVariableINOUT declaracionVariableOUT declaracionVariableVAR declaracionRelacionPOS sentenciaSecuenciaBEGIN END ID "."')
	def modulo(self, p):
		if(p.ID0!=p.ID1):
			print("error al definir modulo, no concuerda el ID {} {} con {} {} - Linea {}".format(p.MODULE, p.ID0, p.END, p.ID1, p.lineno))
			self.errorStatus=True
		elif(self.errorStatus):
			return
		else:
			return Modulo(p.ID0, p.declaracionTipoPuntoComa, p.declaracionConstanteCONST, p.declaracionVariableIN, p.declaracionVariableINOUT, p.declaracionVariableOUT, p.declaracionVariableVAR, p.declaracionRelacionPOS, p.sentenciaSecuenciaBEGIN, p.ID1)

	'''
	declaracionTipoPuntoComa : declaracionTipoPuntoComaR
	|	empty
	;
	'''
	@_('declaracionTipoPuntoComaR')
	def declaracionTipoPuntoComa(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionTipoPuntoComa(p.declaracionTipoPuntoComaR)

	@_('empty')
	def declaracionTipoPuntoComa(self, p):
		return None
	'''
	declaracionTipoPuntoComaR : declaracionTipoPuntoComaR declaracionTipo ";"
	|	declaracionTipo ";"
	;
	'''
	@_('declaracionTipoPuntoComaR declaracionTipo ";"')
	def declaracionTipoPuntoComaR(self, p):
		if(self.errorStatus or p.declaracionTipoPuntoComaR is None):
			return
		else:
			p.declaracionTipoPuntoComaR.append(p.declaracionTipo)
			return p.declaracionTipoPuntoComaR

	@_('declaracionTipo ";"')
	def declaracionTipoPuntoComaR(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionTipoPuntoComaR([p.declaracionTipo])

	'''
	declaracionConstanteCONST : "CONST" declaracionConstanteRecursivo
	|	empty
	;
	'''
	@_('CONST declaracionConstanteRecursivo')
	def declaracionConstanteCONST(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionConstanteCONST(p.declaracionConstanteRecursivo)

	@_('empty')
	def declaracionConstanteCONST(self, p):
		return None
	'''
	declaracionConstanteRecursivo : declaracionConstanteRecursivoR
	|	empty
	;
	'''
	@_('declaracionConstanteRecursivoR')
	def declaracionConstanteRecursivo(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionConstanteRecursivo(p.declaracionConstanteRecursivoR)

	@_('empty')
	def declaracionConstanteRecursivo(self, p):
		return None

	'''
	declaracionConstanteRecursivoR : declaracionConstanteRecursivoR declaracionConstante
	|	declaracionConstante
	;
	'''
	@_('declaracionConstanteRecursivoR declaracionConstante')
	def declaracionConstanteRecursivoR(self, p):
		if(self.errorStatus or p.declaracionConstanteRecursivoR is None):
			return
		else:
			p.declaracionConstanteRecursivoR.append(p.declaracionConstante)
			return p.declaracionConstanteRecursivoR

	@_('declaracionConstante')
	def declaracionConstanteRecursivoR(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionConstanteRecursivoR([p.declaracionConstante])

	'''
	declaracionVariableIN : "IN" declaracionVariableRecursivo
	|	empty
	;
	'''
	@_('IN declaracionVariableRecursivo')
	def declaracionVariableIN(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionVariableIN(p.declaracionVariableRecursivo)

	@_('empty')
	def declaracionVariableIN(self, p):
		return None


	'''
	declaracionVariableRecursivo : declaracionVariableRecursivoR
	|	empty
	;
	'''
	@_('declaracionVariableRecursivoR')
	def declaracionVariableRecursivo(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionVariableRecursivo(p.declaracionVariableRecursivoR)

	@_('empty')
	def declaracionVariableRecursivo(self, p):
		return None

	'''
	declaracionVariableRecursivoR : declaracionVariableRecursivoR declaracionVariable
	|	declaracionVariable
	;
	'''
	@_('declaracionVariableRecursivoR declaracionVariable')
	def declaracionVariableRecursivoR(self, p):
		if(self.errorStatus or p.declaracionVariableRecursivoR is None):
			return
		else:
			p.declaracionVariableRecursivoR.append(p.declaracionVariable)
			return p.declaracionVariableRecursivoR

	@_('declaracionVariable')
	def declaracionVariableRecursivoR(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionVariableRecursivoR([p.declaracionVariable])

	'''
	declaracionVariableINOUT : "INOUT" declaracionVariableRecursivo
	|	empty
	;
	'''
	@_('INOUT declaracionVariableRecursivo')
	def declaracionVariableINOUT(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionVariableINOUT(p.declaracionVariableRecursivo)

	@_('empty')
	def declaracionVariableINOUT(self, p):
		return None

	'''
	declaracionVariableOUT : "OUT" declaracionVariableRecursivo
	|	empty
	;
	'''
	@_('OUT declaracionVariableRecursivo')
	def declaracionVariableOUT(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionVariableOUT(p.declaracionVariableRecursivo)

	@_('empty')
	def declaracionVariableOUT(self, p):
		return None

	'''
	declaracionVariableVAR : "VAR" declaracionVariableRecursivo
	|	empty
	;
	'''
	@_('VAR declaracionVariableRecursivo')
	def declaracionVariableVAR(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionVariableVAR(p.declaracionVariableRecursivo)

	@_('empty')
	def declaracionVariableVAR(self, p):
		return None

	'''
	declaracionVariblePOS : POS declaracionRelacionRecursivo
	|	empty
	;
	'''
	@_('POS declaracionRelacionRecursivo')
	def declaracionRelacionPOS(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionRelacionPOS(p.declaracionRelacionRecursivo)

	@_('empty')
	def declaracionRelacionPOS(self, p):
		return None

	'''
	declaracionRelacionRecursivo :declaracionRelacionR
	|	empty
	;
	'''
	@_('declaracionRelacionR')
	def declaracionRelacionRecursivo(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionRelacionRecursivo(p.declaracionRelacionR)

	@_('empty')
	def declaracionRelacionRecursivo(self, p):
		return None

	'''
	declaracionRelacionR : declaracionRelacionR relacion ";"
	|	relacion ";"
	;
	'''

	@_('declaracionRelacionR relacion ";"')
	def declaracionRelacionR(self, p):
		if(self.errorStatus or p.declaracionRelacionR is None):
			return
		else:
			p.declaracionRelacionR.append(p.relacion)
			return p.declaracionRelacionR

	@_('relacion ";"')
	def declaracionRelacionR(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionRelacionR([p.relacion])


	'''
	sentenciaSecuenciaBEGIN : "BEGIN" sentenciaSecuencia
	|	empty
	;
	'''
	@_('BEGIN sentenciaSecuencia')
	def sentenciaSecuenciaBEGIN(self, p):
		if(self.errorStatus):
			return
		else:
			return SentenciaSecuenciaBEGIN(p.sentenciaSecuencia)

	@_('empty')
	def sentenciaSecuenciaBEGIN(self, p):
		return None

	'''
	tipoFormal : expresionCorcheteO "BIT"
	;
	'''
	@_('expresionCorcheteO BIT')
	def tipoFormal(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormal(p.expresionCorcheteO)

	'''
	expresionCorcheteO : expresionCorcheteOR
	|	empty
	;
	'''
	@_('expresionCorcheteOR')
	def expresionCorcheteO(self, p):
		if(self.errorStatus):
			return
		else:
			return ExpresionCorcheteO(p.expresionCorcheteOR)

	@_('empty')
	def expresionCorcheteO(self, p):
		return None


	'''
	expresionCorcheteOR : expresionCorcheteOR "[" expresionOpcional "]"
	|	"[" expresionOpcional "]"
	;
	'''
	@_('expresionCorcheteOR "[" expresionOpcional "]"')
	def expresionCorcheteOR(self, p):
		if(self.errorStatus or p.expresionCorcheteOR is None):
			return
		else:
			p.expresionCorcheteOR.append(p.expresionOpcional)
			return p.expresionCorcheteOR

	@_('"[" expresionOpcional "]"')
	def expresionCorcheteOR(self, p):
		if(self.errorStatus):
			return
		else:
			return ExpresionCorcheteOR([p.expresionOpcional])

	'''
	expresionOpcional : expresion
	|	empty
	;
	'''
	@_('expresion')
	def expresionOpcional(self, p):
		if(self.errorStatus):
			return
		else:
			return ExpresionOpcional(p.expresion)

	@_('empty')
	def expresionOpcional(self, p):
		return None


	'''
	tipoFormalBus : expresionCorcheteO "TS"
	|	expresionCorcheteO "OC"
	;
	'''
	@_('expresionCorcheteO TS',
	'expresionCorcheteO OC')
	def tipoFormalBus(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormalBus(p[0], p[1])



	@_('TYPE ID simboloPor listaIdParentesis ";" declaracionConstanteCONST tipoFormalIN tipoFormalINOUT declaracionVariableOUT declaracionVariableVAR declaracionRelacionPOS sentenciaSecuenciaBEGIN END ID')
	def declaracionTipo(self, p):
		if(p.ID0!=p.ID1):
			print("error el {} {} no coincide con su nombre de identificador {} {}".format(p.TYPE, p.ID0, p.END, p.ID1))
			self.errorStatus=True
		elif(self.errorStatus):
			return
		else:
			return DeclaracionTipo(p.ID0, p.simboloPor, p.listaIdParentesis, p.declaracionConstanteCONST, p.tipoFormalIN, p.tipoFormalINOUT, p.declaracionVariableOUT, p.declaracionVariableVAR, p.declaracionRelacionPOS, p.sentenciaSecuenciaBEGIN, p.ID1)


	@_('"*"')
	def simboloPor(self, p):
		if(self.errorStatus):
			return
		else:
			return p[0]

	@_('empty')
	def simboloPor(self, p):
		return None

	'''
	listaIdParentesis : "(" listaId ")"
	|	empty
	;
	'''
	@_('"(" listaId ")"')
	def listaIdParentesis(self, p):
		if(self.errorStatus):
			return
		else:
			return ListaIdParentesis(p.listaId)

	@_('empty')
	def listaIdParentesis(self, p):
		return None

	'''
	tipoFormalIN : IN tipoFormallistaId
	|	empty
	;
	'''
	@_('IN tipoFormallistaId')
	def tipoFormalIN(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormalIN(p.tipoFormallistaId)

	@_('empty')
	def tipoFormalIN(self, p):
		return None

	'''
	tipoFormallistaId : tipoFormallistaIdR
	|	empty
	;
	'''
	@_('tipoFormallistaIdR')
	def tipoFormallistaId(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormallistaId(p.tipoFormallistaIdR)

	@_('empty')
	def tipoFormallistaId(self, p):
		return None

	'''
	tipoFormallistaIdR : tipoFormallistaIdR listaId ":" tipoFormal ";"
	|	listaId ":" tipoFormal ";"
	;
	'''
	@_('tipoFormallistaIdR listaId ":" tipoFormal ";"')
	def tipoFormallistaIdR(self, p):
		if(self.errorStatus or p.tipoFormallistaIdR is None):
			return
		else:
			p.tipoFormallistaIdR.append(p.listaId, p.tipoFormal)
			return p.tipoFormallistaIdR

	@_('listaId ":" tipoFormal ";"')
	def tipoFormallistaIdR(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormallistaIdR([p.listaId],[p.tipoFormal])

	'''
	tipoFormnalINOUT : INOUT tipoFormlBuslistaId
	|	empty
	;
	'''
	@_('INOUT tipoFormlBuslistaId')
	def tipoFormalINOUT(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormalINOUT(p.tipoFormlBuslistaId)

	@_('empty')
	def tipoFormalINOUT(self, p):
		return None

	'''
	tipoFormlBuslistaId : tipoFormlBuslistaIdR
	|	empty
	;
	'''
	@_('tipoFormlBuslistaIdR')
	def tipoFormlBuslistaId(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormlBuslistaId(p.tipoFormlBuslistaIdR)

	@_('empty')
	def tipoFormlBuslistaId(self, p):
		return None

	'''
	tipoFormlBuslistaIdR : tipoFormlBuslistaIdR listaId ":" tipoFormalBus ";"
	|	listaId ":" tipoFormalBus ";"
	;
	'''
	@_('tipoFormlBuslistaIdR listaId ":" tipoFormalBus ";"')
	def tipoFormlBuslistaIdR(self, p):
		if(self.errorStatus or p.tipoFormlBuslistaIdR is None):
			return
		else:
			p.tipoFormlBuslistaIdR.append(p.listaId, p.tipoFormalBus)
			return p.tipoFormlBuslistaIdR

	@_('listaId ":" tipoFormalBus ";"')
	def tipoFormlBuslistaIdR(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormlBuslistaIdR([p.listaId], [p.tipoFormalBus])
	'''
	assinacionUnidad : ID selector "(" listaExpresiones ")"
	'''
	@_('ID selector "(" listaExpresiones ")"')
	def asignacionUnidad(self, p):
		if(self.errorStatus):
			return
		else:
			return AsignacionUnidad(p.ID, p.selector, p.listaExpresiones)

	'''
	empty :
	'''
	@_('')
	def empty(self, p):
		return None

	#prueba de errores
	'''
	tipoSimple : tipoBasico
		|	ID "(" listaExpresiones ")"
		|	ID
		;
	'''
	# @_('error')
	# def tipoSimple(self, p):
		# print("error al indicar tipo simple en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass

	'''
	tipoBasico : 'BIT'
		| 'TS'
		| 'OC'
		;
	'''
	@_('error')
	def tipoBasico(self, p):
		print("error al indicar el tipo basico en {} - linea {}, debe ser BIT TS o OC".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass

	@_('error')
	def declaracionConstante(self, p):
		print("error al declarar constante en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass

	'''
	declaracionVariable : listaId ":" tipo ";"
	;
	'''
	@_('listaId error')
	def declaracionVariable(self, p):
		print("error al declarar variable en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass

	'''
	listaId : listaId "," ID
		|	ID
		|	error
		;
	'''
	@_('error')
	def listaId(self, p):
		print("error con la lista de ID en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass


	@_('error factor')
	def termino(self, p):
		print("error al declarar termino en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass


	@_('MODULE ID ";" error')
	def modulo(self, p):
		print("error al declarar MODULO {} en {} - Line {}".format(p.ID, p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass


	@_('error')
	def tipoFormal(self, p):
		print("error al declrar tipo forma en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass

	@_('error')
	def tipoFormalBus(self, p):
		print("error al declarar bus de datos formal en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass


	@_('TYPE ID error')
	def declaracionTipo(self, p):
		print("error al declarar el TYPE {} en {} - linea {}".format(p.ID, p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass


	@_('error')
	def asignacionUnidad(self, p):
		print("error al asignar unidad en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass

	def error(self, p):
		self.errorStatus=True
		if p:
			#print("Syntax error at token", p.type)
			# Just discard the token or tell the parser it's okay.
			self.errok()
		else:
			print("Syntax error at EOF")
		pass

		#pass
def parse(data, debug=0):
	#print(parser.error)
	p = parser.parse(lexer.tokenize(data))
	#print(parser.errorStatus)
	if parser.errorStatus:
		print("error sintactico")
		return None
	print("\n")
	return p

if __name__ == '__main__':
	import sys
	lexer = Lolalexer()
	parser = LolaParser()
	if(len(sys.argv)!=2):
		sys.stderr.write('Usage: "{}" "filename"\n'.format(sys.argv[0]))
		raise SystemExit(1)
	file= open(sys.argv[1]).read()

	lexer.fileName=sys.argv[1]
	p1 = lexer.tokenize(file)
	result=parser.parse(p1)


	p=parse(file)
	#result = parser.parse(p1)
	# DOT
	'''
	dot=DotCode()
	dot.visit(result)
	result.treeprint()
	print(dot)
	'''

	#para generar codigo
	check=CheckProgramVisitor()
	check.visit(p)
	gen=GenerateCode()
	gen.visit(p)
	for enum, code in enumerate(gen.code):
		print(enum,code)
