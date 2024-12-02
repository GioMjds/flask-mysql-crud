from flask import Blueprint, jsonify, render_template, request, redirect, url_for
import mysql.connector

crud = Blueprint('crud', __name__, template_folder='templates')

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'users_db',
    'auth_plugin': 'mysql_native_password',
}

@crud.route('/', methods=['GET', 'POST'])
def test():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            return jsonify({'message': 'Database connection successful. You may type to the URL /read to continue'}), 200
    except mysql.connector.Error as e:
        return jsonify({'message': f'Database connection failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# Create operation
@crud.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        birthday = request.form['birthday']
        username = request.form['username']
        password = request.form['password']
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO users_info (firstname, middlename, lastname, birthday, username, password) VALUES (%s, %s, %s, %s, %s, %s)', (firstname, middlename, lastname, birthday, username, password))
            conn.commit()
            return redirect(url_for('crud.read'))
        except mysql.connector.Error as e:
            return f"Adding data failed! Error: {str(e)}"
        finally:
            cursor.close()
            conn.close()
    else:
        return render_template('create.html')

# Read operation
@crud.route('/read')
def read():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users_info')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', data=data)

# Update operation
@crud.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    if request.method == 'POST':
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        birthday = request.form['birthday']
        username = request.form['username']
        password = request.form['password']
        
        try:
            cursor.execute('UPDATE users_info SET firstname=%s, middlename=%s, lastname=%s, birthday=%s, username=%s, password=%s WHERE id=%s', 
                            (firstname, middlename, lastname, birthday, username, password, id))
            conn.commit()
            return f'''
            <script>
                alert('Data updated successfully');
                window.location.href = "{url_for('crud.read')}";
            </script>'''
        except mysql.connector.Error as e:
            return f"Updating data failed! Error: {str(e)}"
    else:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM users_info WHERE id=%s', (id,))
            data = cursor.fetchone()
            if data is None:
                return 'Data not found!', 404
            return render_template('update.html', data=data)
        except mysql.connector.Error as e:
            return f"Fetching data failed! Error: {str(e)}"
        finally:
            cursor.close()
            conn.close()
            return render_template('update.html', data=data)
    
# Delete operation
@crud.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM users_info WHERE id=%s', (id,))
        conn.commit()
        return redirect(url_for('crud.read'))
    except mysql.connector.Error as e:
        return f"Deleting data failed! Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()