from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db'  # Nombre del servicio MySQL definido en docker-compose.yml
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'usuario'

mysql = MySQL(app)


@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Bienvenido a mi aplicación"})

@app.route('/users', methods=['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    data = cur.fetchone()
    cur.close()
    return jsonify(data)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    name = data['name']
    last_name = data['last_name']
    phone = data['phone']
    email = data['email']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (name, last_name, phone, email) VALUES (%s, %s, %s, %s)",
                (name, last_name, phone, email))
    mysql.connection.commit()
    cur.close()
    
    return jsonify({"message": "User added successfully"})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    name = data['name']
    last_name = data['last_name']
    phone = data['phone']
    email = data['email']
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET name = %s, last_name = %s, phone = %s, email = %s WHERE id = %s",
                (name, last_name, phone, email, user_id))
    mysql.connection.commit()
    cur.close()
    
    return jsonify({"message": "User updated successfully"})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    
    return jsonify({"message": "User deleted successfully"})

def create_user_table():
    cur = mysql.connection.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            email VARCHAR(255) NOT NULL
        )
    ''')
    mysql.connection.commit()
    cur.close()

if __name__ == '__main__':
    with app.app_context():
        create_user_table()
    app.run(host='0.0.0.0', port=5000)
    
