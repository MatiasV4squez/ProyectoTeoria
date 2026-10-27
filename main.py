"""
Programa principal de GameRules.

Uso:
    python main.py "WHEN vida < 20 THEN usar pocion;"
    python main.py -f ejemplos/valido.gr
    python main.py                      # modo interactivo

Opciones:
    --tokens      muestra la lista de tokens
    --epsilon     muestra los nodos ε en el árbol
    --dot ARCH    guarda el árbol en formato Graphviz (DOT)
"""

import argparse
import sys

from gamerules.arbol import imprimir_arbol, exportar_dot
from gamerules.lexico import ErrorLexico, analizador_lexico
from gamerules.sintactico import analizar


def procesar(texto, mostrar_tokens=False, mostrar_epsilon=False, archivo_dot=None):
    """Analiza un texto e imprime el resultado. Retorna True si es válido."""
    if mostrar_tokens:
        try:
            print('Tokens:')
            for token in analizador_lexico(texto):
                print(f'  {token.tipo:<11} {token.lexema!r:<14} '
                      f'(línea {token.linea}, columna {token.columna})')
            print()
        except ErrorLexico:
            pass  # el error se informa más abajo

    arbol, errores = analizar(texto)

    if errores:
        print(f'✘ Entrada inválida ({len(errores)} error(es)):')
        for e in errores:
            print(f'  {e}')
        return False

    print('✔ Entrada sintácticamente válida.\n')
    print('Árbol sintáctico:')
    print(imprimir_arbol(arbol, mostrar_epsilon))

    if archivo_dot:
        with open(archivo_dot, 'w', encoding='utf-8') as f:
            f.write(exportar_dot(arbol, mostrar_epsilon))
        print(f'\nÁrbol guardado en {archivo_dot} '
              f'(visualizar con: dot -Tpng {archivo_dot} -o arbol.png)')
    return True


def modo_interactivo(opciones):
    print('GameRules: escriba una o más reglas (línea vacía o Ctrl+D para salir).')
    while True:
        try:
            linea = input('GameRules> ')
        except EOFError:
            print()
            break
        if not linea.strip():
            break
        procesar(linea, opciones.tokens, opciones.epsilon, opciones.dot)
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Analizador sintáctico LL(1) del lenguaje GameRules.')
    parser.add_argument('texto', nargs='?', help='programa a analizar')
    parser.add_argument('-f', '--archivo', help='leer el programa desde un archivo')
    parser.add_argument('--tokens', action='store_true', help='mostrar los tokens')
    parser.add_argument('--epsilon', action='store_true', help='mostrar nodos ε en el árbol')
    parser.add_argument('--dot', metavar='ARCHIVO', help='guardar el árbol en formato DOT')
    opciones = parser.parse_args()

    if opciones.archivo:
        with open(opciones.archivo, encoding='utf-8') as f:
            texto = f.read()
    elif opciones.texto is not None:
        texto = opciones.texto
    elif sys.stdin.isatty():
        modo_interactivo(opciones)
        return
    else:
        texto = sys.stdin.read()

    valido = procesar(texto, opciones.tokens, opciones.epsilon, opciones.dot)
    sys.exit(0 if valido else 1)


if __name__ == '__main__':
    main()
