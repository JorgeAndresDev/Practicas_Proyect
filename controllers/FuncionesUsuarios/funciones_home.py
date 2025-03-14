from conexion.conexionBD import connectionBD


def lista_usuariosBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT id, name_surname, email_user, created_user FROM users"
                cursor.execute(querySQL,)
                usuariosBD = cursor.fetchall()
        return usuariosBD
    except Exception as e:
        print(f"Error en lista_usuariosBD : {e}")
        return []


# Eliminar uEmpleado
def sql_eliminar_empleado(cc):
    try:
        connection = connectionBD()
        if connection:
            with connection.cursor() as cursor:
                # Consulta para eliminar el empleado
                querySQL = "DELETE FROM tbl_empleados WHERE CC = %s"
                cursor.execute(querySQL, (cc,))
                connection.commit()
                return True
        else:
            return False
    except Exception as e:
        print(f"Error al eliminar empleado: {e}")
        return False
    finally:
        if connection:
            connection.close()


# Eliminar usuario
def eliminarUsuario(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM users WHERE id=%s"
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarUsuario : {e}")
        return []