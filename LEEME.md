# Pastelería Delicias - Panel de Administración

## Instalación y Configuración

Sigue estos pasos para configurar el proyecto en tu entorno local:

### Prerrequisitos
- **Python 3.7+**
- **Node.js 16+**
- **npm** (viene con Node.js)

### Pasos de instalación

1. **Clonar/descargar el proyecto**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd ASE251S2_T07_wp
   ```

2. **Instalar Python y Node.js si no están**
   - Descargar Python desde: https://www.python.org/
   - Descargar Node.js desde: https://nodejs.org/

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

4. **Inicializar base de datos**
   ```bash
   flask init-db
   flask seed-db
   ```

5. **Construir CSS**
   ```bash
   npm run build:css
   ```

6. **Ejecutar**
   ```bash
   python app.py
   ```

## Acceso al Sistema

### Sitio Web
El proyecto estará disponible en: **http://127.0.0.1:5000**

### Panel de Administración
**URL:** `http://127.0.0.1:5000/admin`

### Credenciales de Acceso

####  Usuario Administrador
- **Email:** `admin@pasteleria.com`
- **Contraseña:** `admin123`

## Características Principales

 Panel de Administración
- **Dashboard** con estadísticas en tiempo real
- **Gestión de Productos** (CRUD completo)
- **Gestión de Usuarios** (activar/desactivar, roles)
- **Interfaz profesional y responsive**
- **Seguridad por roles** con protección de rutas

### 📊 Funcionalidades de Administración

#### Productos
- Crear, editar, eliminar productos
- Activar/desactivar productos sin eliminarlos
- Marcar productos como destacados
- Filtros por categoría y búsqueda
- Vista previa en tiempo real

#### Usuarios
- Ver todos los usuarios registrados
- Activar/desactivar cuentas
- Promover a administrador
- Eliminar usuarios con confirmación

#### Seguridad
- Protección automática contra acceso no autorizado
- Los administradores no pueden modificarse a sí mismos
- Validación de formularios en frontend y backend

## Estructura del Proyecto

```
ASE251S2_T07_wp/
├── app.py                    # Aplicación Flask principal
├── requirements.txt          # Dependencias Python
├── package.json             # Dependencias Node.js
├── pasteleria.db            # Base de datos SQLite
├── LEEME.md               # Este archivo
├── static/
│   ├── css/               # Estilos CSS generados
│   ├── js/components/     # Componentes JavaScript
│   └── image/            # Imágenes del sitio
└── templates/
    ├── base.html         # Plantilla principal
    ├── components/       # Componentes reutilizables
    ├── admin/           # Plantillas del panel admin
    └── *.html           # Páginas del sitio
```

## Comandos Útiles

### Desarrollo
```bash
# Construir CSS una vez
npm run build:css

# Ver y reconstruir CSS automáticamente
npm run build:css:watch

# Modo desarrollo (con autoreload)
npm run dev
```

### Base de Datos
```bash
# Inicializar tablas
flask init-db

# Poblar con datos de ejemplo
flask seed-db

# Reiniciar base de datos (borrar archivo .db)
rm pasteleria.db && flask init-db && flask seed-db
```

### Ejecución
```bash
# Servidor Flask
python app.py

# Servidor con puerto personalizado
PORT=8000 python app.py

# Servidor accesible desde red local
HOST=0.0.0.0 PORT=8000 python app.py
```

## Notas Importantes

- **Archivo `requirements.txt`:** Contiene todas las dependencias de Python necesarias
- **Archivo `package.json`:** Contiene las dependencias de Node.js y scripts para CSS
- **Base de datos:** Se crea automáticamente en `pasteleria.db` al ejecutar `flask init-db`
- **CSS:** Se genera automáticamente en `static/css/output.css` desde `static/css/input.css`
- **Imágenes:** Deben estar en la carpeta `static/image/` para que funcionen correctamente

