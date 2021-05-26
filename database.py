import sqlite3


def initialize_db():
    """Creates the table, if needed"""

    conn = sqlite3.connect("passwordEntries.db")
    cursor = conn.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS passwordEntry (
                           titel text,
                            url text,
                            username text,
                            password text,
                            id text
                            )
    """)

    conn.commit()
    conn.close()


def search_entries(term):
    """Searches the database entries for the given terms"""
    conn = sqlite3.connect("passwordEntries.db")
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM passwordEntry where id LIKE :term
                   or titel LIKE :term 
                   or url LIKE :term 
                   or username LIKE :term""",
                   {'term': "%{}%".format(term)})
    records = cursor.fetchall()

    conn.commit()
    conn.close()

    return records


def add_to_database(entry):
    """Adds the given entry to the database"""

    conn = sqlite3.connect("passwordEntries.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO passwordEntry VALUES (:titel, :url, :username, :password, :id)",
                   {
                       'titel': entry.get_titel(),
                       'url': entry.get_url(),
                       'username': entry.get_username(),
                       'password': str(entry.get_password()),
                       'id': entry.get_id()
                   }
                   )
    conn.commit()
    conn.close()


def read_from_database():
    """Returns every existing entry from the database"""

    conn = sqlite3.connect("passwordEntries.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM passwordEntry")
    records = cursor.fetchall()

    conn.commit()
    conn.close()

    return records


def delete_entry(entry_id):
    """Deletes all entries with the given id."""

    conn = sqlite3.connect("passwordEntries.db")
    cursor = conn.cursor()

    if entry_id != "":
        cursor.execute("DELETE FROM passwordEntry where id = ? ", (entry_id,))
    else:
        conn.commit()
        conn.close()

        return False

    conn.commit()
    conn.close()

    return True


def update_entry(entry):
    """Updates all entries with the given id"""

    conn = sqlite3.connect("passwordEntries.db")
    cursor = conn.cursor()

    cursor.execute("""UPDATE passwordEntry SET 
                titel = :titel,
                url = :url,
                username = :username,
                password = :password

                WHERE id = :id""",
                   {
                       'titel': entry.get_titel(),
                       'url': entry.get_url(),
                       'username': entry.get_username(),
                       'password': str(entry.get_password()),
                       'id': entry.get_id()
                   }
                   )
    conn.commit()
    conn.close()


def read_one_from_database(id_param):
    """Returns all entries with the given id"""

    conn = sqlite3.connect("passwordEntries.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM passwordEntry where id = ?", (id_param,))
    records = cursor.fetchall()

    conn.commit()
    conn.close()

    return records
