"""
Analizador léxico de GameRules.

Basado en el analizador léxico entregado por el docente, con dos cambios:
  1. Se agregó el token COMA para separar los parámetros de las acciones.
  2. Cada token guarda su línea y columna, para que el parser pueda
     indicar dónde ocurre un error.
"""

import re
from collections import namedtuple

# Un token es (tipo, lexema, línea, columna).
Token = namedtuple('Token', ['tipo', 'lexema', 'linea', 'columna'])

ESPECIFICACION_TOKENS = [
    ('NUM',        r'\d+'),
    ('OP_REL',     r'>=|<=|==|!=|>|<'),
    ('PUNTO_COMA', r';'),
    ('COMA',       r','),
    ('PARENT_IZQ', r'\('),
    ('PARENT_DER', r'\)'),
    ('ID',         r'[A-Za-z_][A-Za-z0-9_]*'),
    ('SALTO',      r'\n'),
    ('ESPACIO',    r'[ \t\r]+'),
    ('ERROR',      r'.'),
]

PATRON = re.compile('|'.join(
    f'(?P<{nombre}>{expresion})'
    for nombre, expresion in ESPECIFICACION_TOKENS
))

PALABRAS_RESERVADAS = {'WHEN', 'THEN', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE'}


class ErrorLexico(Exception):
    """Se lanza cuando la entrada contiene un símbolo que no pertenece al alfabeto."""

    def __init__(self, lexema, linea, columna):
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
        super().__init__(
            f"Error léxico (línea {linea}, columna {columna}): "
            f"símbolo no reconocido '{lexema}'."
        )


def analizador_lexico(cadena):
    """
    Convierte una cadena de entrada en una lista de tokens.

    Retorna:
        [Token(tipo, lexema, linea, columna), ...]
    Lanza:
        ErrorLexico si encuentra un símbolo fuera del alfabeto.
    """
    tokens = []
    linea = 1
    inicio_linea = 0  # índice donde empieza la línea actual

    for coincidencia in PATRON.finditer(cadena):
        tipo = coincidencia.lastgroup
        lexema = coincidencia.group()
        columna = coincidencia.start() - inicio_linea + 1

        if tipo == 'SALTO':
            linea += 1
            inicio_linea = coincidencia.end()
            continue

        if tipo == 'ESPACIO':
            continue

        if tipo == 'ID' and lexema.upper() in PALABRAS_RESERVADAS:
            tipo = lexema.upper()

        elif tipo == 'ERROR':
            raise ErrorLexico(lexema, linea, columna)

        tokens.append(Token(tipo, lexema, linea, columna))

    return tokens


if __name__ == '__main__':
    entrada = "WHEN vida < 20 AND NOT jefe_cerca THEN usar pocion(1, TRUE);"
    for token in analizador_lexico(entrada):
        print(token)
