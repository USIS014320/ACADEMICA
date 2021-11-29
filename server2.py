from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from typing import NamedTuple
from urllib import parse
import json
import mysql.connector
from mysql.connector import Error
from collections import namedtuple


class crud:
    def __init__(self):
        self.conexion = mysql.connector.connect(user='root', password='root',
                                                host='localhost', database='db_academica')
        if self.conexion.is_connected():
            print('Conectado exitosamente a la base de datos')
        else:
            print('Error al conectar a la base de datos')


crud = crud()


class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
        if  self.path == "/":
            self.path = "/index.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == "/registro":
            self.path = "/registro.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == "/perfil":
            self.path = "/perfil.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == "/agregarPelicula":
            self.path = "/añadir_pelicula.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == "/editarPelicula":
            self.path = "/editar_pelicula.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == "/eliminarPelicula":
            self.path = "/eliminar_pelicula.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == "/agregarActor":
            self.path = "/añadir_actor.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == "/editarActor":
            self.path = "/editar_actor.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == "/eliminarActor":
            self.path = "/eliminar_actor.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == "/consulta":
            resp = crud.consultar()
            resp = json.dumps(dict(data=resp))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(resp.encode("utf-8"))

    def do_POST(self):
        longitud_contenido = int(self.headers['Content-Length'])
        contenido = self.rfile.read(longitud_contenido)
        contenido = contenido.decode("utf-8")
        contenido = parse.unquote(contenido)
        contenido = json.loads(contenido)
        resp = crud.administrar_alumno(contenido)
        resp = json.dumps(dict(resp=resp))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(resp.encode("utf-8"))


print("Servidor iniciado")
server = HTTPServer(("localhost", 3000), servidorBasico)
server.serve_forever()