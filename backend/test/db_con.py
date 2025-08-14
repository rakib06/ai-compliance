import psycopg2
from psycopg2 import OperationalError
DATABASE_URL=r"postgres://k7bcef0f:SDVXnONOpZDR@postgres-service-ydjtv.db.eu-east-1.onmiget.com:5432/fbnmyhk1"

def test_connection():
    try:
        # Replace with your actual connection URL
        connection_url = DATABASE_URL
        connection = psycopg2.connect(connection_url)
        print("Connection successful!")
        connection.close()
    except OperationalError as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()