import sqlite3

URL='app/search_photos/photos.db'

def create():
    with sqlite3.connect(URL) as connection:
        cursor = connection.cursor()
        with connection:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS photos (
            link TEXT NOT NULL,
            date INTEGER
            );
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS descriptions (
            fname TEXT NOT NULL PRIMARY KEY,
            description TEXT
            );
            ''')
            cursor.execute('''
            DELETE FROM photos;
            ''')
            # cursor.execute('''
            # DELETE FROM descriptions;
            # ''')
        with connection:
            try:
                cursor.execute('''
                DELETE FROM SQLITE_SEQUENCE WHERE name='photos';
                ''')
                # cursor.execute('''
                # DELETE FROM SQLITE_SEQUENCE WHERE name='descriptions';
                # ''')
            except:
                pass



def trunc_descs():
    with sqlite3.connect(URL) as connection:
        cursor = connection.cursor()
        
        with connection:
            cursor.execute('''
            DELETE FROM descriptions;
            ''')
        with connection:
            try:
                cursor.execute('''
                DELETE FROM SQLITE_SEQUENCE WHERE name='descriptions';
                ''')
            except:
                pass

def save_link(js):
    '''[{url:str, date:str}]'''
    sqltuples = [(i['url'], int(i['date'])) for i in js]
    with sqlite3.connect(URL) as connection:
        cursor = connection.cursor()
        with connection:
            cursor.executemany('INSERT INTO photos (link, date) VALUES (?,?)', sqltuples)

def get_links():
    '''->[(url),]'''
    with sqlite3.connect(URL) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT link FROM photos ORDER BY date")

        rows = cursor.fetchall()

        return rows
    
def save_desc(js):
    '''[{fname:str, desc:str}]'''
    sqltuples = [(i['fname'], i['desc']) for i in js]
    with sqlite3.connect(URL) as connection:
        cursor = connection.cursor()
        with connection:
            try:
                cursor.executemany('INSERT INTO descriptions (fname, description) VALUES (?,?)', sqltuples)
            except:
                pass

def get_descs():
    with sqlite3.connect(URL) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM descriptions")
        rows = cursor.fetchall()
        return rows