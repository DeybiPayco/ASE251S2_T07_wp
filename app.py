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

@app.route('/contact')
def contactanos():
    return render_template('contactanos.html')

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
if __name__ == '__main__':
    app.run(debug=True)
