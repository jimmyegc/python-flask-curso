from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL

app = Flask(__name__)

conexion = MySQL(app)

@app.route('/')
def index():
  return "menikmati"

@app.route('/cursos')
def listar_cursos():
  try:
    cursor=conexion.connection.cursor()
    sql="Select codigo, nombre, creditos from curso"
    cursor.execute(sql)
    datos = cursor.fetchall()
    cursos = []
    for fila in datos:
      curso={'codigo': fila[0], 'nombre': fila[1], 'creditos': fila[2]}
      cursos.append(curso)
    
    return jsonify({ "status": "Ok", "message": "Cursos listados", "data": cursos })
  except Exception as ex: 
    return jsonify({ "status": "Error", "message": ex })

@app.route('/cursos/<codigo>', methods=['GET'])
def leer_curso(codigo):
  try:
    cursor=conexion.connection.cursor()
    sql="Select codigo, nombre, creditos from curso where codigo='{0}'".format(codigo)
    cursor.execute(sql)
    datos=cursor.fetchone()
    if datos != None:
      curso = {'codigo': datos[0], 'nombre': datos[1], 'creditos': datos[2]}
      return jsonify({ "status": "Ok", "message": "Curso encontrado", "data": curso })
    else:
      return jsonify({ "status": "Ok", "message": "Curso no encontrado", "data": {} })
  except Exception as ex:
    return jsonify({ "status": "Error", "message": ex })

@app.route('/cursos', methods=['POST'])
def crear_curso():
  try:
    # print(request.json)
    cursor=conexion.connection.cursor()
    sql = """INSERT INTO curso (codigo, nombre, creditos) 
    VALUES ('{0}','{1}','{2}')""".format(
      request.json['codigo'], request.json['nombre'], request.json['creditos']
    )    
    cursor.execute(sql)
    conexion.connection.commit()
    return jsonify({ "status": "Ok", "message": "Curso registrado" })
  except Exception as ex:
    return jsonify({ "status": "Error", "message": ex })

@app.route('/cursos/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
  try:
    # print(request.json)
    cursor=conexion.connection.cursor()
    sql = "DELETE FROM curso WHERE codigo = '{0}'".format(codigo)
    cursor.execute(sql)
    conexion.connection.commit()
    return jsonify({ "status": "Ok", "message": "Curso eliminado" })
  except Exception as ex:
    return jsonify({ "status": "Error", "message": ex })

@app.route('/cursos/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):
  try:
    # print(request.json)
    cursor=conexion.connection.cursor()
    sql = """UPDATE curso SET nombre = '{0}', creditos = {1}
    WHERE codigo = '{2}'""".format(
      request.json['nombre'], request.json['creditos'], codigo
    )    
    cursor.execute(sql)
    conexion.connection.commit()
    return jsonify({ "status": "Ok", "message": "Curso actualizado" })
  except Exception as ex:
    return jsonify({ "status": "Error", "message": ex })

def pagina_no_encontrada(error):
  return "<h1>Página no encontrada</h1>"

if __name__ == '__main__':
  app.config.from_object(config['development'])
  app.register_error_handler(404, pagina_no_encontrada)
  app.run()