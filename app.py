from flask import Flask, render_template,request,redirect,url_for,flash
from flask.helpers import flash
from flask_mysqldb import MySQL
# from werkzeug.wrappers import request

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'colegio'
mysql = MySQL(app)


@app.route('/')
def Index():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM alumnos')
    data=cur.fetchall()
    return render_template('index.html',alumnos = data)

app.secret_key='mysecretkey'

@app.route('/add_estudiante', methods=['POST'])
def add_estudiante():
    if request.method == 'POST':
        details = request.form
        id = details['Id']
        Nombre = details['Nombre']
        Apellido = details['Apellido']
        Sexo = details['Sexo']
        FechaNacimiento = details['FechaNacimiento']
        FechaRegistro = details['FechaRegistro']
        Correo = details['correo']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO alumnos(id,nombre,apellido,sexo,fecha_nacimiento,fecha_registro,correo) VALUES (%s, %s, %s, %s, %s, %s, %s)", (id,Nombre,Apellido,Sexo,FechaNacimiento,FechaRegistro,Correo))
        mysql.connection.commit()
        flash('Estudiante Agregado Correctamente')
        # cur.close()
        return redirect(url_for('Index'))

        


@app.route('/edit/<string:id>')
def get_alumno(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM alumnos WHERE id = %s',[id])
    data = cur.fetchall()
    print(data[0])
    return render_template('editAlumnos.html',alumnos=data[0])

@app.route('/update/<string:id>',methods=['POST'])
def update_alumno(id):
    if request.method == 'POST':
        details = request.form
        Nombre = details['Nombre']
        Apellido = details['Apellido']
        Sexo = details['Sexo']
        FechaNacimiento = details['FechaNacimiento']
        FechaRegistro = details['FechaRegistro']
        Correo = details['correo']
        cur=mysql.connection.cursor()
        cur.execute("""
            UPDATE alumnos
            SET nombre = %s,
                apellido = %s,
                sexo = %s,
                fecha_nacimiento = %s,
                fecha_registro = %s,
                correo = %s
            WHERE id = %s
        """,(Nombre,Apellido,Sexo,FechaNacimiento,FechaRegistro,Correo,id))
        mysql.connection.commit()
        flash('Alumno actualizado con exito')
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>')
def delete(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM alumnos WHERE id = %s',[id])
    mysql.connection.commit()
    flash('Alumno eliminado correctamente')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(debug=True)
