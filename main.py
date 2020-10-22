#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pythones.net
import copy
from flask import Flask, render_template, request, redirect
app = Flask(__name__)


def Mover(board, x, y, player, dirx, diry, n):
    totctr = 0
    board[y][x] = player
    for d in range(8):
        ctr = 0
        for i in range(8):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            if dx < 0 or dx > n - 1 or dy < 0 or dy > n - 1:
                ctr = 0; break
            elif board[dy][dx] == player:
                break
            elif board[dy][dx] == '2':
                ctr = 0; break
            else:
                ctr += 1
        for i in range(ctr):
            dx = x + dirx[d] * (i + 1)
            dy = y + diry[d] * (i + 1)
            board[dy][dx] = player
        totctr += ctr
    return (board, totctr)

def ValidMove(board, x, y, player, n, dirx, diry):
    if x < 0 or x > n - 1 or y < 0 or y > n - 1:
        return False
    if board[y][x] != '2':
        return False
    (boardTemp, totctr) = Mover(copy.deepcopy(board), x, y, player, dirx, diry, n)
    if totctr == 0:
        return False
    return True

def EvalBoard(board, player, n):
    tot = 0
    for y in range(n):
        for x in range(n):
            if board[y][x] == player:
                if (x == 0 or x == n - 1) and (y == 0 or y == n - 1):
                    tot += 4
                elif (x == 0 or x == n - 1) or (y == 0 or y == n - 1):
                    tot += 2
                else:
                    tot += 1
    return tot


def IsTerminalNode(board, player, n, dirx, diry):
    for y in range(n):
        for x in range(n):
            if ValidMove(board, x, y, player, n, dirx, diry):
                return False
    return True

def Minimax(board, player, depth, maximizingPlayer, n, dirx, diry, minEvalBoard, maxEvalBoard):
    if depth == 0 or IsTerminalNode(board, player, n, dirx, diry):
        return EvalBoard(board, player, n)
    if maximizingPlayer:
        bestValue = minEvalBoard
        for y in range(n):
            for x in range(n):
                if ValidMove(board, x, y, player, n, dirx, diry):
                    (boardTemp, totctr) = Mover(copy.deepcopy(board), x, y, player, dirx, diry, n)
                    v = Minimax(boardTemp, player, depth - 1, False, n, dirx, diry, minEvalBoard, maxEvalBoard)
                    bestValue = max(bestValue, v)
    else:
        bestValue = maxEvalBoard
        for y in range(n):
            for x in range(n):
                if ValidMove(board, x, y, player, n, dirx, diry):
                    (boardTemp, totctr) = Mover(copy.deepcopy(board), x, y, player, dirx, diry, n)
                    v = Minimax(boardTemp, player, depth - 1, True, n, dirx, diry, minEvalBoard, maxEvalBoard)
                    bestValue = min(bestValue, v)
    return bestValue

def BestMove(board, player, n, dirx,diry,depth, minEvalBoard, maxEvalBoard):
    maxPoints = 0
    mx = -1; my = -1
    for y in range(n):
        for x in range(n):
            if ValidMove(board, x, y, player, n, dirx, diry):
                (boardTemp, totctr) = Mover(copy.deepcopy(board), x, y, player, dirx, diry, n)
                points = Minimax(boardTemp, player, depth, True, n, dirx, diry, minEvalBoard, maxEvalBoard)
                if points > maxPoints:
                    maxPoints = points
                    mx = x; my = y
    return (mx, my)

def iniciaIA(turno, estado):
    n = 8
    filas=[]
    columnas=[]
    for x in range(8):
        filas=[]
        for y in range(8):
            filas.append(estado[(x*n)+y])
        columnas.append(filas)
    board=columnas

    minEvalBoard = -1
    maxEvalBoard = n * n + 4 * n + 4 + 1
    dirx = [-1, 0, 1, -1, 1, -1, 0, 1]
    diry = [-1, -1, -1, 0, 0, 1, 1, 1]
    
    depth = 3
    (x, y) = BestMove(board, turno, n, dirx,diry,depth, minEvalBoard, maxEvalBoard)
    if not (x == -1 and y == -1):
        (board, totctr) = Mover(board, x, y, turno, dirx, diry, n)

    res=str(y)+str(x)
    return res

@app.route("/calcular", methods=['GET'])
def heuristica():
    try:
        estado = request.args.get('estado')
        turno = request.args.get('turno')
        result= iniciaIA(str(turno), str(estado))
        print(result)
        return result
    except:
        print('error fatal')
        return '00'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
