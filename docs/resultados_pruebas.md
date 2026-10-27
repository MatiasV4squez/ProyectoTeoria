| # | Tipo | Entrada | Resultado esperado | Resultado obtenido | Observación |
|---|---|---|---|---|---|
| 1 | Válida | `WHEN vida < 20 THEN usar pocion;` | VÁLIDA | VÁLIDA | Regla simple con verbo y objeto |
| 2 | Válida | `WHEN enemigos > 3 AND municion == 0 THEN huir;` | VÁLIDA | VÁLIDA | Condición con AND; acción sin objeto |
| 3 | Válida | `WHEN NOT escudo_activo THEN activar escudo(10);` | VÁLIDA | VÁLIDA | Extensión: NOT y acción con un parámetro |
| 4 | Válida | `WHEN (vida < 30 OR veneno == TRUE) AND NOT jefe_cerca THEN curar jugador(25, FALSE);` | VÁLIDA | VÁLIDA | Extensión: paréntesis, OR, AND, NOT y varios parámetros |
| 5 | Válida | `WHEN puntos >= 1000 THEN subir nivel; WHEN tiempo == 0 THEN terminar partida;` | VÁLIDA | VÁLIDA | Programa con dos reglas |
| 6 | Válida | `WHEN oro >= 500 OR nivel != 1 THEN comprar espada(oro, 1);` | VÁLIDA | VÁLIDA | OR con operadores >= y !=; parámetro identificador |
| 7 | Válida | `WHEN distancia <= 5 AND arma_cargada == TRUE OR modo_furia THEN atacar enemigo(3);` | VÁLIDA | VÁLIDA | AND y OR combinados sin paréntesis (precedencia) |
| 8 | Válida | `WHEN NOT (vida > 50 AND escudo > 0) THEN defender;` | VÁLIDA | VÁLIDA | Extensión: NOT aplicado a un grupo |
| 9 | Válida | `WHEN vida < vida_maxima THEN regenerar(2, TRUE, velocidad);` | VÁLIDA | VÁLIDA | Comparación entre identificadores; tres parámetros |
| 10 | Válida | `WHEN jefe_derrotado == TRUE THEN abrir puerta; WHEN llave == FALSE THEN mostrar mensaje(404); WHEN vidas == 0 THEN game_over;` | VÁLIDA | VÁLIDA | Programa con tres reglas |
| 11 | Inválida | `WHEN vida < THEN huir;` | INVÁLIDA | INVÁLIDA | Falta el valor después del operador. Error sintáctico (línea 1, columna 13): se esperaba un valor (número, TRUE, FALSE o identificador) después de '<', pero se encontró 'THEN'. |
| 12 | Inválida | `WHEN vida < 20 usar pocion;` | INVÁLIDA | INVÁLIDA | Falta THEN. Error sintáctico (línea 1, columna 16): se esperaba AND, OR o la palabra reservada THEN después de '20', pero se encontró 'usar'. |
| 13 | Inválida | `WHEN vida < 20 THEN usar pocion` | INVÁLIDA | INVÁLIDA | Falta ';' al final. Error sintáctico (línea 1, columna 32): se esperaba '(' o ';' después de 'pocion', pero se encontró el fin de la entrada. |
| 14 | Inválida | `WHEN (vida < 20 THEN huir;` | INVÁLIDA | INVÁLIDA | Paréntesis sin cerrar. Error sintáctico (línea 1, columna 17): se esperaba ')' para cerrar el '(' de la línea 1, columna 6, después de '20', pero se encontró 'THEN'. |
| 15 | Inválida | `WHEN vida < 20 AND THEN huir;` | INVÁLIDA | INVÁLIDA | AND sin operando derecho. Error sintáctico (línea 1, columna 20): se esperaba una condición (un identificador, NOT o '(') después de 'AND', pero se encontró 'THEN'. |
| 16 | Inválida | `WHEN vida < 20 THEN atacar();` | INVÁLIDA | INVÁLIDA | Lista de parámetros vacía. Error sintáctico (línea 1, columna 28): se esperaba al menos un parámetro (número, TRUE, FALSE o identificador) después de '(', pero se encontró ')'. |
| 17 | Inválida | `THEN huir;` | INVÁLIDA | INVÁLIDA | La regla no empieza con WHEN. Error sintáctico (línea 1, columna 1): se esperaba la palabra reservada WHEN al inicio de la regla, pero se encontró 'THEN'. |
| 18 | Inválida | `WHEN vida > 20) THEN huir;` | INVÁLIDA | INVÁLIDA | Paréntesis ')' sin abrir. Error sintáctico (línea 1, columna 15): se esperaba la palabra reservada THEN después de '20', pero se encontró ')'. |
| 19 | Inválida | `WHEN vida < 20 THEN atacar(1,);` | INVÁLIDA | INVÁLIDA | Coma sin parámetro siguiente. Error sintáctico (línea 1, columna 30): se esperaba un valor (número, TRUE, FALSE o identificador) después de ',', pero se encontró ')'. |
| 20 | Inválida | `WHEN vida == 0 THEN usar pocion grande;` | INVÁLIDA | INVÁLIDA | Acción con dos objetos. Error sintáctico (línea 1, columna 33): se esperaba '(' o ';' después de 'pocion', pero se encontró 'grande'. |
| 21 | Inválida | `WHEN vida < 20.5 THEN huir;` | INVÁLIDA | INVÁLIDA | Error léxico: '.' no pertenece al alfabeto. Error léxico (línea 1, columna 15): símbolo no reconocido '.'. |
| 22 | Límite | _(vacía)_ | INVÁLIDA | INVÁLIDA | Entrada vacía: un programa necesita al menos una regla. Error sintáctico (línea 1, columna 1): se esperaba la palabra reservada WHEN al inicio de la regla, pero se encontró el fin de la entrada. |
| 23 | Límite | `WHEN a THEN b;` | VÁLIDA | VÁLIDA | Regla mínima: variable booleana y acción de una palabra |
| 24 | Límite | `WHEN NOT NOT NOT alerta THEN huir;` | VÁLIDA | VÁLIDA | NOT encadenado varias veces |
| 25 | Límite | `WHEN ((((vida < 10)))) THEN huir;` | VÁLIDA | VÁLIDA | Paréntesis anidados en varios niveles |
| 26 | Límite | `when vida < 20 then huir;` | VÁLIDA | VÁLIDA | Palabras reservadas en minúsculas |
| 27 | Límite | `WHEN vida < 20 ⏎   AND enemigos > 2 ⏎ THEN ⏎   huir;` | VÁLIDA | VÁLIDA | Regla escrita en varias líneas |
| 28 | Límite | `WHEN TRUE THEN huir;` | INVÁLIDA | INVÁLIDA | Una condición no puede ser solo un valor. Error sintáctico (línea 1, columna 6): se esperaba una condición (un identificador, NOT o '(') después de 'WHEN', pero se encontró 'TRUE'. |
| 29 | Límite | `WHEN vida < 20 < 30 THEN huir;` | INVÁLIDA | INVÁLIDA | Comparación encadenada. Error sintáctico (línea 1, columna 16): se esperaba AND, OR o la palabra reservada THEN después de '20', pero se encontró '<'. |
| 30 | Límite | `WHEN a > 1 THEN x y z; WHEN b THEN ok; WHEN c 5 THEN r;` | INVÁLIDA | INVÁLIDA | Recuperación de errores: informa los 2 errores y analiza la regla correcta del medio. Error sintáctico (línea 1, columna 21): se esperaba '(' o ';' después de 'y', pero se encontró 'z'. \| Error sintáctico (línea 1, columna 47): se esperaba un operador relacional, AND, OR o la palabra reservada THEN después de 'c', pero se encontró '5'. |
