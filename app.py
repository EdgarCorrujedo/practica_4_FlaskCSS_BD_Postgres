import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        raise ValueError("La variable de entorno DATABASE_URL no está configurada en Render.")
    conn = psycopg2.connect(db_url)
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

# Inicializar la base de datos al arrancar
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        try:
            nombre = request.form.get('Nombre')
            numero_control = request.form.get('NumeroControl')
            fecha_nacimiento = request.form.get('FechaNacimiento') or None
            carrera = request.form.get('Carrera')
            turno = request.form.get('Turno')
            
            # Obtener listas de checkboxes
            deportes_lista = request.form.getlist('Deportes')
            pasatiempos_lista = request.form.getlist('Pasatiempos')

            # Si la lista tiene elementos los une con coma; si está vacía, envía None (NULL en Postgres)
            deportes = ", ".join(deportes_lista) if deportes_lista else None
            pasatiempos = ", ".join(pasatiempos_lista) if pasatiempos_lista else None

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

        except Exception as e:
            print(f"Error al guardar datos: {e}")
            return f"Error en la base de datos: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
