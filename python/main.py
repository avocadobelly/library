from flask import Flask, g
import sqlite3
import json

app = Flask(__name__)

DATABASE = 'C:\\Work\\library\\library.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/getbooks/avalible')
def getBooks():
    db = get_db()

    result = db.execute("""SELECT title, author, year, genre.name, available 
                        FROM books 
                        JOIN genre
                        ON genre.id = books.genre_id
                        WHERE available = 1;""").fetchall()
    return json.dumps(result)

@app.route('/getbooks/all')
def getBooksAll():
    db = get_db()

    result = db.execute("""SELECT title, author, year, genre.name, available 
                        FROM books 
                        JOIN genre
                        ON genre.id = books.genre_id;""").fetchall()
    return json.dumps(result)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
