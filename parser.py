import sys
from lexer import *


class Parser(object):
	"""docstring for Parser"""
	def __init__(self, lexer):
		super(Parser, self).__init__()
		self.lexer = lexer
		self.curToken = None
		self.peekToken = None
		self.nextToken()
		self.nextToken()

	def checkToken(self, kind):
		return kind == self.curToken.kind

	def checkPeek(self, kind):
		return kind == self.peekToken.kind

	def match(self, kind):
		if not self.checkToken(kind):
			self.abort("Esperava por " + kind.name + ", apareceu " + self.curToken.kind.name)
		self.nextToken()

	def nextToken(self):
		self.curToken = self.peekToken
		self.peekToken = self.lexer.getToken()

	def abort(self, msg):
		sys.exit("Erro sintatico: " + msg)


	def program(self):
		print("PROGRAM")
		while not self.checkToken(TokenType.EOF):
			self.statement()

	def statement(self):
		if self.checkToken(TokenType.PRINT):
			print("STM-PRINT")
			self.nextToken()
			if self.checkToken(TokenType.STRING):
				self.nextToken()
			else:
				self.expression()
		elif self.checkToken(TokenType.IF):
			print ("STM-IF")
			self.nextToken()
			self.comparison()
			self.match(TokenType.THEN)
			self.nl()
			while not self.checkToken(TokenType.ENDIF):
				self.statement()
			self.match(TokenType.ENDIF)
		elif self.checkToken(TokenType.WHILE):
			print ("STM-WHILE")
			self.nextToken()
			self.comparison()
			self.match(TokenType.REPEAT)
			self.nl()
			while not self.checkToken(TokenType.ENDWHILE):
				self.statement()
			self.match(TokenType.ENDWHILE)
		elif self.checkToken(TokenType.LET):
			print ("STM-LET")
			self.nextToken()
			self.match(TokenType.IDENT)
			self.match(TokenType.EQ)
			self.expression()
		elif self.checkToken(TokenType.INPUT):
			print ("STM-INPUT")
			self.nextToken()
			self.match(TokenType.IDENT)
		else:
			self.abort("Erro, problema com " + self.curToken.kind.name)
		self.nl()

	def comparison(self):
		print ("COMPARISON")
		self.expression()
		if self.isComparisonOperator():
			self.nextToken()
			self.expression()
		else:
			self.abort("Esperava por algum operador de comparação: " + self.curToken.text)


	def isComparisonOperator(self):
		return self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.GTEQ)or self.checkToken(TokenType.GT) 

	def expression(self):
		print ("EXPRESSION")
		self.term()
		while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
			self.nextToken()
			self.term()

	def term(self):
		print ("TERM")
		self.unary()
		while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
			self.nextToken()
			self.unary()

	def unary(self):
		print ("UNARY")
		if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
			self.nextToken()
		self.primary()

	def primary(self):
		print ("PRIMARY (" + self.curToken.text + ")")
		if self.checkToken(TokenType.NUMBER):
			self.nextToken()
		elif self.checkToken(TokenType.IDENT):
			self.nextToken()
		else:
			self.abort("Token inesperado: " + self.curToken.text)

	def nl(self):
		print("NEW LINE")
		self.match(TokenType.NEWLINE)
		while self.checkToken(TokenType.NEWLINE):
			self.nextToken()