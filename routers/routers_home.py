from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error

from flask import request, redirect, render_template
from flask import render_template, request, redirect, url_for, jsonify

# Importar la conexión desde tu archivo
from conexion.conexionBD import connectionBD

import pandas as pd
from conexion.conexionBD import connectionBD
from flask import Flask, send_file, make_response
from io import BytesIO
from datetime import datetime
# Importando cenexión a BD
from controllers.FuncionesEmpleados.F_empleados import buscarEmpleadoBD, buscarEmpleadoUnico, obtener_empleado_por_cc, registrar_empleado, sql_lista_empleadosBD
from controllers.FuncionesUsuarios.funciones_usuarios import eliminarUsuario, lista_usuariosBD, sql_eliminar_empleado
from controllers.funciones_login import *

PATH_URL = "public/empleados"


# Rutas para las funciones de empleados
# Ruta para registrar empleado
@app.route('/registrar_empleado', methods=['GET', 'POST'])
def viewFormEmpleado():
    if request.method == 'GET':
        return render_template('public/empleados/registrar.html')
    
    elif request.method == 'POST':
        # Obtener los datos del formulario
        cc = request.form.get('cc')
        nom = request.form.get('nom')
        car = request.form.get('car')
        centro = request.form.get('centro')
        
        # Llamar a la función para crear el empleado
        resultado, mensaje = registrar_empleado(cc, nom, car, centro)
        
        # Mostrar mensaje de éxito o error
        if resultado:
            flash(mensaje, 'success')
        else:
            flash(mensaje, 'error')
        
        return redirect(url_for('viewFormEmpleado'))


# Ruta para listar empleados
@app.route('/lista_empleados')
def lista_empleados():
    empleados = sql_lista_empleadosBD()
    print("Ruta de la plantilla:", app.template_folder)  # Depuración
    return render_template('public/empleados/lista_empleados.html', empleados=empleados)


@app.route('/detalles-empleado/<int:cc>', methods=['GET'])
def editar_empleado(cc):
    # Obtener los datos del empleado usando la función
    empleado = obtener_empleado_por_cc(cc)
    
    if empleado:
        # Si el empleado existe, pasamos los datos a la plantilla
        return render_template('editar_empleado.html', empleado=empleado)
    else:
        # Si no se encuentra el empleado, mostramos una página de error
        return render_template('error.html', mensaje="Empleado no encontrado")


# Ruta para buscar empleados
@app.route('/buscar-empleado', methods=['POST'])
def buscarEmpleado():
    try:
        # Obtener el término de búsqueda del formulario
        search_term = request.form.get('search', '')
        
        # Si el término de búsqueda está vacío, redireccionar a la página principal
        if not search_term:
            return redirect(url_for('index'))
        
        # Realizar la búsqueda
        resultados = buscarEmpleadoBD(search_term)
        
        # Debuggear resultados
        print(f"Término de búsqueda: {search_term}")
        print(f"Resultados encontrados: {len(resultados)}")
        
        # Renderizar la plantilla con los resultados
        return render_template('empleados.html', empleados=resultados, search=search_term)
    
    except Exception as e:
        # En caso de error, mostrar mensaje y redireccionar
        print(f"Error en buscarEmpleado(): {e}")
        flash(f'Error al buscar empleado: {str(e)}', 'error')
        return redirect(url_for('index'))
    


@app.route('/buscar-empleado-ajax', methods=['POST'])
def buscarEmpleadoAjax():
    try:
        search_term = request.values.get('search', '').strip()
        
        # Si el término está vacío, en lugar de redirigir, devolver lista vacía
        if not search_term:
            return jsonify([])
        
        resultados = buscarEmpleadoBD(search_term)
        return jsonify(resultados)  # Enviar resultados en formato JSON
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Rutas para las funciones de usuarios 
@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicioCpanel'))


@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))


@app.route('/eliminar-empleado/<string:cc>')
def eliminar_empleado(cc):
    # Eliminamos el empleado de la base de datos
    resultado = sql_eliminar_empleado(cc)
    
    # Mensaje flash para mostrar al usuario
    if resultado:
        flash('Empleado eliminado correctamente', 'success')
    else:
        flash('Error al eliminar empleado', 'danger')
    
    # Redireccionamos a la lista de empleados
    return redirect(url_for('lista_empleados'))
    
@app.route('/subir-excel', methods=['POST'])
def subir_excel():
    if 'file' not in request.files:
        return jsonify({"message": "No se ha subido ningún archivo"}), 400
    
    file = request.files['file']
    df = pd.read_excel(file)  # Leer el archivo Excel

    # Se remplaza NaN por 0
    df = df.fillna(0)

    conn = connectionBD()
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


# Ruta para mostrar el formulario de edición
@app.route('/editar_empleado/<cc>')
def mostrar_form_editar_empleado(cc):
    print(f"Intentando editar empleado con CC: {cc}")
    
    try:
        conn = connectionBD()  # <-- Cambia esto ✅
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tbl_empleados WHERE CC = %s", (int(cc),))
        empleado = cursor.fetchone()
        cursor.close()
        conn.close()
        
        print(f"Datos del empleado: {empleado}")
        
        if empleado is None:
            flash('Empleado no encontrado', 'danger')
            return redirect(url_for('lista_empleados'))
        
        return render_template('public/empleados/editar_empleado.html', empleado=empleado)

    
    except Exception as e:
        print(f"Error en editar_empleado: {str(e)}")
        flash(f'Error al cargar los datos: {str(e)}', 'danger')
        return redirect(url_for('lista_empleados'))


@app.route('/test-editar/<cc>')
def test_editar(cc):
    return f"Probando edición para el empleado con CC: {cc}"

# Ruta para procesar la actualización
@app.route('/actualizar_empleado', methods=['POST'])
def procesar_actualizacion_empleado():
    # Obtener los datos del formulario
    cc = request.form['cc']
    nombre = request.form['nom']
    cargo = request.form['car']
    centro = request.form['centro']
    
    try:
        # Crear conexión y cursor
        conn = connectionBD()
        cursor = conn.cursor()
        
        # Query para actualizar los datos del empleado
        sql = """
            UPDATE tbl_empleados 
            SET NOM = %s, CAR = %s, CENTRO = %s 
            WHERE CC = %s
        """
        
        # Ejecutar la consulta
        cursor.execute(sql, (nombre, cargo, centro, cc))
        
        # Confirmar los cambios en la base de datos
        conn.commit()
        
        # Cerrar cursor y conexión
        cursor.close()
        conn.close()
        
        flash('Datos del empleado actualizados correctamente', 'success')
    
    except Exception as e:
        flash(f'Error al actualizar los datos: {str(e)}', 'danger')
    
    # Redireccionar a la lista de empleados
    return redirect(url_for('lista_empleados'))




@app.route('/descargar-informe-empleados')
def descargar_informe_empleados():
    try:
        # Conectar a la base de datos
        conn = connectionBD()
        cursor = conn.cursor(dictionary=True)
        
        # Consultar todos los datos de la tabla de empleados
        sql = "SELECT * FROM tbl_empleados"
        cursor.execute(sql)
        empleados = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not empleados:
            # Si no hay datos, puedes mostrar un mensaje o redirigir
            return "La base de datos esta vacia, no se puede generer un reporte :("
        
        # Crear un DataFrame con los datos
        df = pd.DataFrame(empleados)
        
        # Crear un buffer para el archivo Excel
        output = BytesIO()
        
        # Crear un writer de Excel
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        
        # Escribir el DataFrame al archivo Excel
        df.to_excel(writer, sheet_name='Empleados', index=False)
        
        # Obtener el libro de trabajo y la hoja
        workbook = writer.book
        worksheet = writer.sheets['Empleados']
        
        # Añadir formato a las columnas (opcional)
        # Por ejemplo, formato para columnas numéricas y porcentuales
        formato_porcentaje = workbook.add_format({'num_format': '0.00%'})
        formato_numero = workbook.add_format({'num_format': '0.00'})
        
        # Aplicar formato a columnas específicas (ajusta los índices según tus columnas)
        # Por ejemplo, si CHECK, MOD, ER son porcentajes:
        for col_idx, col_name in enumerate(df.columns):
            if col_name in ['CHECK', 'MOD', 'ER', 'PERFORMANCE']:
                # Convertir de texto a número si es necesario
                worksheet.set_column(col_idx, col_idx, 12, formato_porcentaje)
            elif col_name in ['CASH', 'SAC', 'PARADAS']:
                worksheet.set_column(col_idx, col_idx, 12, formato_numero)
        
        # Ajustar el ancho de las columnas automáticamente
        for i, col in enumerate(df.columns):
            column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_width)
        
        # Guardar el archivo
        writer.close()
        
        # Reiniciar el puntero del buffer al principio
        output.seek(0)
        
        # Configurar la respuesta para la descarga del archivo
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Informe_Empleados_{fecha_actual}.xlsx"
        
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        return response
        
    except Exception as e:
        # Manejo de errores
        return f"Error al generar el informe: {str(e)}", 500