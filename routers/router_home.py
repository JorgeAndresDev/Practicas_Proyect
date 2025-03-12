from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error




# Importando cenexión a BD
from controllers.funciones_home import *

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
def detalles_empleado(cc):
    # Obtener los datos del empleado usando la función
    empleado = obtener_empleado_por_cc(cc)
    
    if empleado:
        # Si el empleado existe, pasamos los datos a la plantilla
        return render_template('detalles_empleado.html', empleado=empleado)
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
        
        # Renderizar la plantilla con los resultados
        return render_template('empleados.html', empleados=resultados, search=search_term)
    
    except Exception as e:
        # En caso de error, mostrar mensaje y redireccionar
        flash(f'Error al buscar empleado: {str(e)}', 'error')
        return redirect(url_for('index'))
    





@app.route("/editar-empleado/<int:id>", methods=['GET'])
def viewEditarEmpleado(id):
    if 'conectado' in session:
        respuestaEmpleado = buscarEmpleadoUnico(id)
        if respuestaEmpleado:
            return render_template(f'{PATH_URL}/form_empleado_update.html', respuestaEmpleado=respuestaEmpleado)
        else:
            flash('El empleado no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actulizar informacion de empleado
from flask import request, redirect, render_template


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
    




    