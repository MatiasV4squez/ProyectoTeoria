"""
Analizador sintáctico predictivo LL(1) de GameRules, por descenso recursivo.

Cada no terminal de la gramática (sección 3.2 del informe) es un método de la
clase Parser. Cada método mira el token actual y decide qué producción
aplicar, exactamente como indica la tabla LL(1) (sección 6.2). Los números
de producción aparecen en los comentarios para relacionar el código con la
gramática.

Gramática final:
     1  <programa>     → <regla> <programa'>
     2  <programa'>    → <regla> <programa'>
     3  <programa'>    → ε
     4  <regla>        → WHEN <condicion> THEN <accion> ;
     5  <condicion>    → <termino> <condicion'>
     6  <condicion'>   → OR <termino> <condicion'>
     7  <condicion'>   → ε
     8  <termino>      → <factor> <termino'>
     9  <termino'>     → AND <factor> <termino'>
    10  <termino'>     → ε
    11  <factor>       → NOT <factor>
    12  <factor>       → ( <condicion> )
    13  <factor>       → ID <comparacion>
    14  <comparacion>  → OP_REL <valor>
    15  <comparacion>  → ε
    16  <valor>        → NUM
    17  <valor>        → TRUE
    18  <valor>        → FALSE
    19  <valor>        → ID
    20  <accion>       → ID <objeto> <parametros>
    21  <objeto>       → ID
    22  <objeto>       → ε
    23  <parametros>   → ( <argumentos> )
    24  <parametros>   → ε
    25  <argumentos>   → <valor> <argumentos'>
    26  <argumentos'>  → , <valor> <argumentos'>
    27  <argumentos'>  → ε
"""

from .arbol import Nodo
from .lexico import Token, ErrorLexico, analizador_lexico

# FIRST y FOLLOW usados para decidir (secciones 5.1 y 5.2 del informe).
FIRST_VALOR = {'NUM', 'TRUE', 'FALSE', 'ID'}
FOLLOW_CONDICION_PRIMA = {'THEN', 'PARENT_DER'}
FOLLOW_TERMINO_PRIMA = {'OR', 'THEN', 'PARENT_DER'}
FOLLOW_COMPARACION = {'AND', 'OR', 'THEN', 'PARENT_DER'}
FOLLOW_OBJETO = {'PARENT_IZQ', 'PUNTO_COMA'}
FOLLOW_PARAMETROS = {'PUNTO_COMA'}
FOLLOW_ARGUMENTOS_PRIMA = {'PARENT_DER'}

# Tokens donde se reanuda el análisis después de un error (modo pánico):
# ';' termina la regla con error; WHEN y $ forman FOLLOW(<regla>).
TOKENS_SINCRONIZACION = {'PUNTO_COMA', 'WHEN', '$'}

# Cómo se nombra cada tipo de token en los mensajes de error.
DESCRIPCION_TOKEN = {
    'WHEN': 'la palabra reservada WHEN',
    'THEN': 'la palabra reservada THEN',
    'AND': 'AND',
    'OR': 'OR',
    'NOT': 'NOT',
    'TRUE': 'TRUE',
    'FALSE': 'FALSE',
    'ID': 'un identificador',
    'NUM': 'un número',
    'OP_REL': 'un operador relacional',
    'PARENT_IZQ': "'('",
    'PARENT_DER': "')'",
    'COMA': "','",
    'PUNTO_COMA': "';'",
}


class ErrorSintactico(Exception):
    """Error sintáctico con la posición del token donde se detectó."""

    def __init__(self, mensaje, token):
        self.token = token
        super().__init__(
            f"Error sintáctico (línea {token.linea}, columna {token.columna}): {mensaje}"
        )


class Parser:
    """Parser de descenso recursivo: un método por cada no terminal."""

    def __init__(self, tokens):
        # Se agrega el token $ para marcar el fin de la entrada.
        if tokens:
            ultimo = tokens[-1]
            fin = Token('$', '$', ultimo.linea, ultimo.columna + len(ultimo.lexema))
        else:
            fin = Token('$', '$', 1, 1)
        self.tokens = list(tokens) + [fin]
        self.pos = 0
        self.errores = []
        self.parentesis_abiertos = []  # tokens '(' de condiciones aún sin cerrar

    # ------------------------------------------------------------------
    # Funciones auxiliares
    # ------------------------------------------------------------------

    @property
    def actual(self):
        return self.tokens[self.pos]

    def anterior(self):
        return self.tokens[self.pos - 1] if self.pos > 0 else None

    def avanzar(self):
        token = self.actual
        if token.tipo != '$':
            self.pos += 1
        return token

    def coincidir(self, tipo, esperado=None):
        """Consume el token actual si es del tipo indicado; si no, lanza un error."""
        if self.actual.tipo == tipo:
            token = self.avanzar()
            return Nodo(tipo, token)
        raise self.error(esperado or DESCRIPCION_TOKEN[tipo])

    def error(self, esperado):
        """Construye un mensaje del tipo: se esperaba X después de Y, pero se encontró Z."""
        encontrado = ('el fin de la entrada' if self.actual.tipo == '$'
                      else f"'{self.actual.lexema}'")
        mensaje = f"se esperaba {esperado}"
        previo = self.anterior()
        if previo is not None:
            mensaje += f" después de '{previo.lexema}'"
        mensaje += f", pero se encontró {encontrado}."
        return ErrorSintactico(mensaje, self.actual)

    def esperado_fin_condicion(self):
        """Qué puede venir después de una condición, según si hay un '(' abierto."""
        if self.parentesis_abiertos:
            return "AND, OR o ')'"
        return "AND, OR o la palabra reservada THEN"

    def sincronizar(self):
        """Recuperación en modo pánico: salta tokens hasta un punto seguro."""
        self.parentesis_abiertos.clear()
        while self.actual.tipo not in TOKENS_SINCRONIZACION:
            self.avanzar()
        if self.actual.tipo == 'PUNTO_COMA':
            self.avanzar()

    # ------------------------------------------------------------------
    # Punto de entrada
    # ------------------------------------------------------------------

    def analizar(self):
        """Analiza toda la entrada. Retorna (arbol, errores); arbol es None si hay errores."""
        arbol = self.programa()
        if self.errores:
            return None, self.errores
        return arbol, []

    # ------------------------------------------------------------------
    # Un método por cada no terminal
    # ------------------------------------------------------------------

    def programa(self):
        # 1: <programa> → <regla> <programa'>
        nodo = Nodo('<programa>')
        nodo.agregar(self.regla_con_recuperacion())
        nodo.agregar(self.programa_prima())
        return nodo

    def programa_prima(self):
        nodo = Nodo("<programa'>")
        if self.actual.tipo == 'WHEN':
            # 2: <programa'> → <regla> <programa'>
            nodo.agregar(self.regla_con_recuperacion())
            nodo.agregar(self.programa_prima())
        elif self.actual.tipo == '$':
            # 3: <programa'> → ε
            nodo.agregar(Nodo('ε'))
        else:
            # M[<programa'>, a] vacío: se reporta y se continúa con la siguiente regla.
            self.errores.append(self.error(
                'la palabra reservada WHEN (inicio de una regla) o el fin de la entrada'))
            self.sincronizar()
            nodo.agregar(self.programa_prima())
        return nodo

    def regla_con_recuperacion(self):
        """Analiza una regla; si tiene un error lo registra y sigue con la siguiente."""
        try:
            return self.regla()
        except ErrorSintactico as e:
            self.errores.append(e)
            self.sincronizar()
            return Nodo('<regla>')

    def regla(self):
        # 4: <regla> → WHEN <condicion> THEN <accion> ;
        nodo = Nodo('<regla>')
        nodo.agregar(self.coincidir('WHEN', 'la palabra reservada WHEN al inicio de la regla'))
        nodo.agregar(self.condicion())
        nodo.agregar(self.coincidir('THEN', 'la palabra reservada THEN'))
        nodo.agregar(self.accion())
        nodo.agregar(self.coincidir('PUNTO_COMA', "';' al final de la regla"))
        return nodo

    def condicion(self):
        # 5: <condicion> → <termino> <condicion'>
        # FIRST(<condicion>) = FIRST(<factor>), así que si el token no sirve
        # el error se detecta y se informa en factor().
        nodo = Nodo('<condicion>')
        nodo.agregar(self.termino())
        nodo.agregar(self.condicion_prima())
        return nodo

    def condicion_prima(self):
        nodo = Nodo("<condicion'>")
        if self.actual.tipo == 'OR':
            # 6: <condicion'> → OR <termino> <condicion'>
            nodo.agregar(self.coincidir('OR'))
            nodo.agregar(self.termino())
            nodo.agregar(self.condicion_prima())
        elif self.actual.tipo in FOLLOW_CONDICION_PRIMA:
            # 7: <condicion'> → ε
            nodo.agregar(Nodo('ε'))
        else:
            raise self.error(self.esperado_fin_condicion())
        return nodo

    def termino(self):
        # 8: <termino> → <factor> <termino'>
        nodo = Nodo('<termino>')
        nodo.agregar(self.factor())
        nodo.agregar(self.termino_prima())
        return nodo

    def termino_prima(self):
        nodo = Nodo("<termino'>")
        if self.actual.tipo == 'AND':
            # 9: <termino'> → AND <factor> <termino'>
            nodo.agregar(self.coincidir('AND'))
            nodo.agregar(self.factor())
            nodo.agregar(self.termino_prima())
        elif self.actual.tipo in FOLLOW_TERMINO_PRIMA:
            # 10: <termino'> → ε
            nodo.agregar(Nodo('ε'))
        else:
            raise self.error(self.esperado_fin_condicion())
        return nodo

    def factor(self):
        nodo = Nodo('<factor>')
        if self.actual.tipo == 'NOT':
            # 11: <factor> → NOT <factor>
            nodo.agregar(self.coincidir('NOT'))
            nodo.agregar(self.factor())
        elif self.actual.tipo == 'PARENT_IZQ':
            # 12: <factor> → ( <condicion> )
            abre = self.actual
            nodo.agregar(self.coincidir('PARENT_IZQ'))
            self.parentesis_abiertos.append(abre)
            nodo.agregar(self.condicion())
            nodo.agregar(self.coincidir(
                'PARENT_DER',
                f"')' para cerrar el '(' de la línea {abre.linea}, columna {abre.columna},"))
            self.parentesis_abiertos.pop()
        elif self.actual.tipo == 'ID':
            # 13: <factor> → ID <comparacion>
            nodo.agregar(self.coincidir('ID'))
            nodo.agregar(self.comparacion())
        else:
            raise self.error("una condición (un identificador, NOT o '(')")
        return nodo

    def comparacion(self):
        nodo = Nodo('<comparacion>')
        if self.actual.tipo == 'OP_REL':
            # 14: <comparacion> → OP_REL <valor>
            nodo.agregar(self.coincidir('OP_REL'))
            nodo.agregar(self.valor())
        elif self.actual.tipo in FOLLOW_COMPARACION:
            # 15: <comparacion> → ε   (variable booleana sin comparar)
            nodo.agregar(Nodo('ε'))
        else:
            raise self.error('un operador relacional, ' + self.esperado_fin_condicion())
        return nodo

    def valor(self):
        # 16–19: <valor> → NUM | TRUE | FALSE | ID
        nodo = Nodo('<valor>')
        if self.actual.tipo in FIRST_VALOR:
            nodo.agregar(self.coincidir(self.actual.tipo))
        else:
            raise self.error('un valor (número, TRUE, FALSE o identificador)')
        return nodo

    def accion(self):
        # 20: <accion> → ID <objeto> <parametros>
        nodo = Nodo('<accion>')
        nodo.agregar(self.coincidir('ID', 'una acción (identificador)'))
        nodo.agregar(self.objeto())
        nodo.agregar(self.parametros())
        return nodo

    def objeto(self):
        nodo = Nodo('<objeto>')
        if self.actual.tipo == 'ID':
            # 21: <objeto> → ID
            nodo.agregar(self.coincidir('ID'))
        elif self.actual.tipo in FOLLOW_OBJETO:
            # 22: <objeto> → ε
            nodo.agregar(Nodo('ε'))
        else:
            raise self.error("un objeto (identificador), '(' o ';'")
        return nodo

    def parametros(self):
        nodo = Nodo('<parametros>')
        if self.actual.tipo == 'PARENT_IZQ':
            # 23: <parametros> → ( <argumentos> )
            nodo.agregar(self.coincidir('PARENT_IZQ'))
            nodo.agregar(self.argumentos())
            nodo.agregar(self.coincidir('PARENT_DER', "')' para cerrar los parámetros"))
        elif self.actual.tipo in FOLLOW_PARAMETROS:
            # 24: <parametros> → ε
            nodo.agregar(Nodo('ε'))
        else:
            raise self.error("'(' o ';'")
        return nodo

    def argumentos(self):
        # 25: <argumentos> → <valor> <argumentos'>
        nodo = Nodo('<argumentos>')
        if self.actual.tipo not in FIRST_VALOR:
            raise self.error('al menos un parámetro (número, TRUE, FALSE o identificador)')
        nodo.agregar(self.valor())
        nodo.agregar(self.argumentos_prima())
        return nodo

    def argumentos_prima(self):
        nodo = Nodo("<argumentos'>")
        if self.actual.tipo == 'COMA':
            # 26: <argumentos'> → , <valor> <argumentos'>
            nodo.agregar(self.coincidir('COMA'))
            nodo.agregar(self.valor())
            nodo.agregar(self.argumentos_prima())
        elif self.actual.tipo in FOLLOW_ARGUMENTOS_PRIMA:
            # 27: <argumentos'> → ε
            nodo.agregar(Nodo('ε'))
        else:
            raise self.error("',' o ')'")
        return nodo


def analizar(texto):
    """
    Analiza un texto completo (léxico + sintáctico).

    Retorna (arbol, errores):
      - entrada válida:   (Nodo raíz, [])
      - entrada inválida: (None, [lista de errores léxicos o sintácticos])
    """
    try:
        tokens = analizador_lexico(texto)
    except ErrorLexico as e:
        return None, [e]
    return Parser(tokens).analizar()
