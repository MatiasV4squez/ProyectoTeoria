"""
Verificación de la parte teórica.

Calcula automáticamente FIRST, FOLLOW y la tabla LL(1) de la gramática final
para comprobar los cálculos hechos a mano en el informe (secciones 5 y 6).
Este módulo NO lo usa el parser: el parser está escrito a mano en sintactico.py.

Uso:
    python -m gamerules.gramatica
"""

EPS = 'ε'
FIN = '$'
INICIAL = '<programa>'

# (número, lado izquierdo, lado derecho). [] representa ε.
PRODUCCIONES = [
    (1,  '<programa>',    ['<regla>', "<programa'>"]),
    (2,  "<programa'>",   ['<regla>', "<programa'>"]),
    (3,  "<programa'>",   []),
    (4,  '<regla>',       ['WHEN', '<condicion>', 'THEN', '<accion>', ';']),
    (5,  '<condicion>',   ['<termino>', "<condicion'>"]),
    (6,  "<condicion'>",  ['OR', '<termino>', "<condicion'>"]),
    (7,  "<condicion'>",  []),
    (8,  '<termino>',     ['<factor>', "<termino'>"]),
    (9,  "<termino'>",    ['AND', '<factor>', "<termino'>"]),
    (10, "<termino'>",    []),
    (11, '<factor>',      ['NOT', '<factor>']),
    (12, '<factor>',      ['(', '<condicion>', ')']),
    (13, '<factor>',      ['ID', '<comparacion>']),
    (14, '<comparacion>', ['OP_REL', '<valor>']),
    (15, '<comparacion>', []),
    (16, '<valor>',       ['NUM']),
    (17, '<valor>',       ['TRUE']),
    (18, '<valor>',       ['FALSE']),
    (19, '<valor>',       ['ID']),
    (20, '<accion>',      ['ID', '<objeto>', '<parametros>']),
    (21, '<objeto>',      ['ID']),
    (22, '<objeto>',      []),
    (23, '<parametros>',  ['(', '<argumentos>', ')']),
    (24, '<parametros>',  []),
    (25, '<argumentos>',  ['<valor>', "<argumentos'>"]),
    (26, "<argumentos'>", [',', '<valor>', "<argumentos'>"]),
    (27, "<argumentos'>", []),
]

NO_TERMINALES = list(dict.fromkeys(izq for _, izq, _ in PRODUCCIONES))
TERMINALES = ['WHEN', 'THEN', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE',
              'ID', 'NUM', 'OP_REL', '(', ')', ',', ';']


def first_de_cadena(simbolos, first):
    """FIRST de una secuencia de símbolos."""
    resultado = set()
    for s in simbolos:
        f = first[s] if s in first else {s}
        resultado |= f - {EPS}
        if EPS not in f:
            return resultado
    resultado.add(EPS)
    return resultado


def calcular_first():
    first = {nt: set() for nt in NO_TERMINALES}
    cambio = True
    while cambio:
        cambio = False
        for _, izq, der in PRODUCCIONES:
            nuevo = first_de_cadena(der, first)
            if not nuevo <= first[izq]:
                first[izq] |= nuevo
                cambio = True
    return first


def calcular_follow(first):
    follow = {nt: set() for nt in NO_TERMINALES}
    follow[INICIAL].add(FIN)
    cambio = True
    while cambio:
        cambio = False
        for _, izq, der in PRODUCCIONES:
            for i, s in enumerate(der):
                if s not in follow:
                    continue
                resto = first_de_cadena(der[i + 1:], first)
                nuevo = resto - {EPS}
                if EPS in resto:
                    nuevo |= follow[izq]
                if not nuevo <= follow[s]:
                    follow[s] |= nuevo
                    cambio = True
    return follow


def construir_tabla(first, follow):
    """Retorna (tabla, conflictos). tabla[(A, a)] es la lista de producciones."""
    tabla = {}
    for num, izq, der in PRODUCCIONES:
        f = first_de_cadena(der, first)
        destinos = f - {EPS}
        if EPS in f:
            destinos |= follow[izq]
        for a in destinos:
            tabla.setdefault((izq, a), []).append(num)
    conflictos = {k: v for k, v in tabla.items() if len(v) > 1}
    return tabla, conflictos


def formatear(conjunto):
    orden = TERMINALES + [FIN, EPS]
    return '{ ' + ', '.join(sorted(conjunto, key=orden.index)) + ' }'


def main():
    first = calcular_first()
    follow = calcular_follow(first)
    tabla, conflictos = construir_tabla(first, follow)

    ancho = max(len(nt) for nt in NO_TERMINALES)

    print('FIRST')
    for nt in NO_TERMINALES:
        print(f'  {nt:<{ancho}}  {formatear(first[nt])}')

    print('\nFOLLOW')
    for nt in NO_TERMINALES:
        print(f'  {nt:<{ancho}}  {formatear(follow[nt])}')

    print('\nTABLA LL(1)')
    columnas = TERMINALES + [FIN]
    print(' ' * (ancho + 2) + ''.join(f'{c:>7}' for c in columnas))
    for nt in NO_TERMINALES:
        celdas = []
        for c in columnas:
            prods = tabla.get((nt, c), [])
            celdas.append(f"{'/'.join(map(str, prods)):>7}")
        print(f'  {nt:<{ancho}}' + ''.join(celdas))

    print()
    if conflictos:
        print('La gramática NO es LL(1). Conflictos:')
        for (nt, a), prods in conflictos.items():
            print(f'  M[{nt}, {a}] = {prods}')
    else:
        print('La gramática es LL(1): ninguna celda tiene más de una producción.')


if __name__ == '__main__':
    main()
