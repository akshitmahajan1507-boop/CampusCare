
from database import get_connection

try:
    connection = get_connection()

    if connection.is_connected():
        print("CampusCare database connected successfully!")

    connection.close()

except Exception as error:
    print("Database connection failed:", error)
