from flask import Flask, render_template, redirect, url_for, request, flash, send_file, after_this_request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from gtts import gTTS
import os
import tempfile
import re
# Configuración de la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelo de usuario, ahora usando "email" en lugar de "username"
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas, intente nuevamente.')
    return render_template('login.html')

# Ruta para registrarse
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Por favor, ingresa un correo electrónico válido.")
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('El correo ya está registrado.')
            return redirect(url_for('register'))
        new_user = User(
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('register.html')

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Ruta para el convertidor de texto a audio
@app.route('/converter', methods=['GET', 'POST'])
@login_required
def converter():
    if request.method == 'POST':
        text = request.form.get('text')
        lang = request.form.get('lang')  # Recupera el idioma elegido
        if not text:
            flash("Debes ingresar texto para convertir.")
            return redirect(url_for('converter'))
        # Crear un archivo temporal para almacenar el audio
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.close()
        try:
            # Usa el idioma seleccionado; por ejemplo, 'es' para español o 'en' para inglés
            tts = gTTS(text, lang=lang)
            tts.save(temp_file.name)
        except Exception as e:
            flash("Error al generar el audio: " + str(e))
            return redirect(url_for('converter'))
        @after_this_request
        def remove_file(response):
            try:
                os.remove(temp_file.name)
            except Exception as error:
                app.logger.error("Error al eliminar el archivo temporal: %s", error)
            return response
        return send_file(temp_file.name, mimetype="audio/mpeg", as_attachment=True, download_name="audio.mp3")
    return render_template('converter.html')




# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
