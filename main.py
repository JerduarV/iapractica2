#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pythones.net

from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route("/calcular", methods=['GET'])
def heuristica():
    try:
        #estado = request.args.get('estado')
        #turno = request.args.get('turno')
        #print('estado: ')
        #print(estado)
        #print('turno: ')
        print('hola')
        return '52'
    except:
        print('no llegaron parametros')
        return '00'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
