from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Cadena de conexión a PostgreSQL obtenida de la variable de entorno o por defecto
DATABASE_URL = os.getenv("DATABASE_URL", "TU_SERVICE_URI_DE_AIVEN_AQUI")

def get_db_connection():
    # Conexión directa a PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Crear la tabla automáticamente al iniciar la app si no existe
def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS alumnos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100),
                control VARCHAR(50),
                carrera VARCHAR(100),
                turno VARCHAR(20),
                pasatiempos VARCHAR(255)
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Tabla en Postgres verificada/creada con éxito.")
    except Exception as e:
        print(f"Error al conectar/crear tabla: {e}")

# Llamar a la inicialización
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form.get('nombre')
    control = request.form.get('control')
    carrera = request.form.get('carrera')
    turno = request.form.get('turno')
    
    # Los checkboxes se obtienen como una lista y los unimos en un solo texto separado por comas
    pasatiempos_lista = request.form.getlist('pasatiempos')
    pasatiempos = ", ".join(pasatiempos_lista) if pasatiempos_lista else "Ninguno"

    conn = get_db_connection()
    cur = conn.cursor()
    
    # Inserción utilizando sintaxis de Postgres (%s)
    cur.execute(
        "INSERT INTO alumnos (nombre, control, carrera, turno, pasatiempos) VALUES (%s, %s, %s, %s, %s)",
        (nombre, control, carrera, turno, pasatiempos)
    )
    conn.commit()
    cur.close()
    conn.close()

    return "<h1>¡Datos guardados con éxito en la base de datos de Postgres!</h1><br><a href='/'>Regresar</a>"

if __name__ == '__main__':
    app.run(debug=True)
