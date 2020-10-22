#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pythones.net
import copy
from flask import Flask, render_template, request, redirect
app = Flask(__name__)


def Mover(tablero, x, y, player, dirx, diry, n):
    totctr = 0
    tablero[y][x] = player
    for d in range(8):
        ctr = 0
        for i in range(8):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            if dx < 0 or dx > n - 1 or dy < 0 or dy > n - 1:
                ctr = 0; break
            elif tablero[dy][dx] == player:
                break
            elif tablero[dy][dx] == '2':
                ctr = 0; break
            else:
                ctr += 1
        for i in range(ctr):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            tablero[dy][dx] = player
        totctr += ctr
    return (tablero, totctr)

#Valida qeu los movimiento se puedan realizar
def Validar(tablero, x, y, player, n, dirx, diry):
    if x < 0 or x > n - 1 or y < 0 or y > n - 1:
        return False
    if tablero[y][x] != '2':
        return False
    (tableroTemp, totctr) = Mover(copy.deepcopy(tablero), x, y, player, dirx, diry, n)
    if totctr == 0:
        return False
    return True

def Evaltablero(tablero, player, n):
    tot = 0
    for y in range(n):
        for x in range(n):
            if tablero[y][x] == player:
                if (x == 0 or x == n - 1) and (y == 0 or y == n - 1):
                    tot += 4
                elif (x == 0 or x == n - 1) or (y == 0 or y == n - 1):
                    tot += 2
                else:
                    tot += 1
    return tot


def IsTerminalNode(tablero, player, n, dirx, diry):
    for y in range(n):
        for x in range(n):
            if Validar(tablero, x, y, player, n, dirx, diry):
                return False
    return True

def Minimax(tablero, player, depth, maximizingPlayer, n, dirx, diry, minEvaltablero, maxEvaltablero):
    if depth == 0 or IsTerminalNode(tablero, player, n, dirx, diry):
        return Evaltablero(tablero, player, n)
    if maximizingPlayer:
        bestValue = minEvaltablero
        for y in range(n):
            for x in range(n):
                if Validar(tablero, x, y, player, n, dirx, diry):
                    (tableroTemp, totctr) = Mover(copy.deepcopy(tablero), x, y, player, dirx, diry, n)
                    v = Minimax(tableroTemp, player, depth - 1, False, n, dirx, diry, minEvaltablero, maxEvaltablero)
                    bestValue = max(bestValue, v)
    else:
        bestValue = maxEvaltablero
        for y in range(n):
            for x in range(n):
                if Validar(tablero, x, y, player, n, dirx, diry):
                    (tableroTemp, totctr) = Mover(copy.deepcopy(tablero), x, y, player, dirx, diry, n)
                    v = Minimax(tableroTemp, player, depth - 1, True, n, dirx, diry, minEvaltablero, maxEvaltablero)
                    bestValue = min(bestValue, v)
    return bestValue

def BestMove(tablero, player, n, dirx,diry,depth, minEvaltablero, maxEvaltablero):
    maxPoints = 0
    mx = -1; my = -1
    for y in range(n):
        for x in range(n):
            if Validar(tablero, x, y, player, n, dirx, diry):
                (tableroTemp, totctr) = Mover(copy.deepcopy(tablero), x, y, player, dirx, diry, n)
                points = Minimax(tableroTemp, player, depth, True, n, dirx, diry, minEvaltablero, maxEvaltablero)
                if points > maxPoints:
                    maxPoints = points
                    mx = x; my = y
    return (mx, my)

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
    dirx = [-1, 0, 1, -1, 1, -1, 0, 1]
    diry = [-1, -1, -1, 0, 0, 1, 1, 1]
    
    depth = 3
    (x, y) = BestMove(tablero, turno, n, dirx,diry,depth, minEvaltablero, maxEvaltablero)
    if not (x == -1 and y == -1):
        (tablero, totctr) = Mover(tablero, x, y, turno, dirx, diry, n)

    res=str(y)+str(x)
    return res

@app.route("/calcular", methods=['GET'])
def heuristica():
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
