import sys
import ply.yacc as yacc
import turtle
import copy

from gramatica import tokens

class CalcError(Exception):
    def __init__(self, message):
        self.message = message


variables = {"main": {"type": "void", "param": {},
                      "run": [], "var": {"cont sys": 0}}}

# Cubo semantico con las variables y sus respectivos resultados
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

def searchType(tipo):
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

def searchVar(tempPar,tempVar,var):
     # Busca la variable entre las variables globales
     if variables["main"]["var"].get(var) != None:
          return variables["main"]["var"][var]
     elif variables["active sys"] != "main": # Busca entre los parametros y variables locales recibidos si no esta activa la funcion main
          if tempVar.get(var) != None:
               return tempVar[var]
          elif tempPar.get(var) != None:
               return tempPar[var]
     print("ERROR: Variable no encontrada")
     raise CalcError("Variable invalida")

# Regresar operador
def op(op,op1,op2):
     if op == '*':
          return op1 + op2
     elif op == '-':
          return op1 - op2
     elif op == '/':
          return op1 / op2
     elif op == '*':
          return op1 * op2
     elif op == '==':
          return op1 == op2
     elif op == '<':
          return op1 < op2
     elif op == '>':
          return op1 > op2
     elif op == '<=':
          return op1 <= op2
     elif op == '>=':
          return op1 >= op2
     elif op == '!=':
          return op1 != op2
     elif op == '&':
          return op1 and op2
     elif op == '|':
          return op1 or op2
     else:
          print("ERROR: Error en operador")
          raise CalcError("Error en sistema")

def call(function,param,var):
     cont = 0
     while cont < len(variables[function]["run"]):
          a = variables[function]["run"][cont][0]
          b = variables[function]["run"][cont][1]
          c = variables[function]["run"][cont][2]
          d = variables[function]["run"][cont][3]
          if a == "read":
               # Recibe el apuntador a la variable
               vard = searchVar(param,var,d)
               vard["value"] = read(vard["type"])
          elif (a == '*' or a == '/' or a == '-' or a == '+' or a == '==' or a == '>' or a == '<' or a == '<=' or a == '>=' or a == '!=' or a == '&' or a == '|'):
               # Recibe el apuntador a la variable
               varb = searchVar(param,var,b)
               # Comprueba que la variable se encuentre inicializada
               if varb.get("value") == None:
                    print("ERROR: Variable no inicializada")
                    raise CalcError("Expresion invalida")
               varc = searchVar(param,var,c)
               if varc.get("value") == None:
                    print("ERROR: Variable no inicializada")
                    raise CalcError("Expresion invalida")
               vard = searchVar(param,var,d)
               # Recibe el resultado de la operacion
               vard["value"] = op(a,varb["value"],varc["value"])
          elif a == '=':
               # Recibe el apuntador a la variable
               varb = searchVar(param,var,b)
               # Comprueba que la variable se encuentre inicializada
               if varb.get("value") == None:
                    print("ERROR: Variable no inicializada")
                    raise CalcError("Expresion invalida")
               vard = searchVar(param,var,d)
               # Ejecuta la asignacion
               vard["value"] = varb["value"]
          elif a == "callr" or a == "call":
               # Activa la nueva funcion a ejecutar
               variables["active sys"] = b
               # Hace una copia local de los parametros
               tparam = copy.deepcopy(variables[b]["param"])
               tcont = 0
               # Inicializa cada parametro con el valor recibido
               for x in tparam:
                    varc = searchVar(param,var,c[tcont])
                    if varc.get("value") == None:
                         print("ERROR: Variable no inicializada")
                         raise CalcError("Expresion invalida")
                    tparam[x]["value"] = varc["value"]
                    tcont = tcont + 1
               if a == "callr":
                    # Ejecuta la funcion con parametros locales, ya inicializados, y envia una copia local de las variables
                    # Guarda el retorno de la funcion en una variable temporal
                    temp = call(b,tparam,copy.deepcopy(variables[b]["var"]))
                    # Activa la funcion anterior
                    variables["active sys"] = function
                    # Si la funcion regresa un valor, lo guarda en la variable asignada
                    if temp == "Sys None":
                         print("ERROR: No llego a un return la funcion")
                         raise CalcError("Estatuto faltante")
                    else:
                         vard = searchVar(param,var,d)
                         vard["value"] = temp
               else:
                    # Ejecuta la funcion con parametros locales, ya inicializados, y envia una copia local de las variables
                    call(b,tparam,copy.deepcopy(variables[b]["var"]))
                    # Activa la funcion anterior
                    variables["active sys"] = function
          elif a == "gotof":
               varb = searchVar(param,var,b)
               # Si el valor de la variable es falso, actualiza el cont
               if varb["value"] == False:
                    cont = cont + d - 1
          elif a == "goto":
               # Actualiza el cont
               cont = cont + d - 1
          elif a == "return":
               vard = searchVar(param,var,d)
               if vard.get("value") == None:
                    print("ERROR: Variable no inicializada")
                    raise CalcError("Expresion invalida")
               # Regresa el valor de la variable
               return vard["value"]
          elif a == "write":
               vard = searchVar(param,var,d)
               if vard.get("value") == None:
                    print("ERROR: Variable no inicializada")
                    raise CalcError("Expresion invalida")
               # Imprime el valor de la variable
               print(vard["value"])
          elif a == "callf":
               tempValues = []
               # Crea un listado con los valores de los parametros recibidos
               for value in c:
                    varc = searchVar(param,var,value)
                    tempValues.append(varc["value"])
               # Llama a ejecutar la funcion especial
####            # callf(b,tempValues) 
          else:
               print("ERROR: CALL01")
               raise CalcError("Error en sistema")
          cont = cont + 1
     return "Sys None"

def read(tipo):
     if tipo == "int":
          return int(input())
     elif tipo == "float":
          return float(input())
     elif tipo == "char":
          inputTemp = str(input())
          if len(inputTemp) != 1:
               print("ERROR: Longitud mayor a 1")
               raise CalcError("Input invalido")
          return inputTemp
     print("ERROR: Unable to READ")
     raise CalcError("Error en sistema")

def run():
     # Declara a main como función activa
     variables["active sys"] = "main" ###
     # Comienza la ejecución con un apuntador a las variables y parámetros globales de main
     call("main",variables["main"]["param"],variables["main"]["var"])
###


def p_program(p):
    '''program : programI funcVar funcTemp programM'''
    for funcion in variables:
          if funcion != "active sys":
               variables["active sys"] = funcion
               for a,b,c,d in variables[funcion]["run"]:
                    if (a == '+' or a == '-' or a == '*' or a == '/' or a == '==' or a == '!=' or a == '<=' or a == '>=' or a == '<' or a == '>' or a == '&' or a == '|'):
                         tempB = searchType(b)
                         tempC = searchType(c)
                         if dataTable[tempB][tempC][a] == "error":
                              print("ERROR: Tipos de valores invalidos")
                              raise CalcError("Expresion invalida")
                         variables[variables["active sys"]]["var"][d] = {"type": dataTable[tempB][tempC][a]}
                    elif a == "gotof":
                         if searchType(b) != "bool":
                              print("ERROR: PROGRAM02")
                              raise CalcError("Expresion invalida")
                    elif a == "=":
                         tempB = searchType(b)
                         tempD = searchType(d)
                         if (dataTable[tempB][tempD][a] != tempD):
                              print("ERROR: Tipo de variable invalido en asignacion")
                              raise CalcError("Estatuto invalido")
                    elif a == "return":
                         if variables[variables["active sys"]]["type"] == "void":
                              print("ERROR: Return en funcion void")
                              raise CalcError("Estatuto invalido")
                         elif variables[variables["active sys"]]["type"] != searchType(d):
                              print("ERROR: Tipo de return invalido")
                              raise CalcError("Estatuto invalido")
                    elif a == "callr":
                         if variables.get(b) == None:
                              print("ERROR: Llamada a funcion invalida")
                              raise CalcError("Estatuto invalido")
                         if variables[b]["type"] == "void":
                              print("ERROR: Llamada con return a funcion void")
                              raise CalcError("Estatuto invalido")
                         else:
                              variables[variables["active sys"]]["var"][d] = {"type": variables[b]["type"]}
                         if len(variables[b]["param"]) != len(c):
                              print("ERROR: Cantidad de parametros invalida")
                              raise CalcError("Estatuto invalido")
                         cont = 0
                         for param in variables[b]["param"]:
                              tc = searchType(c[cont])
                              if (variables[b]["param"][param]["type"] != tc and (variables[b]["param"][param]["type"] == "int" and tc != "float")):
                                   print("ERROR: Tipo de parametro esperado invalido en return")
                                   raise CalcError("Estatuto invalido")
                              cont = cont + 1
                    elif a == "call":
                         if variables.get(b) == None:
                              print("ERROR: Llamada a funcion invalida")
                              raise CalcError("Estatuto invalido")
                         if variables[b]["type"] != "void":
                              print("ERROR: Llamada a funcion con return en llamada void")
                              raise CalcError("Estatuto invalido")
                         elif b == "main":
                              print("ERROR: Llamada a main")
                              raise CalcError("Estatuto invalido")
                         if len(variables[b]["param"]) != len(c):
                              print("ERROR: Cantidad de parametros invalida")
                              raise CalcError("Estatuto invalido")
                         cont = 0
                         for param in variables[b]["param"]:
                              tempC = searchType(c[cont])
                              if (variables[b]["param"][param]["type"] != tempC and (variables[b]["param"][param]["type"] == "int" and tempC != "float")):
                                   print("ERROR: Tipo de parametro esperado invalido")
                                   raise CalcError("Estatuto invalido")
                              cont = cont + 1
                    elif a == "read" or a == "write":
                         searchType(d)
                    elif (a != "callf" and a != "goto"):
                         print("ERROR: PROGRAM01")
                         raise CalcError("Error en sistema")
          print("PROGRAMA COMPILADO")
          run()
    # p[0] = "PROGRAMA COMPILADO"

def p_funcTemp(p):
     '''funcTemp : funcC funcTemp2''' 

def p_funcTemp2(p):
    '''funcTemp : empty'''
     
def p_programM(p):
    '''programM : programMI bloque'''
    variables["main"]["run"] = p[3]
     
def p_programMI(p):
     '''programMI : MAIN PARIZQ PARDER'''
     variables["active sys"] = "main"
     
def p_programI(p):
     '''programI : PROGRAM ID PTCOMA'''
     variables["active sys"] = "main"

def p_funcVar(p):
     '''funcVar : VAR funcVar2
               | empty '''

def p_funcVar2(p):
     '''funcVar2 : tipo SVAR nombreVar funcVar2
             | empty '''
     if p[1] != None:
          t = [p[2]]
          t.extend(p[3])
          for x in t:
               if variables["main"]["var"].get(x) != None:
                    print("ERROR: Nombre de variable repetido, variable global declarada")
                    raise CalcError("Variable repetida")
               if variables["active sys"] != "main":
                    if variables[variables["active sys"]]["param"].get(x) != None:
                         print("ERROR: Nombre de parametro repetido, funcion declarada")
                         raise CalcError("Variable repetida")
                    if variables[variables["active sys"]]["var"].get(x) != None:
                         print("ERROR: Nombre de variable repetido, funcion declarada")
                         raise CalcError("Variable repetida")
               variables[variables["active sys"]]["var"][x] = {"type": p[1]}

def p_nombreVar(p):
     '''nombreVar : COMA ID nombreVar
               | PTCOMA '''
     if p[1] != ';':
          t = [p[2]]
          t.extend(p[3]) # Add all elements to end of list
          p[0] = t
     else:
          p[0] = []

# mio

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
                  | NOIGUAL exp
                  | ESIGUAL exp
                  | MAYIG exp
                  | MENIG exp'''

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

# Error si falla la sintaxis de la entrada
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


