"""
Ejecuta los casos de prueba de GameRules (definidos en casos.py), compara el
resultado esperado con el obtenido y muestra un resumen.

Uso (desde la carpeta raíz del proyecto):
    python pruebas/ejecutar_pruebas.py              # resultados en la terminal
    python pruebas/ejecutar_pruebas.py --markdown   # además genera docs/resultados_pruebas.md
"""

import os
import sys

# Permite importar el paquete gamerules al ejecutar este archivo directamente.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from gamerules.sintactico import analizar
from casos import CASOS, VALIDA, INVALIDA


def ejecutar():
    resultados = []
    for categoria, entrada, esperado, descripcion in CASOS:
        arbol, errores = analizar(entrada)
        obtenido = VALIDA if not errores else INVALIDA
        detalle = 'Aceptada' if not errores else ' | '.join(str(e) for e in errores)
        resultados.append((categoria, entrada, esperado, obtenido, descripcion, detalle))
    return resultados


def mostrar(resultados):
    for i, (categoria, entrada, esperado, obtenido, descripcion, detalle) in enumerate(resultados, 1):
        marca = '✔' if esperado == obtenido else '✘ FALLA'
        print(f'[{i:02}] {marca}  ({categoria}) {descripcion}')
        print(f'     Entrada:   {entrada!r}')
        print(f'     Esperado:  {esperado}   Obtenido: {obtenido}')
        if obtenido == INVALIDA:
            for linea in detalle.split(' | '):
                print(f'     {linea}')
        print()


def generar_markdown(resultados, ruta=os.path.join(RAIZ, 'docs', 'resultados_pruebas.md')):
    def celda(texto):
        return texto.replace('|', '\\|').replace('\n', ' ⏎ ')

    lineas = ['| # | Tipo | Entrada | Resultado esperado | Resultado obtenido | Observación |',
              '|---|---|---|---|---|---|']
    for i, (categoria, entrada, esperado, obtenido, descripcion, detalle) in enumerate(resultados, 1):
        entrada_md = f'`{celda(entrada)}`' if entrada else '_(vacía)_'
        observacion = celda(descripcion if obtenido == VALIDA else f'{descripcion}. {detalle}')
        lineas.append(f'| {i} | {categoria} | {entrada_md} | {esperado} | {obtenido} | {observacion} |')
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas) + '\n')
    print(f'Tabla guardada en {ruta}')


def main():
    resultados = ejecutar()
    mostrar(resultados)

    correctas = sum(1 for r in resultados if r[2] == r[3])
    print(f'Resultado: {correctas}/{len(resultados)} pruebas correctas.')

    if '--markdown' in sys.argv:
        generar_markdown(resultados)

    sys.exit(0 if correctas == len(resultados) else 1)


if __name__ == '__main__':
    main()
