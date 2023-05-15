from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
import os, logging


app = Flask(__name__)
app.secret_key = os.urandom(24)

app.logger.setLevel(logging.ERROR)
file_handler = logging.FileHandler('error.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
app.logger.addHandler(file_handler)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts;')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    err = ""
    if request.method == 'POST':
       fullname = request.form['fullname']
       phone = request.form['phone']
       email = request.form['email']
       
       #Validar los campos
    if not fullname:
        err = f'El campo fullname esta vacio {fullname}'
    
    if not phone:
        err = f'El campo phone esta vacio {phone}'
    
    if not email:
        err = f'El campo email esta vacio {email}'
        
    if not err:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s);' ,(fullname, phone, email))
        mysql.connection.commit()
        flash("Contacto agregado")
        return redirect(url_for('Index'))
    else:
        app.logger.error(f'Error en some_route: {err}')
        return "Error"
       
@app.route('/get_edit/<string:id>')
def get_edit(id):
    cur = mysql.connection.cursor()
    cur.execute(f'SELECT * FROM contacts WHERE id = {id};')
    data = cur.fetchall()
    return render_template('edit.html', contact = data[0])


@app.route('/edit/<string:id>',  methods=['POST'])
def edit_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE contacts 
                SET 
                fullname = %s,
                phone = %s,
                email = %s
                WHERE id = %s;
                """, (fullname, phone, email, id))
    mysql.connection.commit()
    flash("Se edito correctamente")
    return redirect(url_for('Index'))


@app.route('/delete/<string:id>')
def edit_delete(id):
    cur = mysql.connection.cursor()
    cur.execute(f'DELETE FROM contacts WHERE id = {id};')
    mysql.connection.commit()
    flash(f"Se borro el registro{id}")
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=3000, debug = True)
