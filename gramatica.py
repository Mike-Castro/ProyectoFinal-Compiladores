import ply.lex as lex

reserved = {
    'program' : 'PROGRAM',
    'if' : 'IF',
    'else' : 'ELSE',
    'do' : 'DO',
    'while' : 'WHILE',
    'var' : 'VAR',
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'print' : 'PRINT',
    'main' : 'MAIN',
    'void' : 'VOID',
    'return' : 'RETURN',
    'true' : 'TRUE',
    'false' : 'FALSE'
}

tokens = [
    'PARIZQ',
    'PARDER',
    'CURLIZQ',
    'CURLDER',
    'PTCOMA',
    'MAYOR',
    'MENOR',
    'MAYIG',
    'MENIG',
    'SUMA',
    'RESTA',
    'POR',
    'DIV',
    'NOIGUAL',
    'COMA',
    'ID',
    'CTEF',
    'CTEI',
    'CTESTRING',
    'CTECHAR',
    'DOSPT',
    'IGUAL',
    'AND',
    'OR'
 ] + list(reserved.values())

t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CURLIZQ = r'\{'
t_CURLDER = r'\}'
t_PTCOMA = r';'
t_DOSPT = r':'
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYIG = r'>='
t_MENIG = r'<='
t_ESIGUAL = r'=='
t_NOIGUAL = r'!='
t_SUMA = r'\+'
t_RESTA = r'-'
t_POR = r'\*'
t_DIV = r'/'
t_COMA = r','
t_IGUAL = r'='
t_OR = r'\|'
t_AND = r'\&'

def t_CTEF(t):
    r'([0-9]+[.])[0-9]+'
    t.value = float(t.value)
    return t

def t_CTEI(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_CTESTRING(t):
    r'\".*\"'
    return t

def t_CTECHAR(t):
    r'\'.\''
    return t

t_ignore = ' \t'

# Nueva linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ERROR handling rule 
def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

lex.lex()
