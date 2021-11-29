import conexion

db = conexion.conexion()


class crud_pelicula:
    def consultar_pelicula(self):
        sql = "SELECT * FROM pelicula"
        return db.consultar(sql)
    
#ADMINISTRAR ACTOR
def administrar_pelicula(self, peliculas):
    try:
        print(peliculas)
        
        #AGREGAR PELCICULAS
        if peliculas['action'] == 'insertar':
            sql = "INSERT INTO peliculas (idPelciula, nombrePelicula, nuevo_nombrePelicula, duracionPelicula, fecha_estrenoPelicula, directorPelicula, generoPelicula, paisPelicula, imagenPelicula, trailerPelicula, tagsPelicula) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (self.crear_id('Pelicula'), peliculas['nombrePelicula'], peliculas['nuevo_nombrePelicula'], peliculas['duracionPelicula'], peliculas['fecha_estrenoPelicula'], peliculas['directorPelicula'], peliculas['generoPelicula'], peliculas['paisPelicula'], peliculas['imagenPelicula'], peliculas['trailerPelicula'], peliculas['tagsPelicula'])
        
            #ACTUALIZAR PELICULAS
        elif peliculas['action'] == 'actualizar':
            sql = "UPDATE peliculas SET nombrePelicula = %s, nuevo_nombrePelicula = %s, duracionPelicula = %s, fecha_estrenoPelicula =%s, directorPelicula =%s, generoPelicula =%s, paisPelicula =%s, imagenPelicula =%s, trailerPelicula =%s, tagsPelicula =%s  WHERE idPelicula = %s"
            val = (peliculas['nombrePelicula'], peliculas['nuevo_nombrePelicula'], peliculas['duracionPelicula'], peliculas['fecha_estrenoPelicula'], peliculas['directorPelicula'], peliculas['generoPelicula'], peliculas['paisPelicula'], peliculas['imagenPelicula'], peliculas['trailerPelicula'], peliculas['tagsPelicula'])
            
            #ELIMINAR PELICULAS
        elif peliculas['action'] == 'eliminar':
                sql = "DELETE FROM peliculas WHERE idPelicula = %s"
                val = (peliculas['id'],)
        else:
                print('Accion no valida')
        return self.ejecutar_sql(sql, val)
    except Exception as e:
        return {'status':'error', 'msg': 'No se pudo realizar la accion', 'code': str(e)}
