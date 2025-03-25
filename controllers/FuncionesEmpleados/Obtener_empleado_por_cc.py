from conexion.conexionBD import connectionBD  # Conexión a BD

def obtener_empleado_por_cc(cc):
    try:
        # Establecer la conexión con la base de datos
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Consulta SQL para obtener los datos del empleado según su cédula (CC)
                querySQL = "SELECT * FROM tbl_empleados WHERE cc = %s"
                cursor.execute(querySQL, (cc,))
                
                # Obtener el primer resultado (empleado)
                empleado = cursor.fetchone()
                
                # Si se encuentra un empleado, lo devolvemos, si no, devolvemos None
                if empleado:
                    return empleado
                else:
                    # Retorna None si no se encuentra el empleado
                    print(f"No se encontró ningún empleado con CC: {cc}")
                    return None
                
    except Exception as e:
        # Capturar cualquier excepción y mostrar el mensaje de error
        print(f"Ocurrió un error en obtener_empleado_por_cc: {e}")
        return None