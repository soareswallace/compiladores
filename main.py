from lexer import *
from parser import *
import sys

def main():
	if len(sys.argv) != 2:
		sys.exit("Erro")
	with open(sys.argv[1], 'r') as inputFile:
		input  = inputFile.read()

	lexer = Lexer(input)
	parser = Parser(lexer)
	parser.program()
	print ("terminamos o parser")

main()