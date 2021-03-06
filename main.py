#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pythones.net
import copy
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

#Inicializa el tablero en función de los parámetros recibidos
def Inicializar(turno, estado):
    n = 8
    filas=[]
    columnas=[]
    for x in range(8):
        filas=[]
        for y in range(8):
            filas.append(estado[(x*n)+y])
        columnas.append(filas)
    tablero=columnas

    minEvaltablero = -1
    maxEvaltablero = n * n + 4 * n + 4 + 1
    direccion_x = [-1, 0, 1, -1, 1, -1, 0, 1]
    direccion_y = [-1, -1, -1, 0, 0, 1, 1, 1]
    
    nivel = 3
    (x, y) = MejorJugada(tablero, turno, n, direccion_x,direccion_y,nivel, minEvaltablero, maxEvaltablero)
    if not (x == -1 and y == -1):
        (tablero, puntos_acumulados) = Mover(tablero, x, y, turno, direccion_x, direccion_y, n)

    res=str(y)+str(x)
    return res

#Valida qeu los movimiento se puedan realizar
def Validar(tablero, x, y, jugador, n, direccion_x, direccion_y):
    if x < 0 or x > n - 1 or y < 0 or y > n - 1:
        return False
    if tablero[y][x] != '2':
        return False
    (tableroTemp, puntos_acumulados) = Mover(copy.deepcopy(tablero), x, y, jugador, direccion_x, direccion_y, n)
    if puntos_acumulados == 0:
        return False
    return True

#Evaluación del tablero
def Evaltablero(tablero, jugador, n):
    total = 0
    for y in range(n):
        for x in range(n):
            if tablero[y][x] == jugador:
                if (x == 0 or x == n - 1) and (y == 0 or y == n - 1):
                    total += 4
                elif (x == 0 or x == n - 1) or (y == 0 or y == n - 1):
                    total += 2
                else:
                    total += 1
    return total

#Evalua si un nodo es una hoja
def EsHoja(tablero, jugador, n, direccion_x, direccion_y):
    for y in range(n):
        for x in range(n):
            if Validar(tablero, x, y, jugador, n, direccion_x, direccion_y):
                return False
    return True

#Define la mejor jugada
def MejorJugada(tablero, jugador, n, direccion_x,direccion_y,nivel, minEvaltablero, maxEvaltablero):
    Maximo = 0
    mx = -1; my = -1
    for y in range(n):
        for x in range(n):
            if Validar(tablero, x, y, jugador, n, direccion_x, direccion_y):
                (tableroTemp, puntos_acumulados) = Mover(copy.deepcopy(tablero), x, y, jugador, direccion_x, direccion_y, n)
                points = Minimax(tableroTemp, jugador, nivel, True, n, direccion_x, direccion_y, minEvaltablero, maxEvaltablero)
                if points > Maximo:
                    Maximo = points
                    mx = x; my = y
    return (mx, my)

#Definición del algoritmo MinMax
def Minimax(tablero, jugador, nivel, maximizingPlayer, n, direccion_x, direccion_y, minEvaltablero, maxEvaltablero):
    if nivel == 0 or EsHoja(tablero, jugador, n, direccion_x, direccion_y):
        return Evaltablero(tablero, jugador, n)
    if maximizingPlayer:
        bestValue = minEvaltablero
        for y in range(n):
            for x in range(n):
                if Validar(tablero, x, y, jugador, n, direccion_x, direccion_y):
                    (tableroTemp, puntos_acumulados) = Mover(copy.deepcopy(tablero), x, y, jugador, direccion_x, direccion_y, n)
                    v = Minimax(tableroTemp, jugador, nivel - 1, False, n, direccion_x, direccion_y, minEvaltablero, maxEvaltablero)
                    bestValue = max(bestValue, v)
    else:
        bestValue = maxEvaltablero
        for y in range(n):
            for x in range(n):
                if Validar(tablero, x, y, jugador, n, direccion_x, direccion_y):
                    (tableroTemp, puntos_acumulados) = Mover(copy.deepcopy(tablero), x, y, jugador, direccion_x, direccion_y, n)
                    v = Minimax(tableroTemp, jugador, nivel - 1, True, n, direccion_x, direccion_y, minEvaltablero, maxEvaltablero)
                    bestValue = min(bestValue, v)
    return bestValue

#Muevo 
def Mover(tablero, x, y, jugador, direccion_x, direccion_y, n):
    puntos_acumulados = 0
    tablero[y][x] = jugador
    for d in range(8):
        ctr = 0
        for i in range(8):
            dx = x + direccion_x[d] * (i + 1)
            dy = y + direccion_y[d] * (i + 1)
            if dx < 0 or dx > n - 1 or dy < 0 or dy > n - 1:
                ctr = 0; break
            elif tablero[dy][dx] == jugador:
                break
            elif tablero[dy][dx] == '2':
                ctr = 0; break
            else:
                ctr += 1
        for i in range(ctr):
            dx = x + direccion_x[d] * (i + 1)
            dy = y + direccion_y[d] * (i + 1)
            tablero[dy][dx] = jugador
        puntos_acumulados += ctr
    return (tablero, puntos_acumulados)

@app.route("/calcular", methods=['GET'])
def MinMaxApi():
    try:
        estado = request.args.get('estado')
        turno = request.args.get('turno')
        result= Inicializar(str(turno), str(estado))
        print(result)
        return result
    except:
        print('error fatal')
        return '00'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
