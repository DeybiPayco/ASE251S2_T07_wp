<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from sqlalchemy import or_
import os

# Configuración de la aplicación Flask
app = Flask(__name__,
           template_folder='templates',
           static_folder='static')

# Configuración de la base de datos
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "pasteleria.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de la base de datos y login manager
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

# Modelos de la base de datos
class User(UserMixin, db.Model):
    """Modelo para los usuarios/clientes"""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.Text, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    es_admin = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

class Producto(db.Model):
    """Modelo para los productos de la pastelería"""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False)
    imagen = db.Column(db.String(200), nullable=True)
    categoria = db.Column(db.String(50), nullable=False)
    destacado = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Producto {self.nombre}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'imagen': self.imagen,
            'categoria': self.categoria,
            'destacado': self.destacado,
            'activo': self.activo
        }

# User loader para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rutas principales
@app.route('/')
def index():
    """Página principal con carrusel y productos destacados"""
    productos_destacados = Producto.query.filter_by(destacado=True, activo=True).limit(3).all()
    return render_template('index.html', productos_destacados=productos_destacados)

@app.route('/productos')
def productos():
    """Catálogo completo de productos"""
    categoria = request.args.get('categoria', '')
=======
from flask import Flask, render_template, request, redirect, url_for

# Inicialización de Flask
app = Flask(__name__)

# Rutas principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')
>>>>>>> 6bbafa98b1d904e818105a3cc8c7de5716e4ce54

    if categoria:
        productos_lista = Producto.query.filter_by(categoria=categoria, activo=True).all()
    else:
        productos_lista = Producto.query.filter_by(activo=True).all()

    categorias = db.session.query(Producto.categoria).distinct().all()
    categorias = [cat[0] for cat in categorias]

    return render_template('productos.html',
                         productos=productos_lista,
                         categorias=categorias,
                         categoria_actual=categoria)

@app.route('/contactanos')
def contactanos():
    """Página de contacto"""
    return render_template('contactanos.html')

<<<<<<< HEAD
@app.route('/test')
def test():
    """Página de prueba para botones"""
    return render_template('test.html')

# Rutas de autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión de usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'¡Bienvenido de nuevo, {user.nombre}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de nuevos usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validaciones
        if not all([nombre, email, password, confirm_password]):
            flash('Por favor completa todos los campos requeridos.', 'warning')
        elif password != confirm_password:
            flash('Las contraseñas no coinciden.', 'warning')
        elif len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'warning')
        else:
            # Verificar si el email ya existe
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Este email ya está registrado.', 'warning')
            else:
                # Crear nuevo usuario
                new_user = User(
                    nombre=nombre,
                    email=email,
                    telefono=telefono,
                    direccion=direccion
                )
                new_user.set_password(password)

                db.session.add(new_user)
                db.session.commit()

                flash('¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.', 'success')
                return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Cierre de sesión"""
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('index'))

@app.route('/perfil')
@login_required
def perfil():
    """Perfil del usuario"""
    return render_template('perfil.html')

# Rutas alternativas (para compatibilidad)
@app.route('/contact')
def contact():
    from flask import redirect, url_for
    return redirect(url_for('contactanos'))

# Manejo de errores
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Context processors para variables globales en templates
@app.context_processor
def utility_functions():
    return {
        'site_name': 'Pastelería Delicias',
        'current_year': 2025,
        'current_user': current_user
    }

# Comandos de base de datos
@app.cli.command('init-db')
def init_db_command():
    """Crea las tablas de la base de datos"""
    db.create_all()
    print('Base de datos inicializada correctamente.')

@app.cli.command('seed-db')
def seed_db_command():
    """Pobla la base de datos con datos de ejemplo"""
    # Productos de ejemplo
    productos = [
        Producto(
            nombre='Pastel de Chocolate',
            descripcion='Bizcocho suave con cobertura de chocolate belga y relleno cremoso.',
            precio=350.00,
            imagen='image/4.jpg',
            categoria='Pasteles',
            destacado=True
        ),
        Producto(
            nombre='Tarta de Fresa',
            descripcion='Fresas frescas con crema batida casera y base de masa quebrada.',
            precio=280.00,
            imagen='image/6.jpg',
            categoria='Tartas',
            destacado=True
        ),
        Producto(
            nombre='Galletas Artesanales',
            descripcion='Crujientes y hechas con amor, perfectas para cualquier ocasión.',
            precio=120.00,
            imagen='image/5.jpg',
            categoria='Galletas',
            destacado=True
        ),
        Producto(
            nombre='Pastel de Vainilla',
            descripcion='Clásico pastel de vainilla con crema de mantequilla.',
            precio=320.00,
            imagen='image/4.jpg',
            categoria='Pasteles',
            destacado=False
        ),
        Producto(
            nombre='Brownies Especiales',
            descripcion='Brownies de chocolate con nueces y un toque de caramelo.',
            precio=150.00,
            imagen='image/5.jpg',
            categoria='Postres',
            destacado=False
        )
    ]

    # Crear usuario administrador por defecto
    admin_user = User(
        nombre='Administrador',
        email='admin@pasteleria.com',
        telefono='1234567890',
        es_admin=True
    )
    admin_user.set_password('admin123')

    # Crear usuario cliente de ejemplo
    cliente_user = User(
        nombre='Juan Pérez',
        email='juan@ejemplo.com',
        telefono='0987654321',
        direccion='Calle Principal #123, Ciudad'
    )
    cliente_user.set_password('cliente123')

    for producto in productos:
        db.session.add(producto)

    db.session.add(admin_user)
    db.session.add(cliente_user)
    db.session.commit()
    print('Base de datos poblada con datos de ejemplo.')

# Decorador para requerir rol de administrador
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.es_admin:
            flash('Acceso denegado. Se requieren permisos de administrador.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Rutas de administración
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Panel principal de administración"""
    total_productos = Producto.query.count()
    productos_activos = Producto.query.filter_by(activo=True).count()
    productos_destacados = Producto.query.filter_by(destacado=True, activo=True).count()
    total_usuarios = User.query.count()
    usuarios_activos = User.query.filter_by(activo=True).count()
    usuarios_admin = User.query.filter_by(es_admin=True, activo=True).count()

    # Últimos usuarios registrados
    ultimos_usuarios = User.query.order_by(User.creado_en.desc()).limit(5).all()

    # Últimos productos agregados
    ultimos_productos = Producto.query.order_by(Producto.creado_en.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                         total_productos=total_productos,
                         productos_activos=productos_activos,
                         productos_destacados=productos_destacados,
                         total_usuarios=total_usuarios,
                         usuarios_activos=usuarios_activos,
                         usuarios_admin=usuarios_admin,
                         ultimos_usuarios=ultimos_usuarios,
                         ultimos_productos=ultimos_productos)

# Rutas de productos para administración
@app.route('/admin/productos')
@login_required
@admin_required
def admin_productos():
    """Lista de productos para administración"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    categoria = request.args.get('categoria', '')

    query = Producto.query

    if search:
        query = query.filter(Producto.nombre.contains(search))
    if categoria:
        query = query.filter(Producto.categoria == categoria)

    productos = query.order_by(Producto.creado_en.desc()).paginate(
        page=page, per_page=10, error_out=False)

    categorias = db.session.query(Producto.categoria).distinct().all()
    categorias = [cat[0] for cat in categorias]

    return render_template('admin/productos.html',
                         productos=productos,
                         categorias=categorias,
                         search=search,
                         categoria_actual=categoria)

@app.route('/admin/productos/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_producto_nuevo():
    """Crear nuevo producto"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        imagen = request.form.get('imagen')
        categoria = request.form.get('categoria')
        destacado = request.form.get('destacado') == 'on'
        activo = request.form.get('activo') == 'on'

        if not all([nombre, precio, categoria]):
            flash('Por favor completa los campos requeridos.', 'warning')
        else:
            try:
                precio = float(precio)
                nuevo_producto = Producto(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=precio,
                    imagen=imagen,
                    categoria=categoria,
                    destacado=destacado,
                    activo=activo
                )
                db.session.add(nuevo_producto)
                db.session.commit()
                flash('Producto creado exitosamente.', 'success')
                return redirect(url_for('admin_productos'))
            except ValueError:
                flash('El precio debe ser un número válido.', 'danger')

    return render_template('admin/producto_form.html',
                         producto=None,
                         action='Crear',
                         categorias=get_categorias())

@app.route('/admin/productos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_producto_editar(id):
    """Editar producto existente"""
    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio_str = request.form.get('precio')
        imagen = request.form.get('imagen')
        categoria = request.form.get('categoria')
        destacado = request.form.get('destacado') == 'on'
        activo = request.form.get('activo') == 'on'

        # Establecer campos de texto primero
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.imagen = imagen
        producto.categoria = categoria
        producto.destacado = destacado
        producto.activo = activo

        if not all([nombre, precio_str, categoria]):
            flash('Por favor completa los campos requeridos.', 'warning')
        else:
            try:
                precio = float(precio_str)
                producto.precio = precio
                db.session.commit()
                flash('Producto actualizado exitosamente.', 'success')
                return redirect(url_for('admin_productos'))
            except ValueError:
                flash('El precio debe ser un número válido.', 'danger')

    return render_template('admin/producto_form.html',
                         producto=producto,
                         action='Editar',
                         categorias=get_categorias())

@app.route('/admin/productos/<int:id>/eliminar', methods=['POST'])
@login_required
@admin_required
def admin_producto_eliminar(id):
    """Eliminar producto"""
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado exitosamente.', 'success')
    return redirect(url_for('admin_productos'))

@app.route('/admin/productos/<int:id>/toggle-activo', methods=['POST'])
@login_required
@admin_required
def admin_producto_toggle_activo(id):
    """Activar/desactivar producto"""
    producto = Producto.query.get_or_404(id)
    producto.activo = not producto.activo
    db.session.commit()

    estado = "activado" if producto.activo else "desactivado"
    flash(f'Producto {estado} exitosamente.', 'success')
    return redirect(url_for('admin_productos'))

@app.route('/admin/productos/<int:id>/toggle-destacado', methods=['POST'])
@login_required
@admin_required
def admin_producto_toggle_destacado(id):
    """Marcar/desmarcar producto como destacado"""
    producto = Producto.query.get_or_404(id)
    producto.destacado = not producto.destacado
    db.session.commit()

    estado = "marcado como destacado" if producto.destacado else "desmarcado como destacado"
    flash(f'Producto {estado} exitosamente.', 'success')
    return redirect(url_for('admin_productos'))

# Rutas de usuarios para administración
@app.route('/admin/usuarios')
@login_required
@admin_required
def admin_usuarios():
    """Lista de usuarios para administración"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    role_filter = request.args.get('role', '')

    query = User.query

    if search:
        query = query.filter(or_(User.nombre.contains(search), User.email.contains(search)))
    if role_filter == 'admin':
        query = query.filter(User.es_admin == True)
    elif role_filter == 'cliente':
        query = query.filter(User.es_admin == False)

    usuarios = query.order_by(User.creado_en.desc()).paginate(
        page=page, per_page=15, error_out=False)

    return render_template('admin/usuarios.html',
                         usuarios=usuarios,
                         search=search,
                         role_filter=role_filter)

@app.route('/admin/usuarios/<int:id>/toggle-activo', methods=['POST'])
@login_required
@admin_required
def admin_usuario_toggle_activo(id):
    """Activar/desactivar usuario"""
    if id == current_user.id:
        flash('No puedes desactivar tu propia cuenta.', 'warning')
        return redirect(url_for('admin_usuarios'))

    usuario = User.query.get_or_404(id)
    usuario.activo = not usuario.activo
    db.session.commit()

    estado = "activado" if usuario.activo else "desactivado"
    flash(f'Usuario {estado} exitosamente.', 'success')
    return redirect(url_for('admin_usuarios'))

@app.route('/admin/usuarios/<int:id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def admin_usuario_toggle_admin(id):
    """Convertir usuario en administrador o quitar permisos"""
    if id == current_user.id:
        flash('No puedes modificar tus propios permisos de administrador.', 'warning')
        return redirect(url_for('admin_usuarios'))

    usuario = User.query.get_or_404(id)
    usuario.es_admin = not usuario.es_admin
    db.session.commit()

    if usuario.es_admin:
        flash(f'Usuario {usuario.email} ahora es administrador.', 'success')
    else:
        flash(f'Se han quitado los permisos de administrador a {usuario.email}.', 'info')

    return redirect(url_for('admin_usuarios'))

@app.route('/admin/usuarios/<int:id>/eliminar', methods=['POST'])
@login_required
@admin_required
def admin_usuario_eliminar(id):
    """Eliminar usuario"""
    if id == current_user.id:
        flash('No puedes eliminar tu propia cuenta.', 'warning')
        return redirect(url_for('admin_usuarios'))

    usuario = User.query.get_or_404(id)
    email = usuario.email
    db.session.delete(usuario)
    db.session.commit()
    flash(f'Usuario {email} eliminado exitosamente.', 'success')
    return redirect(url_for('admin_usuarios'))

# Función auxiliar
def get_categorias():
    """Obtener lista de categorías de productos"""
    return ['Pasteles', 'Tartas', 'Galletas', 'Postres', 'Panadería', 'Bebidas']

# Inicialización del servidor
=======
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

# 🧁 Ruta para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Aquí puedes agregar lógica de autenticación
        print(f"Usuario: {email}, Contraseña: {password}")
        return redirect(url_for('index'))  # Redirige al home después de iniciar sesión
    return render_template('login.html')

# 🍓 Ruta para registro (opcional)
@app.route('/registro')
def registro():
    return render_template('registro.html')

# Ejecutar servidor
>>>>>>> 6bbafa98b1d904e818105a3cc8c7de5716e4ce54
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    app.run(host=host, port=port, debug=True)