from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://...")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS alumnos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100),
                control VARCHAR(50),
                fecha_nacimiento DATE,
                carrera VARCHAR(100),
                turno VARCHAR(20),
                deportes VARCHAR(255),
                pasatiempos VARCHAR(255)
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Tabla en Postgres verificada/creada con éxito.")
    except Exception as e:
        print(f"Error al conectar/crear tabla: {e}")

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form.get('nombre')
    control = request.form.get('control')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    carrera = request.form.get('carrera')
    turno = request.form.get('turno')
    
    # Procesar listas de deportes y pasatiempos
    deportes_lista = request.form.getlist('deportes')
    deportes = ", ".join(deportes_lista) if deportes_lista else "Ninguno"

    pasatiempos_lista = request.form.getlist('pasatiempos')
    pasatiempos = ", ".join(pasatiempos_lista) if pasatiempos_lista else "Ninguno"

    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO alumnos (nombre, control, fecha_nacimiento, carrera, turno, deportes, pasatiempos) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (nombre, control, fecha_nacimiento, carrera, turno, deportes, pasatiempos)
    )
    conn.commit()
    cur.close()
    conn.close()

    return "<h1>¡Datos guardados con éxito en la base de datos de Postgres!</h1><br><a href='/'>Regresar</a>"

if __name__ == '__main__':
    app.run(debug=True)
