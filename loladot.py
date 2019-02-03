
# Lola - Dibujar AST + graphviz

import pydotplus as pgv
from lolaast import *
class DotCode(NodeVisitor):
	def __init__(self):
		super(DotCode, self).__init__()

		# Secuencia para los nombres de nodos
		self.id = 0

		# Stack para retornar nodos procesados
		self.stack = []

		# Inicializacion del grafo para Dot
		self.dot = pgv.Dot('AST', graph_type='digraph')

		self.dot.set_edge_defaults(arrowhead='vee')

	def __repr__(self):
		return self.dot.to_string()

	def new_node(self, node, shape, color, style, label=None):
		if label is None: label = node.__class__.__name__
		self.id += 1
		return pgv.Node('n{}'.format(self.id), label=label, shape=shape, color=color, style=style)

	def push_node(self, current, node):
		self.dot.add_node(current)
		self.stack.append(current)
		self.stack.pop()
		if len(self.stack):
			self.dot.add_edge(pgv.Edge(self.stack[len(self.stack)-1], current))

	def visit_Module(self, node):
		current = self.new_node(node, 'octagon', 'blue', 'filled')
		self.push_node(current, node)


	def generic_visit(self, node):
		current = self.new_node(node,'box', 'lightgray', 'filled')
		self.push_node(current, node)
