

from conexion.conexionBD import connectionBD


def registrar_empleado(CC, NOM, CAR, CENTRO):
    try:
        # Crear conexión a la base de datos
        conexion = connectionBD()
        cursor = conexion.cursor(dictionary=True)
        
        # Verificar si el empleado ya existe por cédula
        sql_check = "SELECT * FROM app_empresa_bd.tbl_empleados WHERE CC = %s"
        cursor.execute(sql_check, (CC,))
        empleado_existente = cursor.fetchone()
        
        if empleado_existente:
            return False, "Ya existe un empleado registrado con esta cédula"
        
        # Insertar el empleado con valores por defecto para los demás campos
        sql_insert = """
            INSERT INTO tbl_empleados (CC, NOM, CAR, CENTRO, CASH, SAC, `CHECK`, `MOD`, `ER`, PARADAS) 
            VALUES (%s, %s, %s, %s, 0, 0, 0, 0, 0, 0)
        """
        
        cursor.execute(sql_insert, (CC, NOM, CAR, CENTRO))
        conexion.commit()
        
        cursor.close()
        conexion.close()
        
        return True, "Empleado registrado correctamente"
        
    except Exception as e:
        return False, f"Error al registrar empleado: {str(e)}"



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



# Lista de Empleados
def sql_lista_empleadosBD():     
    try:         
        connection = connectionBD()         
        if connection:             
            with connection.cursor(dictionary=True) as cursor:                 
                querySQL = """                     
                    SELECT                         
                        CC,                         
                        NOM,                         
                        CAR,                         
                        CENTRO                                            
                    FROM tbl_empleados                     
                    ORDER BY CC DESC                 
                """                 
                cursor.execute(querySQL)                 
                empleadosBD = cursor.fetchall()                 
                return empleadosBD         
        else:             
            return None     
    except Exception as e:         
        print(f"Error en la función sql_lista_empleadosBD: {e}")         
        return None     
    finally:         
        if connection:             
            connection.close()




def buscarEmpleadoBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = """
                    SELECT 
                        CC, 
                        NOM AS Nombre,  <!-- Renombramos NOM a Nombre para mayor claridad -->
                        CAR, 
                        CENTRO AS Centro  <!-- Renombramos CENTRO a Centro -->
                    FROM tbl_empleados
                    WHERE 
                        CC LIKE %s OR 
                        NOM LIKE %s OR 
                        CAR LIKE %s OR 
                        CENTRO LIKE %s
                    ORDER BY CC DESC
                """
                search_pattern = f"%{search}%"  # Agregar "%" alrededor del término de búsqueda
                mycursor.execute(querySQL, (
                    search_pattern, search_pattern, search_pattern, search_pattern
                ))
                resultado_busqueda = mycursor.fetchall()
                return resultado_busqueda
    except Exception as e:
        print(f"Error en la función buscarEmpleadoBD: {e}")
        return None
def buscarEmpleadoUnico(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
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
                        WHERE e.cc =%s LIMIT 1
                    """)
                mycursor.execute(querySQL, (id,))
                empleado = mycursor.fetchone()
                return empleado

    except Exception as e:
        print(f"Ocurrió un error en def buscarEmpleadoUnico: {e}")
        return []

# Agregar esto a controllers/empleados_controller.py o donde corresponda según tu estructura

def buscarEmpleadoBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
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
                """)
                search_pattern = f"%{search}%"  # Agregar "%" alrededor del término de búsqueda
                mycursor.execute(querySQL, (search_pattern, search_pattern))
                resultado_busqueda = mycursor.fetchall()
                return resultado_busqueda
    except Exception as e:
        print(f"Error en la búsqueda: {e}")
        return []