"""
Casos de prueba de GameRules: 10 válidos, 11 inválidos y 9 casos límite.

Cada caso es (categoría, entrada, resultado esperado, descripción).
"""

VALIDA = 'VÁLIDA'
INVALIDA = 'INVÁLIDA'

# (categoría, entrada, resultado esperado, descripción)
CASOS = [
    # ---------------- Entradas válidas ----------------
    ('Válida', 'WHEN vida < 20 THEN usar pocion;', VALIDA,
     'Regla simple con verbo y objeto'),
    ('Válida', 'WHEN enemigos > 3 AND municion == 0 THEN huir;', VALIDA,
     'Condición con AND; acción sin objeto'),
    ('Válida', 'WHEN NOT escudo_activo THEN activar escudo(10);', VALIDA,
     'Extensión: NOT y acción con un parámetro'),
    ('Válida', 'WHEN (vida < 30 OR veneno == TRUE) AND NOT jefe_cerca THEN curar jugador(25, FALSE);', VALIDA,
     'Extensión: paréntesis, OR, AND, NOT y varios parámetros'),
    ('Válida', 'WHEN puntos >= 1000 THEN subir nivel; WHEN tiempo == 0 THEN terminar partida;', VALIDA,
     'Programa con dos reglas'),
    ('Válida', 'WHEN oro >= 500 OR nivel != 1 THEN comprar espada(oro, 1);', VALIDA,
     'OR con operadores >= y !=; parámetro identificador'),
    ('Válida', 'WHEN distancia <= 5 AND arma_cargada == TRUE OR modo_furia THEN atacar enemigo(3);', VALIDA,
     'AND y OR combinados sin paréntesis (precedencia)'),
    ('Válida', 'WHEN NOT (vida > 50 AND escudo > 0) THEN defender;', VALIDA,
     'Extensión: NOT aplicado a un grupo'),
    ('Válida', 'WHEN vida < vida_maxima THEN regenerar(2, TRUE, velocidad);', VALIDA,
     'Comparación entre identificadores; tres parámetros'),
    ('Válida', 'WHEN jefe_derrotado == TRUE THEN abrir puerta; WHEN llave == FALSE THEN mostrar mensaje(404); WHEN vidas == 0 THEN game_over;', VALIDA,
     'Programa con tres reglas'),

    # ---------------- Entradas inválidas ----------------
    ('Inválida', 'WHEN vida < THEN huir;', INVALIDA,
     'Falta el valor después del operador'),
    ('Inválida', 'WHEN vida < 20 usar pocion;', INVALIDA,
     'Falta THEN'),
    ('Inválida', 'WHEN vida < 20 THEN usar pocion', INVALIDA,
     "Falta ';' al final"),
    ('Inválida', 'WHEN (vida < 20 THEN huir;', INVALIDA,
     'Paréntesis sin cerrar'),
    ('Inválida', 'WHEN vida < 20 AND THEN huir;', INVALIDA,
     'AND sin operando derecho'),
    ('Inválida', 'WHEN vida < 20 THEN atacar();', INVALIDA,
     'Lista de parámetros vacía'),
    ('Inválida', 'THEN huir;', INVALIDA,
     'La regla no empieza con WHEN'),
    ('Inválida', 'WHEN vida > 20) THEN huir;', INVALIDA,
     "Paréntesis ')' sin abrir"),
    ('Inválida', 'WHEN vida < 20 THEN atacar(1,);', INVALIDA,
     'Coma sin parámetro siguiente'),
    ('Inválida', 'WHEN vida == 0 THEN usar pocion grande;', INVALIDA,
     'Acción con dos objetos'),
    ('Inválida', 'WHEN vida < 20.5 THEN huir;', INVALIDA,
     "Error léxico: '.' no pertenece al alfabeto"),

    # ---------------- Casos límite ----------------
    ('Límite', '', INVALIDA,
     'Entrada vacía: un programa necesita al menos una regla'),
    ('Límite', 'WHEN a THEN b;', VALIDA,
     'Regla mínima: variable booleana y acción de una palabra'),
    ('Límite', 'WHEN NOT NOT NOT alerta THEN huir;', VALIDA,
     'NOT encadenado varias veces'),
    ('Límite', 'WHEN ((((vida < 10)))) THEN huir;', VALIDA,
     'Paréntesis anidados en varios niveles'),
    ('Límite', 'when vida < 20 then huir;', VALIDA,
     'Palabras reservadas en minúsculas'),
    ('Límite', 'WHEN vida < 20\n  AND enemigos > 2\nTHEN\n  huir;', VALIDA,
     'Regla escrita en varias líneas'),
    ('Límite', 'WHEN TRUE THEN huir;', INVALIDA,
     'Una condición no puede ser solo un valor'),
    ('Límite', 'WHEN vida < 20 < 30 THEN huir;', INVALIDA,
     'Comparación encadenada'),
    ('Límite', 'WHEN a > 1 THEN x y z; WHEN b THEN ok; WHEN c 5 THEN r;', INVALIDA,
     'Recuperación de errores: informa los 2 errores y analiza la regla correcta del medio'),
]
