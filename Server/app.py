from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Funciona la aplicacion"})


@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = psycopg2.connect(
            host="db",
            database="usuarios",
            user="admin",
            password="admin"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "Error al obtener usuarios", "details": str(e)}), 500



@app.route('/users/<string:user_phone>', methods=['GET'])
def get_user_by_phone(user_phone):
    try:
        conn = psycopg2.connect(
            host="db",
            database="usuarios",
            user="admin",
            password="admin"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE phone = %s", (user_phone,))
        data = cursor.fetchone()
        cursor.close()

        if data:
            return jsonify(data)
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "Error al obtener el usuario", "details": str(e)}), 500


@app.route('/users', methods=['POST'])
def add_user():
    try:
        conn = psycopg2.connect(
            host="db",
            database="usuarios",
            user="admin",
            password="admin"
        )
        data = request.json
        name = data['name']
        last_name = data['last_name']
        phone = data['phone']
        email = data['email']

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, last_name, phone, email) VALUES (%s, %s, %s, %s)",
            (name, last_name, phone, email)
        )
        conn.commit()
        cursor.close()

        return jsonify({"message": "User added successfully"})
    except Exception as e:
        return jsonify({"error": "Error al agregar el usuario", "details": str(e)}), 500



@app.route('/users/<string:user_phone>', methods=['PUT'])
def update_user_by_phone(user_phone):
    try:
        conn = psycopg2.connect(
            host="db",
            database="usuarios",
            user="admin",
            password="admin"
        )
        data = request.json
        name = data['name']
        last_name = data['last_name']
        email = data['email']

        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET name = %s, last_name = %s, email = %s WHERE phone = %s",
            (name, last_name, email, user_phone)
        )
        conn.commit()
        cursor.close()

        return jsonify({"message": "User updated successfully"})
    except Exception as e:
        return jsonify({"error": "Error al actualizar el usuario", "details": str(e)}), 500

@app.route('/users/<string:user_phone>', methods=['DELETE'])
def delete_user_by_phone(user_phone):
    try:
        conn = psycopg2.connect(
            host="db",
            database="usuarios",
            user="admin",
            password="admin"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE phone = %s", (user_phone,))
        conn.commit()
        cursor.close()

        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        return jsonify({"error": "Error al eliminar el usuario", "details": str(e)}), 500
    
def create_database():
    try:
        conn = psycopg2.connect(
            host="db",
            database="postgres",
            user="admin",
            password="admin"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT datname FROM pg_database WHERE datname = 'usuarios'")
        existe = cursor.fetchone()

        if not existe:
            cursor.execute("CREATE DATABASE usuarios")
            print("Base de datos creada.")
        else:
            print("Base de datos existente.")

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print("Error al crear la base de datos:", e)

def create_user_table() :
    try:
        conn = psycopg2.connect(
            host="db",
            database="usuarios",
            user="admin",
            password="admin"
        )
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(255) NOT NULL
            );
            """
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Tabla creada o existente.")
    except Exception as e:
        print("Error al crear la tabla:", e)


create_database()
create_user_table() 

if __name__ == '__main__':
    app.run(host='0.0.0.0')

