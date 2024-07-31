import sqlite3


def create_tables():
    with sqlite3.connect('static/database.db') as conn:
        cursor = conn.cursor()

        # Create Reservations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                start TEXT NOT NULL,
                end TEXT NOT NULL,
                description TEXT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(id)
            )
        ''')

        # Insert some initial data into Reservations table
        cursor.execute('''
            INSERT INTO Reservations (title, start, end, description, user_id) VALUES
            ('Consultation', '2023-06-20T10:00:00', '2023-06-20T11:00:00', 'Consultation with client', 1),
            ('Consultation', '2023-06-22T14:00:00', '2023-06-22T15:00:00', 'Consultation with client', 2)
        ''')

        conn.commit()

create_tables()