from flask import Flask
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        # These environment variables will be passed by Docker Compose
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'rootpassword'),
        database=os.environ.get('DB_NAME', 'appdb')
    )

@app.route('/')
def hello():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Create a table if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS visits (id INT AUTO_INCREMENT PRIMARY KEY, count INT)")
        
        # Check current visits
        cursor.execute("SELECT count FROM visits WHERE id = 1")
        result = cursor.fetchone()
        
        if not result:
            cursor.execute("INSERT INTO visits (count) VALUES (1)")
            visits = 1
        else:
            visits = result[0] + 1
            cursor.execute("UPDATE visits SET count = %s WHERE id = 1", (visits,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return f"<h1>Success!</h1><p>Database connected. This page has been viewed <b>{visits}</b> times.</p>"
    except Exception as e:
        return f"<h1>Database connection failed!</h1><p>Error: {e}</p><p>Refresh in a few seconds, the database might still be booting up.</p>"

if __name__ == '__main__':
    # Run the app on all network interfaces
    app.run(host='0.0.0.0', port=5000)