#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pythones.net

from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route("/calcular", methods=['GET'])
def heuristica():
    try:
        estado = request.args.get('estado')
        turno = request.args.get('turno')
        cad_tablero = estado
        tablero = []
        x = 0
        while x < 64:
            fila = []
            y = 0
            while y < 8:
                fila.append(cad_tablero[x])
                y += 1
                x += 1
            tablero.append(fila)

        print(tablero)
        return '52'
    except:
        print('no llegaron parametros')
        return '00'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
