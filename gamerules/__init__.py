"""
Paquete GameRules: analizador léxico y sintáctico LL(1) de un lenguaje de
reglas para videojuegos.

Módulos:
    lexico      analizador léxico (texto → tokens)
    sintactico  parser LL(1) por descenso recursivo (tokens → árbol)
    arbol       árbol sintáctico: impresión en texto y exportación a Graphviz
    gramatica   verificación de FIRST, FOLLOW y tabla LL(1)
"""
