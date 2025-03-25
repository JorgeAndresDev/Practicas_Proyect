from conexion.conexionBD import connectionBD  # Conexión a BD

def  buscar_empleado_unico(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = """
                    SELECT 
                        e.cc,
                        e.nombre_empleado, 
                        e.apellido_empleado,
                        e.sexo_empleado,
                        e.telefono_empleado,
                        e.email_empleado,
                        e.profesion_empleado,
                        e.salario_empleado,
                        e.foto_empleado
                    FROM tbl_empleados AS e
                    WHERE e.cc = %s LIMIT 1
                """
                mycursor.execute(querySQL, (id,))
                empleado = mycursor.fetchone()
                return empleado
    except Exception as e:
        print(f"Ocurrió un error en def  buscar_empleado_unico: {e}")
        return []
