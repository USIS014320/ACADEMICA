from urllib import parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import mysql.connector
import json


class crud:
    def __init__(self):
        self.conexion = mysql.connector.connect(user='root', password='root',
                                                host='localhost', database='db_academica')


crud = crud()


class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'inicio.html'

            return SimpleHTTPRequestHandler.do_GET(self)

        if self.path == '/consultar':
            resp = crud.consultar()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resp=resp)).encode('utf-8'))


print('Servidor iniciado en el puerto 3011')
servidor = HTTPServer(('localhost', 3011), servidorBasico)
servidor.serve_forever()
