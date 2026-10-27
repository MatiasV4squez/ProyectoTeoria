"""
Árbol sintáctico (árbol de derivación) de GameRules.

Cada nodo interno corresponde a un no terminal de la gramática y cada hoja
a un terminal (token) o a ε. El árbol se puede mostrar como texto
jerárquico o exportar a formato DOT de Graphviz.
"""


class Nodo:
    """Nodo del árbol sintáctico."""

    def __init__(self, simbolo, token=None):
        self.simbolo = simbolo  # '<regla>', 'WHEN', 'ID', 'ε', ...
        self.token = token      # Token del léxico (solo en las hojas terminales)
        self.hijos = []

    def agregar(self, hijo):
        self.hijos.append(hijo)
        return hijo

    def es_epsilon(self):
        return self.simbolo == 'ε'

    def etiqueta(self):
        """Texto que se muestra para el nodo."""
        if self.token is None:
            return self.simbolo
        # Para tokens cuyo lexema aporta información se muestra el lexema.
        if self.token.tipo in ('ID', 'NUM', 'OP_REL'):
            return f"{self.simbolo}: {self.token.lexema}"
        return self.token.lexema


def imprimir_arbol(nodo, mostrar_epsilon=False):
    """Retorna el árbol como texto jerárquico."""
    lineas = [nodo.etiqueta()]
    _imprimir_hijos(nodo, '', mostrar_epsilon, lineas)
    return '\n'.join(lineas)


def _imprimir_hijos(nodo, prefijo, mostrar_epsilon, lineas):
    hijos = [h for h in nodo.hijos if mostrar_epsilon or not h.es_epsilon()]
    for i, hijo in enumerate(hijos):
        ultimo = i == len(hijos) - 1
        lineas.append(prefijo + ('└── ' if ultimo else '├── ') + hijo.etiqueta())
        _imprimir_hijos(hijo, prefijo + ('    ' if ultimo else '│   '),
                        mostrar_epsilon, lineas)


def exportar_dot(nodo, mostrar_epsilon=False):
    """Retorna el árbol en formato DOT para visualizarlo con Graphviz."""
    lineas = [
        'digraph ArbolSintactico {',
        '    node [fontname="Helvetica"];',
    ]
    contador = [0]

    def visitar(n):
        id_nodo = f'n{contador[0]}'
        contador[0] += 1
        etiqueta = n.etiqueta().replace('\\', '\\\\').replace('"', '\\"')
        if n.token is not None or n.es_epsilon():
            estilo = 'shape=box, style=filled, fillcolor="#e8f0fe"'
        else:
            estilo = 'shape=ellipse'
        lineas.append(f'    {id_nodo} [label="{etiqueta}", {estilo}];')
        for hijo in n.hijos:
            if mostrar_epsilon or not hijo.es_epsilon():
                lineas.append(f'    {id_nodo} -> {visitar(hijo)};')
        return id_nodo

    visitar(nodo)
    lineas.append('}')
    return '\n'.join(lineas)
