import sqlite3

# connect to the SQLite database ( or create it if doesn't exist)

conn = sqlite3.connect('licensePlates.db')

# create a cursor object to interact with the database
cursor = conn.cursor()

# create a table to store license plate data
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS licensePlates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time TEXT,
        end_time TEXT,
        License_plate TEXT
    )
    '''
)