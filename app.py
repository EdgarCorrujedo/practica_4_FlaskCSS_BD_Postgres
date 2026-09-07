import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100),
                numero_control VARCHAR(50),
                carrera VARCHAR(100),
                turno VARCHAR(20),
                fecha_nacimiento DATE,
                pasatiempos TEXT,
                deportes TEXT
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Tabla inicializada correctamente.")
    except Exception as e:
        print(f"Error al inicializar base de datos: {e}")

# Inicializar la base de datos
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        numero_control = request.form.get('numero_control')
        carrera = request.form.get('carrera')
        turno = request.form.get('turno')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        pasatiempos = request.form.get('pasatiempos')
        deportes = request.form.get('deportes')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO usuarios (nombre, numero_control, carrera, turno, fecha_nacimiento, pasatiempos, deportes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (nombre, numero_control, carrera, turno, fecha_nacimiento, pasatiempos, deportes))
        
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
