from conexion.conexionBD import connectionBD  # Conexión a BD

def subir_empleados_excel():
    if 'file' not in request.files:
        return jsonify({"message": "No se ha subido ningún archivo"}), 400

    file = request.files['file']
    df = pd.read_excel(file)

    # Se remplaza NaN por 0
    df = df.fillna(0)

    conn = conexionBD()
    cursor = conn.cursor(dictionary=True)

    for _, row in df.iterrows():
        sql_check = "SELECT * FROM tbl_empleados WHERE CC = %s"
        cursor.execute(sql_check, (row["CC"],))
        empleado_existente = cursor.fetchone()

        if empleado_existente:
            sql_update = """
                UPDATE tbl_empleados SET NOM = %s, CAR = %s, CENTRO = %s, CASH = %s, 
                SAC = %s, `CHECK` = %s, `MOD` = %s, ER = %s, PARADAS = %s, PERFORMANCE = %s WHERE CC = %s
            """
            cursor.execute(sql_update, (row["NOM"], row["CAR"], row["CENTRO"], row["CASH"], 
                                        row["SAC"], row["CHECK"], row["MOD"], row["ER"], row["PARADAS"],row["PERFORMANCE"], row["CC"]))
        else:
            sql_insert = """
                INSERT INTO tbl_empleados (CC, NOM, CAR, CENTRO, CASH, SAC, `CHECK`, `MOD`, ER, PARADAS,PERFORMANCE)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (row["CC"], row["NOM"], row["CAR"], row["CENTRO"], row["CASH"], 
                                        row["SAC"], row["CHECK"], row["MOD"], row["ER"], row["PARADAS"], row["PERFORMANCE"] ))
        conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Base de datos actualizada correctamente"}), 200