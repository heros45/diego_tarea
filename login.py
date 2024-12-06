from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(100),  nullable=True )
    birth_date = db.Column(db.String(10),  nullable=True )
    dni = db.Column(db.String(20),  nullable=True )
    phone = db.Column(db.String(20),  nullable=True )
    city = db.Column(db.String(100) ,  nullable=True )

# Routes
@app.route('/')
def home():
    context={}
    if 'user_id' in session:     # Verifica si el usuario está autenticado    
        user = User.query.get(session['user_id']) # Obtiene el usuario de la base de datos
        if user:
            context['username'] = user.username  # Pasa el nombre del usuario al contexto
            return render_template('profile.html', context=context)
    # Si no está autenticado, redirige a login
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    context={}
    if request.method == 'POST':
       
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
        

            return redirect(url_for('home'))
        flash('Invalid username or password.', 'danger')
        context['error']='usuario y contraseña no validos'
        
        return render_template('login.html',context=context)
    return render_template('login.html', context=context)

@app.route('/register', methods=['GET', 'POST'])
def register():
    context={}
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', context=context)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    context={}
    # Si no está autenticado, redirige a login
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if request.method== "GET":
        user = User.query.get(session['user_id']) # Obtiene el usuario de la base de datos
        name = user.name
        birth_date = user.birth_date
        dni = user.dni
        phone = user.phone
        city = user.city
        context['name']=name
        context['birth_date']=birth_date
        context['dni']=dni
        context['phone']=phone
        context['city']=city
        return render_template('update.html', user=user, context=context)
    if request.method == 'POST':
        user.name = request.form['name']
        user.birth_date = request.form['birth_date']
        user.dni = request.form['dni']
        user.phone = request.form['phone']
        user.city = request.form['city']
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        context['exito']='actualizacion enviada correctamente'
        return render_template('update.html', user=user, context=context)

    return render_template('update.html', user=user, context=context)

# Initialize database
@app.before_request
def create_tables():
    db.create_all() 

if __name__ == '__main__':

    app.run(debug=True,host='0.0.0.0', port=5000)
