from conexion.conexionBD import connectionBD  # Conexión a BD

def buscarEmpleadoBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = """
                    SELECT 
                        e.CC,
                        e.NOM, 
                        e.CAR,
                        e.CENTRO,
                        e.CASH,
                        e.SAC,
                        e.CHECK,
                        e.MOD,
                        e.ER,
                        e.PARADAS,
                        e.PERFORMANCE
                    FROM tbl_empleados AS e
                    WHERE e.CC LIKE %s OR e.NOM LIKE %s 
                    ORDER BY e.NOM ASC
                """
                search_pattern = f"%{search}%"  # Agregar "%" alrededor del término de búsqueda
                mycursor.execute(querySQL, (search_pattern, search_pattern))
                resultado_busqueda = mycursor.fetchall()
                return resultado_busqueda
    except Exception as e:
        print(f"Error en la búsqueda: {e}")
        return []