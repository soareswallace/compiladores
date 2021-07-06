import enum
import sys

class Lexer:
	def __init__(self, input):
		self.source = input + '\n'
		self.curChar = ''
		self.curPos = -1
		self.nextChar()
		pass

	def nextChar(self):
		self.curPos = self.curPos + 1
		if self.curPos >= len(self.source):
			self.curChar = '\0'
		else:
			self.curChar = self.source[self.curPos]

	def peek(self):
		if self.curPos + 1 >= len(self.source):
			return '\0'
		else:
			return self.source[self.curPos + 1]

	def getToken(self):
		self.skipWhiteSpace()
		self.skipComment()
		if self.curChar == '+':
			token = Token(self.curChar, TokenType.PLUS)
		elif self.curChar == '-':
			token = Token(self.curChar, TokenType.MINUS)
		elif self.curChar == '*':
			token = Token(self.curChar, TokenType.ASTERISK)
		elif self.curChar == '/':
			token = Token(self.curChar, TokenType.SLASH)
		elif self.curChar == '\n':	
			token = Token(self.curChar, TokenType.NEWLINE)
		elif self.curChar == '\0':		
			token = Token(self.curChar, TokenType.EOF)
		elif self.curChar == '=':
			if self.peek() == '=':
				c = self.curChar
				self.nextChar()
				token = Token(c + self.curChar, TokenType.EQEQ)
			else:
				token = Token(self.curChar, TokenType.EQ)
		elif self.curChar == '!':
			if self.peek() == '=':
				c = self.curChar
				self.nextChar()
				token = Token(c + self.curChar, TokenType.NOTEQ)
			else:
				self.abort('Esperava o simbolo de = e recebeu ' + self.peek())
		elif self.curChar == '>':
			if self.peek() == '=':
				c = self.curChar
				self.nextChar()
				token = Token(c + self.curChar, TokenType.GTEQ)
			else:
				token = Token(self.curChar, TokenType.GT)
		elif self.curChar == '<':
			if self.peek() == '=':
				c = self.curChar
				self.nextChar()
				token = Token(c + self.curChar, TokenType.LTEQ)
			else:
				token = Token(self.curChar, TokenType.LT)
		elif self.curChar == '\"':
			self.nextChar()
			startPos = self.curPos
			while self.curChar != '\"':
				if self.curChar == '\\' or self.curChar == '\t' or self.curChar == '\r' or self.curChar == '%':
					self.abort('Caractere ilegal')
				self.nextChar()
			stringText = self.source[startPos : self.curPos]
			token = Token(stringText, TokenType.STRING)
		elif self.curChar.isdigit():
			startPos = self.curPos
			while self.peek().isdigit():
				self.nextChar()
			if self.peek() == '.':
				self.nextChar()
				if not self.peek().isdigit():
					self.abort('Caractere ilegal dentro de numero: '+ self.peek())
				while self.peek().isdigit():
					self.nextChar()
			number = self.source[startPos : self.curPos + 1]
			token = Token(number, TokenType.NUMBER)
		elif self.curChar.isalpha():
			startPos = self.curPos
			while self.peek().isalnum():
				self.nextChar()
			word = self.source[startPos : self.curPos + 1]
			keyword = Token.checkIfKeyword(word)
			if keyword == None:
				token = Token(word, TokenType.IDENT)
			else:
				token = Token(word, keyword)
		else:
			self.abort('Token desconhecido: ' + self.curChar)

		self.nextChar()
		return token

	def abort(self, message):
		sys.exit('Erro léxico! ' + message)

	def skipWhiteSpace(self):
		while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
			self.nextChar()

	def skipComment(self):
		if self.curChar == '#':
			while self.curChar != '\n':
				self.nextChar()

class Token:
	def __init__(self, tokenText, tokenKind):
		self.text = tokenText
		self.kind = tokenKind

	@staticmethod
	def checkIfKeyword(word):
		for kind in TokenType:
			if kind.name == word.upper() and kind.value >= 100 and kind.value < 200:
				return kind
		return None

class TokenType(enum.Enum):
	EOF = -1
	NEWLINE = 0
	NUMBER = 1
	IDENT = 2
	STRING = 3

	#palavras reservadas

	LABEL = 101
	GOTO = 102
	PRINT = 103
	INPUT = 104
	LET = 105
	IF = 106
	THEN = 107
	ENDIF = 108
	WHILE = 109
	REPEAT = 110
	ENDWHILE = 111

	#OPERADORES

	EQ = 201
	PLUS = 202
	MINUS = 203
	ASTERISK = 204
	SLASH = 205
	EQEQ = 206
	NOTEQ = 207
	LT = 208
	LTEQ = 209
	GT = 210
	GTEQ = 211
