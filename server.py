from urllib import parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import crud_usuario
import crud_actor
import crud_pelicula

crud_usuario = crud_usuario.crud_usuario()
crud_actor = crud_actor.crud_actor()
crud_pelicula = crud_pelicula.crud_pelicula
class servidorBasico(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'Vanguard/añadir_pelicula.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        
        elif self.path == '/consultar-usuario':
            resp = crud_usuario.consultar_usuario()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resp=resp)).encode('utf-8'))
        
        elif self.path == '/consultar-actor':
            resp = crud_actor.consultar_actor()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resp=resp)).encode('utf-8'))
        
        elif self.path == '/consultar-pelicula':
            resp = crud_pelicula.consultar_pelicula()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(dict(resp=resp)).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode('utf-8')
        data = parse.unquote(data)
        data = json.loads(data)
        if self.path == '/usuario':
            resp = crud_usuario.administrar_usuarios(data)
        elif self.path == '/actor':
            resp = crud_actor.administrar_actor(data)
        elif self.path == '/pelicula':
            resp = crud_pelicula.administrar_pelicula(data)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(dict(resp=resp)).encode('utf-8'))

print('Servidor iniciado en el puerto 3000')
servidor = HTTPServer(('localhost', 3000), servidorBasico)
servidor.serve_forever()