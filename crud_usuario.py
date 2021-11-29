import conexion

db = conexion.conexion()


class crud_usuario:
    def consultar_usuario(self):
        sql = "SELECT * FROM usuarios"
        return db.consultar(sql)
    
    
    # ADMINISTRAR USUARIOS
    def administrar_usuarios(self, usuario):
        try:
            print(self, usuario)
            # AGREGAR USUARIO
            if usuario['action'] == 'insertar':
                sql = "INSERT INTO usuarios (idUsuario, nombre, nickname, edad, pais, contraseña, contraseña2) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (self.crear_id('Usuario'), usuario['nombre'], usuario['nickname'],usuario['edad'], usuario['pais'], usuario['password'], usuario['password2'], usuario['password3'])

            # ACTUALIZAR USUARIO
            elif usuario['action'] == 'actualizar':
                sql = "UPDATE usuarios SET nombre = %s, nickname = %s, edad = %s, pais = %s, contraseña = %s WHERE idUsuario = %s"
                val = (usuario['nombre'], usuario['nickname'], usuario['edad'], usuario['pais'],usuario['password'], usuario['password2'], usuario['password3'], usuario['id'])

            # ELIMINAR USUARIO
            elif usuario['action'] == 'eliminar':
                sql = "DELETE FROM usuarios WHERE idUsuario = %s"
                val = (usuario['id'],)
            else:
                print('Accion no valida')
                
            return self.ejecutar_sql(sql, val)
        except Exception as e:
            return {'status': 'error', 'msg': 'No se pudo realizar la accion', 'code': str(e)}