from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Conexion a Base de datos MYSQL
app.config['MYSQL_HOST'] = 'database-1.cyzg51c5zdme.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'flaskmovies'
mysql = MySQL(app)

#configuraciones
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM movies')
    data = cur.fetchall()
    print (data)
    return render_template('index.html', peliculas = data)

@app.route('/agregar_pelicula', methods=['POST'])
def agregar_pelicula():
    if request.method == 'POST':
        titulo = request.form['titulo']
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO movies (titulo, categoria, descripcion) VALUES(%s, %s, %s)',
        (titulo, categoria, descripcion))

        mysql.connection.commit()
        flash('Pelicula Agregada Satisfactoriamente')
        return redirect(url_for('Index'))


@app.route('/editar_pelicula/<id>')
def get_pelicula(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM movies WHERE id = %s', (id))
    data = cur.fetchall()
    print(data,[0])
    return render_template('editar-contacto.html', pelicula = data[0])



@app.route('/actualizar/<id>', methods = ['POST'])
def update_pelicula(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE movies
        SET titulo = %s,
            categoria = %s,
            descripcion = %s
        WHERE id = %s
        """, (titulo, categoria, descripcion, id))
        mysql.connection.commit()
        flash('La Pelicula Ha Sido Editada Satisfactoriamente')
        return redirect(url_for('Index'))



@app.route('/eliminar_pelicula/<string:id>')
def eliminar_pelicula(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM movies WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Pelicula eliminada satisfactoriamente')
    return redirect(url_for('Index'))
    

if __name__ == '__main__':
    app.run(port = 3000, debug = True)