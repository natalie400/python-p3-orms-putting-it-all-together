import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self,name = "joey",breed ="cocker spaniel"):
        self.name = name
        self.breed = breed
        self.id = None

    @classmethod 
    def create_table(cls):
        CURSOR.execute("""
                       
                      CREATE TABLE IF NOT EXISTS dogs(
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       breed TEXT
                      ) 
                       
                       """)
        CONN.commit()

    @classmethod
    def drop_table(self):
        CURSOR.execute('DROP TABLE IF EXISTS dogs')
        CONN.commit()

    def save(self):
        # If the Dog instance doesn't have an ID, insert a new row into the database
        if not self.id:
            CURSOR.execute('''
                INSERT INTO dogs (name, breed) VALUES (?, ?)
            ''', (self.name, self.breed))
            self.id = CURSOR.lastrowid  # Update the instance's ID with the newly assigned ID
            CONN.commit()

    @classmethod
    def create(cls, name, breed):
        # Create a new row in the database and return a new instance of the Dog class
        dog_instance = cls(name, breed)
        dog_instance.save()  # Reusing the save() method to save the new instance to the database
        return dog_instance

    @classmethod
    def new_from_db(cls, row):
        # Create a Dog instance from a database row
        dog_instance = cls(row[1], row[2])  # Assuming the order of columns is id, name, breed
        dog_instance.id = row[0]  # Assign the ID from the database row to the instance
        return dog_instance

    @classmethod
    def get_all(cls):
        # Return a list of Dog instances for every record in the dogs table
        CURSOR.execute('SELECT * FROM dogs')
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        # Find a Dog instance by name using SQL statement
        CURSOR.execute('SELECT * FROM dogs WHERE name = ?', (name,))
        row = CURSOR.fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_by_id(cls, dog_id):
        # Find a Dog instance by ID using SQL statement
        CURSOR.execute('SELECT * FROM dogs WHERE id = ?', (dog_id,))
        row = CURSOR.fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_or_create_by(cls, name, breed):
        # Find a dog by name and breed, or create a new one if not found
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            new_dog = cls.create(name, breed)
            return new_dog

    def update(self):
        # Update the database row with the new name of the Dog instance
        if self.id:
            CURSOR.execute('''
                UPDATE dogs SET name = ? WHERE id = ?
            ''', (self.name, self.id))
            CONN.commit()