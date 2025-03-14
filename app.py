from flask import Flask
# Al inicio de tu archivo principal (app.py o similar)
from controllers.FuncionesEmpleados.F_empleados import (
    registrar_empleado,
    sql_lista_empleadosBD,
    obtener_empleado_por_cc,
    buscarEmpleadoBD,
    buscarEmpleadoUnico
)

app = Flask(__name__)
application = app
app.secret_key = '97110c78ae51a45af397b6534caef90ebb9b1dcb3380f008f90b23a5d1616bf1bc29098105da20fe'
