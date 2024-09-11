from __init__ import CURSOR, CONN

class Department:
    def __init__(self, name, location, id=None):
        self.name = name
        self.location = location
        self.id = id

    @classmethod
    def create_table(cls):
        """Create the departments table if it does not exist."""
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the departments table if it exists."""
        sql = "DROP TABLE IF EXISTS departments"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Save the Department instance to the database."""
        if self.id is None:
            sql = "INSERT INTO departments (name, location) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.location))
            self.id = CURSOR.lastrowid
        else:
            self.update()
        CONN.commit()

    @classmethod
    def create(cls, name, location):
        """Create a new Department instance and save it to the database."""
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Update the Department instance in the database."""
        if self.id is None:
            raise ValueError("Cannot update a department that is not saved")
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the Department instance from the database."""
        if self.id is None:
            raise ValueError("Cannot delete a department that is not saved")
        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
