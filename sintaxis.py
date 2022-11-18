import sys
import ply.yacc as yacc
import turtle

from gramatica import tokens

class CalcError(Exception):
    def __init__(self, message):
        self.message = message


variables = {"main":{"type":"void","param":{},"run":[],"var":{"contador sys": 0}}}

dataTable = {}

dataTable["int"] = {"int": {}, "float": {}, "char": {}, "bool": {}}
dataTable["float"] = {"int": {}, "float": {}, "char": {}, "bool": {}}
dataTable["char"] = {"int": {}, "float": {}, "char": {}, "bool": {}}
dataTable["bool"] = {"int": {}, "float": {}, "char": {}, "bool": {}}

dataTable["int"]["int"]["="] = "int"
dataTable["int"]["int"]["+"] = "int"
dataTable["int"]["int"]["-"] = "int"
dataTable["int"]["int"]["*"] = "int"
dataTable["int"]["int"]["/"] = "float"
dataTable["int"]["int"]["=="] = "bool"
dataTable["int"]["int"]["!="] = "bool"
dataTable["int"]["int"]["<="] = "bool"
dataTable["int"]["int"][">="] = "bool"
dataTable["int"]["int"]["<"] = "bool"
dataTable["int"]["int"][">"] = "bool"
dataTable["int"]["int"]["&"] = "error"
dataTable["int"]["int"]["|"] = "error"

dataTable["int"]["float"]["="] = "float"
dataTable["int"]["float"]["+"] = "float"
dataTable["int"]["float"]["-"] = "float"
dataTable["int"]["float"]["*"] = "float"
dataTable["int"]["float"]["/"] = "float"
dataTable["int"]["float"]["=="] = "bool"
dataTable["int"]["float"]["!="] = "bool"
dataTable["int"]["float"]["<="] = "bool"
dataTable["int"]["float"][">="] = "bool"
dataTable["int"]["float"]["<"] = "bool"
dataTable["int"]["float"][">"] = "bool"
dataTable["int"]["float"]["&"] = "error"
dataTable["int"]["float"]["|"] = "error"

dataTable["int"]["char"]["="] = "error"
dataTable["int"]["char"]["+"] = "error"
dataTable["int"]["char"]["-"] = "error"
dataTable["int"]["char"]["*"] = "error"
dataTable["int"]["char"]["/"] = "error"
dataTable["int"]["char"]["=="] = "bool"
dataTable["int"]["char"]["!="] = "bool"
dataTable["int"]["char"]["<="] = "error"
dataTable["int"]["char"][">="] = "error"
dataTable["int"]["char"]["<"] = "error"
dataTable["int"]["char"][">"] = "error"
dataTable["int"]["char"]["&"] = "error"
dataTable["int"]["char"]["|"] = "error"

dataTable["int"]["bool"]["="] = "error"
dataTable["int"]["bool"]["+"] = "error"
dataTable["int"]["bool"]["-"] = "error"
dataTable["int"]["bool"]["*"] = "error"
dataTable["int"]["bool"]["/"] = "error"
dataTable["int"]["bool"]["=="] = "bool"
dataTable["int"]["bool"]["!="] = "bool"
dataTable["int"]["bool"]["<="] = "error"
dataTable["int"]["bool"][">="] = "error"
dataTable["int"]["bool"]["<"] = "error"
dataTable["int"]["bool"][">"] = "error"
dataTable["int"]["bool"]["&"] = "error"
dataTable["int"]["bool"]["|"] = "error"

dataTable["float"]["int"]["="] = "float"
dataTable["float"]["int"]["+"] = "float"
dataTable["float"]["int"]["-"] = "float"
dataTable["float"]["int"]["*"] = "float"
dataTable["float"]["int"]["/"] = "float"
dataTable["float"]["int"]["=="] = "bool"
dataTable["float"]["int"]["!="] = "bool"
dataTable["float"]["int"]["<="] = "bool"
dataTable["float"]["int"][">="] = "bool"
dataTable["float"]["int"]["<"] = "bool"
dataTable["float"]["int"][">"] = "bool"
dataTable["float"]["int"]["&"] = "error"
dataTable["float"]["int"]["|"] = "error"

dataTable["float"]["float"]["="] = "float"
dataTable["float"]["float"]["+"] = "float"
dataTable["float"]["float"]["-"] = "float"
dataTable["float"]["float"]["*"] = "float"
dataTable["float"]["float"]["/"] = "float"
dataTable["float"]["float"]["=="] = "bool"
dataTable["float"]["float"]["!="] = "bool"
dataTable["float"]["float"]["<="] = "bool"
dataTable["float"]["float"][">="] = "bool"
dataTable["float"]["float"]["<"] = "bool"
dataTable["float"]["float"][">"] = "bool"
dataTable["float"]["float"]["&"] = "error"
dataTable["float"]["float"]["|"] = "error"

dataTable["float"]["char"]["="] = "error"
dataTable["float"]["char"]["+"] = "error"
dataTable["float"]["char"]["-"] = "error"
dataTable["float"]["char"]["*"] = "error"
dataTable["float"]["char"]["/"] = "error"
dataTable["float"]["char"]["=="] = "bool"
dataTable["float"]["char"]["!="] = "bool"
dataTable["float"]["char"]["<="] = "error"
dataTable["float"]["char"][">="] = "error"
dataTable["float"]["char"]["<"] = "error"
dataTable["float"]["char"][">"] = "error"
dataTable["float"]["char"]["&"] = "error"
dataTable["float"]["char"]["|"] = "error"

dataTable["float"]["bool"]["="] = "error"
dataTable["float"]["bool"]["+"] = "error"
dataTable["float"]["bool"]["-"] = "error"
dataTable["float"]["bool"]["*"] = "error"
dataTable["float"]["bool"]["/"] = "error"
dataTable["float"]["bool"]["=="] = "bool"
dataTable["float"]["bool"]["!="] = "bool"
dataTable["float"]["bool"]["<="] = "error"
dataTable["float"]["bool"][">="] = "error"
dataTable["float"]["bool"]["<"] = "error"
dataTable["float"]["bool"][">"] = "error"
dataTable["float"]["bool"]["&"] = "error"
dataTable["float"]["bool"]["|"] = "error"

dataTable["char"]["int"]["="] = "error"
dataTable["char"]["int"]["+"] = "error"
dataTable["char"]["int"]["-"] = "error"
dataTable["char"]["int"]["*"] = "error"
dataTable["char"]["int"]["/"] = "error"
dataTable["char"]["int"]["=="] = "bool"
dataTable["char"]["int"]["!="] = "bool"
dataTable["char"]["int"]["<="] = "error"
dataTable["char"]["int"][">="] = "error"
dataTable["char"]["int"]["<"] = "error"
dataTable["char"]["int"][">"] = "error"
dataTable["char"]["int"]["&"] = "error"
dataTable["char"]["int"]["|"] = "error"

dataTable["char"]["float"]["="] = "error"
dataTable["char"]["float"]["+"] = "error"
dataTable["char"]["float"]["-"] = "error"
dataTable["char"]["float"]["*"] = "error"
dataTable["char"]["float"]["/"] = "error"
dataTable["char"]["float"]["=="] = "bool"
dataTable["char"]["float"]["!="] = "bool"
dataTable["char"]["float"]["<="] = "error"
dataTable["char"]["float"][">="] = "error"
dataTable["char"]["float"]["<"] = "error"
dataTable["char"]["float"][">"] = "error"
dataTable["char"]["float"]["&"] = "error"
dataTable["char"]["float"]["|"] = "error"

dataTable["char"]["char"]["="] = "char"
dataTable["char"]["char"]["+"] = "error"
dataTable["char"]["char"]["-"] = "error"
dataTable["char"]["char"]["*"] = "error"
dataTable["char"]["char"]["/"] = "error"
dataTable["char"]["char"]["=="] = "bool"
dataTable["char"]["char"]["!="] = "bool"
dataTable["char"]["char"]["<="] = "error"
dataTable["char"]["char"][">="] = "error"
dataTable["char"]["char"]["<"] = "error"
dataTable["char"]["char"][">"] = "error"
dataTable["char"]["char"]["&"] = "error"
dataTable["char"]["char"]["|"] = "error"

dataTable["char"]["bool"]["="] = "error"
dataTable["char"]["bool"]["+"] = "error"
dataTable["char"]["bool"]["-"] = "error"
dataTable["char"]["bool"]["*"] = "error"
dataTable["char"]["bool"]["/"] = "error"
dataTable["char"]["bool"]["=="] = "bool"
dataTable["char"]["bool"]["!="] = "bool"
dataTable["char"]["bool"]["<="] = "error"
dataTable["char"]["bool"][">="] = "error"
dataTable["char"]["bool"]["<"] = "error"
dataTable["char"]["bool"][">"] = "error"
dataTable["char"]["bool"]["&"] = "error"
dataTable["char"]["bool"]["|"] = "error"

dataTable["bool"]["int"]["="] = "error"
dataTable["bool"]["int"]["+"] = "error"
dataTable["bool"]["int"]["-"] = "error"
dataTable["bool"]["int"]["*"] = "error"
dataTable["bool"]["int"]["/"] = "error"
dataTable["bool"]["int"]["=="] = "bool"
dataTable["bool"]["int"]["!="] = "bool"
dataTable["bool"]["int"]["<="] = "error"
dataTable["bool"]["int"][">="] = "error"
dataTable["bool"]["int"]["<"] = "error"
dataTable["bool"]["int"][">"] = "error"
dataTable["bool"]["int"]["&"] = "error"
dataTable["bool"]["int"]["|"] = "error"

dataTable["bool"]["float"]["="] = "error"
dataTable["bool"]["float"]["+"] = "error"
dataTable["bool"]["float"]["-"] = "error"
dataTable["bool"]["float"]["*"] = "error"
dataTable["bool"]["float"]["/"] = "error"
dataTable["bool"]["float"]["=="] = "bool"
dataTable["bool"]["float"]["!="] = "bool"
dataTable["bool"]["float"]["<="] = "error"
dataTable["bool"]["float"][">="] = "error"
dataTable["bool"]["float"]["<"] = "error"
dataTable["bool"]["float"][">"] = "error"
dataTable["bool"]["float"]["&"] = "error"
dataTable["bool"]["float"]["|"] = "error"

dataTable["bool"]["char"]["="] = "error"
dataTable["bool"]["char"]["+"] = "error"
dataTable["bool"]["char"]["-"] = "error"
dataTable["bool"]["char"]["*"] = "error"
dataTable["bool"]["char"]["/"] = "error"
dataTable["bool"]["char"]["=="] = "bool"
dataTable["bool"]["char"]["!="] = "bool"
dataTable["bool"]["char"]["<="] = "error"
dataTable["bool"]["char"][">="] = "error"
dataTable["bool"]["char"]["<"] = "error"
dataTable["bool"]["char"][">"] = "error"
dataTable["bool"]["char"]["&"] = "error"
dataTable["bool"]["char"]["|"] = "error"

dataTable["bool"]["bool"]["="] = "bool"
dataTable["bool"]["bool"]["+"] = "error"
dataTable["bool"]["bool"]["-"] = "error"
dataTable["bool"]["bool"]["*"] = "error"
dataTable["bool"]["bool"]["/"] = "error"
dataTable["bool"]["bool"]["=="] = "bool"
dataTable["bool"]["bool"]["!="] = "bool"
dataTable["bool"]["bool"]["<="] = "error"
dataTable["bool"]["bool"][">="] = "error"
dataTable["bool"]["bool"]["<"] = "error"
dataTable["bool"]["bool"][">"] = "error"
dataTable["bool"]["bool"]["&"] = "bool"
dataTable["bool"]["bool"]["|"] = "bool"

def buscarTipo(tipo):
     if type(tipo) == type(1):
          return "int"
     elif type(tipo) == type(1.0):
          return "float"
     elif tipo[0] == "'":
          return "char"
     elif tipo[0] == '"':
          return "str"
     elif (tipo == "true" or tipo == "false"):
          return "bool"
     elif variables["main"]["var"].get(tipo) != None:
          return variables["main"]["var"][tipo]["type"]
     elif variables["active sys"] != "main":
          if variables[variables["active sys"]]["var"].get(tipo) != None:
               return variables[variables["active sys"]]["var"][tipo]["type"]
          elif variables[variables["active sys"]]["param"].get(tipo) != None:
               return variables[variables["active sys"]]["param"][tipo]["type"]
     print("ERROR: Tipo de variable no encontrada")
     raise CalcError("Variable invalida")

def p_program(p):
    '''program : PROGRAM ID PTCOMA programP'''
    p[0] = "PROGRAMA COMPILADO"

def p_programaP(p):
    '''programP : varsBloque
                | bloque'''

def p_vars(p):
    '''vars : VAR varV'''

def p_varV(p):
    '''varV : ID varVV'''

def p_varVV(p):
    '''varVV : COMA ID varVV 
             | DOSPT tipo PTCOMA varV
             | DOSPT tipo PTCOMA'''

def p_bloque(p):
    '''bloque : CURLIZQ bloqueB CURLDER
              | CURLIZQ CURLDER'''

def p_bloqueB(b):
    '''bloqueB : estatudo bloqueB 
               | estatuto'''

def p_estatuto(p):
    '''estatuto : asignacion
                | condicion
                | escritura'''

def p_asignacion(p):
    '''asignacion : ID EQUALS expresion PTCOMA'''

def p_condicion(p):
    '''condicion : IF PARIZQ expresion PARDER bloque condicionC'''

def p_condicionC(p):
    '''condicionC : ELSE bloque PTCOMA
                  | PTCOMA'''

def p_escritura(p):
    '''escritura : PRINT PARIZQ escrituraE PARDER PTCOMA'''

def p_escrituraE(p):
    ''' escrituraE : expresion 
                   | expresion COMA escrituraE
                   | CTESTRING 
                   | CTESTRING COMA escrituraE'''

def p_expresion(p):
    '''expresion : exp 
                 | exp expresionE'''

def p_expresionE(p): 
    '''expresionE : MAYOR exp
                  | MENOR exp
                  | NE exp'''

def p_exp(p):
    '''exp : termino 
           | termino exp expE'''

def p_expE(p):
    '''expE : MAS exp
            | MENOS exp'''
    
def p_termino(p):
    '''termino : factor
               | factor termino terminoT'''

def p_terminoT(p):
    '''terminoT : POR termino
                | DIV termino'''

def p_factor(p):
    '''factor : PARIZQ expresion PARDER 
              | factorF'''

def p_factorF(p):
    '''factorF : varcte
               | MAS varcte
               | MENOS varcte'''

def p_varcte(p):
    '''varcte : ID
              | CTEI
              | CTEF'''

def p_empty(p):
    '''empty :'''

def p_error(p):
    print("ERROR en {}".format(p))

yacc.yacc()

# Compilar sintaxis con el archivo de prueba como argumento
if __name__ == '__main__':
    if(len(sys.argv) > 1):
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.read()
            f.close()
            if (yacc.parse(data, tracking=True) == "PROGRAMA COMPILADO"):
                print("Sintaxis valida")
        except EOFError:
            print(EOFError)
    else:
        print("No existe el archivo")


