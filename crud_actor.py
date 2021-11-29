import conexion

db = conexion.conexion()


class crud_actor:
    def consultar_actor(self):
        sql = "SELECT * FROM actor"
        return db.consultar(sql)

#ADMINISTRAR ACTOR
def administrar_actor(self, actor):
    try:
        print(actor)
        
        #AGREGAR ACTOR
        if actor['action'] == 'insertar':
            sql = "INSERT INTO actor (idActor, nombre, fecha_nacimiento, lugar_nacimiento) VALUES (%s, %s, %s, %s)"
            val = (self.crear_id('Actor'), actor['nombre'], actor['fecha_nacimiento'], actor['lugar_nacimiento'])
        
            #ACTUALIZAR ACTOR
        elif actor['action'] == 'actualizar':
            sql = "UPDATE actor SET nombre = %s, fecha_nacimiento = %s, lugar_nacimiento = %s WHERE idActor = %s"
            val = (actor['nombre'], actor['fecha_nacimiento'], actor['lugar_nacimiento'], actor['id'])
            
            #ELIMINAR ACTOR
        elif actor['action'] == 'eliminar':
                sql = "DELETE FROM actor WHERE idActor = %s"
                val = (actor['id'],)
        else:
                print('Accion no valida')
        return self.ejecutar_sql(sql, val)
    except Exception as e:
        return {'status':'error', 'msg': 'No se pudo realizar la accion', 'code': str(e)}

