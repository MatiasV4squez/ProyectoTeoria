# GameRules: analizador sintáctico LL(1)

Proyecto de **Teoría de la Computación (INFO1148)**. Es un analizador sintáctico predictivo por descenso recursivo, escrito a mano en Python, para **GameRules**, un lenguaje de dominio específico que describe reglas de comportamiento de personajes en videojuegos.

```
WHEN vida < 20 AND NOT jefe_cerca THEN usar pocion(1);
WHEN (enemigos > 3 OR municion == 0) AND escudo_activo == FALSE THEN huir;
```

## Requisitos

- **Python 3.8 o superior**. No usa bibliotecas externas.
- *(Opcional)* [Graphviz](https://graphviz.org/download/), para convertir el árbol sintáctico en imagen.

## Estructura del proyecto

```
Proyecto01/
├── main.py                    Programa principal (línea de comandos y modo interactivo)
├── README.md
├── gamerules/                 Código del analizador
│   ├── __init__.py
│   ├── lexico.py              Analizador léxico: texto → tokens (con línea y columna)
│   ├── sintactico.py          Parser LL(1) por descenso recursivo: un método por no terminal
│   ├── arbol.py               Árbol sintáctico: impresión en texto y exportación a Graphviz
│   └── gramatica.py           Verificación de FIRST, FOLLOW y tabla LL(1)
├── pruebas/
│   ├── casos.py               30 casos de prueba (válidos, inválidos y límite)
│   └── ejecutar_pruebas.py    Ejecuta los casos y muestra el resultado
├── ejemplos/                  Programas de ejemplo (.gr)
│   ├── valido.gr
│   ├── invalido.gr
│   └── arbol.gr
└── docs/
    ├── informe.md             Informe del proyecto
    ├── resultados_pruebas.md  Tabla de pruebas generada automáticamente
    ├── img/                   Árbol sintáctico de ejemplo (DOT y PNG)
    └── enunciado/             Enunciado, rúbrica y léxico original del docente
```

Todos los comandos se ejecutan **desde la carpeta raíz** del proyecto.

## Ejecución

### Analizar una regla escrita en la línea de comandos

```bash
python main.py "WHEN vida < 20 THEN usar pocion;"
```

### Analizar un archivo

```bash
python main.py -f ejemplos/valido.gr
python main.py -f ejemplos/invalido.gr
```

### Modo interactivo

```bash
python main.py
GameRules> WHEN vida < 20 THEN huir;
```

### Opciones

| Opción | Efecto |
|---|---|
| `--tokens` | Muestra la lista de tokens generada por el léxico |
| `--epsilon` | Muestra los nodos ε en el árbol |
| `--dot ARCHIVO` | Guarda el árbol en formato DOT de Graphviz |

Para generar la imagen del árbol:

```bash
python main.py -f ejemplos/arbol.gr --dot arbol.dot
dot -Tpng arbol.dot -o arbol.png
```

### Pruebas

```bash
python pruebas/ejecutar_pruebas.py              # ejecuta los 30 casos
python pruebas/ejecutar_pruebas.py --markdown   # además genera docs/resultados_pruebas.md
```

### Verificar FIRST, FOLLOW y la tabla LL(1)

```bash
python -m gamerules.gramatica
```

## Formato de entrada

Un programa es una secuencia de **una o más reglas**, cada una terminada en `;`. Los espacios y saltos de línea se ignoran, y las palabras reservadas no distinguen mayúsculas de minúsculas.

```
WHEN <condición> THEN <acción> [<objeto>] [( <parámetro>, ... )] ;
```

- **Condición:** comparaciones `variable OP valor` o variables booleanas solas, combinadas con `AND`, `OR`, `NOT` y paréntesis. La precedencia es `NOT > AND > OR`.
- **Operadores relacionales:** `>`, `<`, `>=`, `<=`, `==`, `!=`
- **Valores:** números enteros, `TRUE`, `FALSE` o identificadores.
- **Acción:** un verbo, un objeto opcional y parámetros opcionales entre paréntesis.

## Ejemplos de salida

Entrada válida:

```
$ python main.py "WHEN a > 1 THEN huir;"
✔ Entrada sintácticamente válida.

Árbol sintáctico:
<programa>
├── <regla>
│   ├── WHEN
│   ├── <condicion>
│   │   ├── <termino>
│   │   │   ├── <factor>
│   │   │   │   ├── ID: a
│   │   │   │   └── <comparacion>
│   │   │   │       ├── OP_REL: >
│   │   │   │       └── <valor>
│   │   │   │           └── NUM: 1
...
```

Entrada inválida:

```
$ python main.py "WHEN vida < THEN huir;"
✘ Entrada inválida (1 error(es)):
  Error sintáctico (línea 1, columna 13): se esperaba un valor (número, TRUE, FALSE o identificador) después de '<', pero se encontró 'THEN'.
```

Si una entrada tiene varias reglas con errores, el parser los informa todos: al encontrar un error salta hasta el siguiente `;` o `WHEN` y sigue analizando.
