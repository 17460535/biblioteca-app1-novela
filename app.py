from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
Bootstrap(app)

# Configuracion a la conexión con postgres

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bzuvvwhdddncot:0413c40db78faef0f6644939182fc0d60d022d52855ea7ed1009e83d1c9ccb8d@ec2-54-85-13-135.compute-1.amazonaws.com:5432/dcls4msc7r7c7p'
# OJOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# Probe con mi base de datos y funciona, si tu contraseña es novelavega4 y en pgAdmin creaste Escolares ya no debe darte error el db.create_all()
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:12345@localhost:5432/armando'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Alumno(db.Model): 
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(30))
    apellido = db.Column(db.String(30)) 
    lista = []
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == "POST":
        campo_nombre = request.form['nombre']
        campo_apellido = request.form['apellido']
        alumno = Alumno(nombre=campo_nombre,apellido=campo_apellido)
        db.session.add(alumno)
        db.session.commit()
        mensaje = "Registrado"
        return redirect(url_for('index'))
    return render_template("index.html", variable = ["acerca", "Contacto", "Preguntas Frecuentes"])
@app.route('/acerca')
def acerca():
    consulta = Alumno.query.all()
    return render_template("acerca.html", arg = consulta)
@app.route('/eliminar/<id>')
def eliminar(id):
    q = Alumno.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('acerca'))

@app.route('/editar/<id>')
def editar(id):
    r = Alumno.query.filter_by(id=int(id)).first()
    return render_template("editar.html", alumno = r)

@app.route('/actualizar', methods=['GET','POST'])
def actualizar():
    if request.method == "POST":
        qry = Alumno.query.get(request.form['id'])
        qry.nombre = request.form['nombreE']
        qry.apellido =request.form['apellidoE']
        db.session.commit()
        return redirect(url_for('acerca'))
if __name__ == "__main__":
    app.run()
