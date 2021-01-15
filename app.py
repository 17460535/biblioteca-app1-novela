from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
Bootstrap(app)

# Configuracion a la conexión con postgres

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rmucsedqnbitwb:8d106ab9e7347e8ff7e602fdb7c4000e86fcd86feb94e7173934c8e04a7443e0@ec2-52-72-65-76.compute-1.amazonaws.com:5432/df1bkr6n6o1q73'
# OJOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#Probe con mi base de datos y funciona, si tu contraseña es novelavega4 y en pgAdmin creaste Escolares ya no debe darte error el db.create_all()
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:12345@localhost:5432/armando'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))
    apellido = db.Column(db.String(30))
    #Comente esa linea de abajo, no es ni atributo de la clase ni método
    lista = ["Nosotros", "Contacto", "Preguntas frecuentes"]


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == "POST":
        print("request")
        campo_nombre = request.form['nombre']
        campo_apellido = request.form['apellido']
        alumno = Alumno(nombre=campo_nombre, apellido=campo_apellido)
        db.session.add(alumno)
        db.session.commit()
        mensaje = "Alumno registrado"
        return render_template("index.html", mensaje=mensaje)
        return render_template("index.html", variable=lista)

    lista = ["Acerca", "Nosotros", "Contactos", "Preguntas frecuentes"]

    return render_template("index.html", variable=lista)
    # return redirect(url_for ('acerca'))


@app.route('/acerca')
def acerca():
    return render_template("acerca.html")


if __name__ == "__main__":
    app.run()
