from conexion.conexionBD import connectionBD  # Conexión a BD


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