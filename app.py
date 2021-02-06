from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask import render_template, redirect, url_for, request
from flask_login import logout_user, LoginManager, login_user, current_user, login_required
from flask import current_app as app
from werkzeug.local import LocalProxy

'''from .signals import password_reset, reset_password_instructions_sent
from .utils import config_value, get_token_status, hash_data, hash_password, \
    url_for_security, verify_hash'''

import os
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)
app.debug = True
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://igyjuhnhjqsalr:b0619dbf9954e73981073ac211fb4528b13a52130b90ad78ce21f1915ab61b5e@ec2-54-211-77-238.compute-1.amazonaws.com:5432/d1ca3mj1hh9epr'

bcrypt = Bcrypt()
bcrypt.init_app(app)
# login_manager.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.log_viwe = 'login'
app.secret_key = b'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

#app.config['SECRET_KEY'] = 'top-secret'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'serviciosenlanubeflask@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

'''app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')'''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Editorial(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)


class Autor(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(500), nullable=False, index=True)
    apellido = db.Column(db.String(350))
    fecha_nacimiento = db.Column(db.DateTime, default=datetime.utcnow)


class Libros(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(500), nullable=False, index=True)
    autor = db.Column(db.String(350))
    editorial = db.Column(db.String(50))
    clasificacion = db.Column(db.String(80))
    formato = db.Column(db.String(50))
    NoPaginas = db.Column(db.Integer)
    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)

    idEditorial = db.Column(db.Integer, db.ForeignKey('editorial.id'))
    idAutor = db.Column(db.Integer, db.ForeignKey('autor.id'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/eliminarEditoriales/<id>')
@login_required
def eliminarEditoriales(id):
    q = Editorial.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('catalogoEditoriales'))


@app.route('/editarEditoriales/<id>')
@login_required
def editarEditoriales(id):
    r = Editorial.query.filter_by(id=int(id)).first()
    return render_template("editarEditoriales.html", editorial=r)


@app.route('/actualizarEditoriales', methods=['GET', 'POST'])
@login_required
def actualizarEditoriales():
    if request.method == "POST":
        qry = Editorial.query.get(request.form['id'])
        qry.nombre = request.form['nombre']
        db.session.commit()
        return redirect(url_for('catalogoEditoriales'))


@app.route('/eliminarLibro/<id>')
@login_required
def eliminarLibro(id):
    q = Libros.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('catalogoLibros'))


@app.route('/editarLibro/<id>')
@login_required
def editarLibro(id):
    r = Libros.query.filter_by(id=int(id)).first()
    return render_template("editarLibro.html", libro=r)


@app.route('/actualizarLibro', methods=['GET', 'POST'])
@login_required
def actualizarLibro():
    if request.method == "POST":
        qry = Libros.query.get(request.form['id'])
        qry.titulo = request.form['nombre']
        qry.autor = request.form['autor']
        qry.clasificacion = request.form['clasificacion']
        qry.formato = request.form['formato']
        qry.NoPaginas = request.form['paginas']
        qry.fehca_publicacion = request.form['fecha']
        db.session.commit()
        return redirect(url_for('catalogoLibros'))


@app.route('/eliminarAutor/<id>')
@login_required
def eliminarAutor(id):
    q = Autor.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('catalogoAutores'))


@app.route('/editarAutor/<id>')
@login_required
def editarAutor(id):
    r = Autor.query.filter_by(id=int(id)).first()
    return render_template("editarAutor.html", autor=r)


@app.route('/actualizarAutor', methods=['GET', 'POST'])
@login_required
def actualizarAutor():
    if request.method == "POST":
        qry = Autor.query.get(request.form['id'])
        qry.nombre = request.form['nombre']
        qry.apellido = request.form['apellido']
        qry.fehca_nacimiento = request.form['fecha']
        db.session.commit()
        return redirect(url_for('catalogoAutores'))


@app.route('/registrarEditoriales', methods=['GET', 'POST'])
@login_required
def agregarEditorial():
    if request.method == "POST":
        #opts = QuerySelectField(query_factory=Editorial, allow_blank=False, get_label='name')
        nombre = request.form['nombre']
        editorial = Editorial(nombre=nombre)
        db.session.add(editorial)
        db.session.commit()
        return redirect(url_for('catalogoEditoriales'))
    return render_template("registrarEditoriales.html")


@app.route('/registrarLibros', methods=['GET', 'POST'])
@login_required
def agregarLibro():
    if request.method == "POST":
        nombre = request.form['nombre']
        autor = request.form['select']
        editorial = request.form['editorial']
        clasificacion = request.form['clasificacion']
        formato = request.form['formato']
        paginas = request.form['paginas']
        fecha = request.form['fecha']
        libro = Libros(titulo=nombre, autor=autor, editorial=editorial, clasificacion=clasificacion,
                       formato=formato, NoPaginas=paginas, fecha_publicacion=fecha)
        select = request.form['select']
        conEditorial = request.form['editorial']
        db.session.add(libro)
        db.session.commit()
        return redirect(url_for('catalogoLibros', select=select, conEditorial=conEditorial))
    consulta = Autor.query.all()
    conEditorial = Editorial.query.all()
    print(consulta)
    return render_template("registrarLibros.html", consulta=consulta, conEditorial=conEditorial)


@app.route('/registrarAutor', methods=['GET', 'POST'])
@login_required
def agregarAutor():
    if request.method == "POST":
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha = request.form['fecha']
        autor = Autor(nombre=nombre, apellido=apellido, fecha_nacimiento=fecha)
        db.session.add(autor)
        db.session.commit()
        return redirect(url_for('catalogoAutores'))
    return render_template("registrarAutor.html")


@login_manager.user_loader
def load_user(usuarios_id):
    return Usuario.query.get(int(usuarios_id))

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), )
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    pwd = db.Column(db.String(255))

    def is_authenticated(self):
            return True


    def is_active(self):
        return True


    def is_anonymous(self):
        return False


    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.filter_by(id=user_id).first()


@app.route('/registry', methods=['GET', 'POST'])
def registry():
    mensaje = ""
    if request.method == 'POST':
        pwd = request.form["pwd"]
        password = request.form["password"]

        if pwd != password:
            mensaje = "La contraseña no coincide, intenta nuevamente por favor"
            return render_template("registry.html", mensaje=mensaje)
        else:
            nombre = request.form["nombre_usuario"]
            correo = request.form["email"]
            pwd = request.form["pwd"]
            print(nombre, correo, pwd)

            usuario = Usuario(
                nombre=nombre,
                email=correo,
                pwd=bcrypt.generate_password_hash(pwd).decode('utf-8')
            )
            db.session.add(usuario)
            db.session.commit()

            mensaje = "Usuario registrado con éxito"

            msg = Message("Gracias por registrarte",
                          sender="serviciosenlanubeflask@gmail.com", recipients=[correo])
            msg.body = "Este es un mail de prueba"
            msg.html = "<p>Este es un mail</p>"
            mail.send(msg)
            return render_template("registry.html", mensaje=mensaje)
    return render_template("registry.html", mensaje=mensaje)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@app.route('/loginin', methods=['GET', 'POST'])
def loginin():
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["pwd"]
        usuario_existe = Usuario.query.filter_by(email=email).first()
        print(usuario_existe)
        mensaje = usuario_existe.email
        if usuario_existe != None:
            print("Existe")
            if bcrypt.check_password_hash(usuario_existe.pwd, pwd):
                login_user(usuario_existe)
                if current_user.is_authenticated:
                    return redirect(url_for("home"))
                print("Usuario autentificado")
                return render_template("catalogoLibros.html")
        return render_template("login.html", mensaje=mensaje)
    print("Login in...")
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/catalogoEditoriales', methods=['GET', 'POST'])
def catalogoEditoriales():
    catalogoEditoriales = Editorial.query.all()
    return render_template("catalogoEditoriales.html", catalogoEditoriales=catalogoEditoriales)


@app.route('/catalogoLibros', methods=['GET', 'POST'])
def catalogoLibros():
    catalogoLibros = Libros.query.all()
    return render_template("catalogoLibros.html", catalogoLibros=catalogoLibros)


@app.route('/catalogoAutores', methods=['GET', 'POST'])
def catalogoAutores():
    catalogoAutores = Autor.query.all()
    return render_template("catalogoAutores.html", catalogoAutores=catalogoAutores)


@app.route('/olvcon', methods=['GET', 'POST'])
def olvcon():
    return render_template("olvcon.html")


@app.route('/catalogo', methods=['GET', 'POST'])
def catalogo():
    return render_template("catalogo.html")


if __name__ == "__main__":
    app.run()
