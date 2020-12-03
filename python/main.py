from flask import Flask, g, request
import sqlite3
import json

app = Flask(__name__)

DATABASE = 'C:\\Work\\library\\library.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = dict_factory
    return db

def get_genre_id(genre_id, genre_new_text, db):
    if genre_id == 'new':
        result = db.execute("""SELECT id 
                    FROM genre
                    WHERE name = ?;""", (genre_new_text,)).fetchone()

        if result != None:
            db.execute("""INSERT INTO genre (name) VALUES (?);""", (genre_new_text,))

            db.commit()

            result = db.execute("""SELECT id 
                                FROM genre
                                WHERE name = ?;""", (genre_new_text,)).fetchone()



            return result["id"]

        else:
            db.execute("""INSERT INTO genre (name) VALUES (?);""", (genre_new_text,))

            db.commit()

            result = db.execute("""SELECT id 
                                            FROM genre
                                            WHERE name = ?;""", (genre_new_text,)).fetchone()

            return result["id"]

    else:
        return genre_id;


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/addbook', methods=['POST'])
def add_book():
    db = get_db()

    title = request.form['title']
    author = request.form['author']
    year = request.form['year']
    genre_id = request.form['genre']
    genre_new_text = request.form['genre_text']

    genre_id = get_genre_id(genre_id,genre_new_text,db)

    db.execute("""INSERT INTO books (title, author, year, genre_id, available) VALUES (?, ?, ?, ?, 1) """,
               (title, author, year, genre_id))

    db.commit()

    result = db.execute("""SELECT title, author, year, genre.name, available , book_id
                        FROM books 
                        JOIN genre
                        ON genre.id = books.genre_id;""").fetchall()

    return json.dumps(result)

@app.route('/getgenres')
def get_genres():
    db = get_db()

    result = db.execute("""SELECT * FROM genre""")

    return json.dumps(result)

@app.route('/setavail', methods=['POST'])
def set_avalibility():
    db = get_db()

    id = request.form['book_id']
    availability = request.form['availability']

    db.execute("""UPDATE books SET available = ? WHERE book_id = ?""", (availability, id))

    db.commit()

    result = db.execute("""SELECT title, author, year, genre.name, available , book_id
                            FROM books 
                            JOIN genre
                            ON genre.id = books.genre_id;""").fetchall()

    return json.dumps(result)

@app.route('/getbooks/avalible')
def get_books():
    db = get_db()

    result = db.execute("""SELECT title, author, year, genre.name, available , book_id
                        FROM books 
                        JOIN genre
                        ON genre.id = books.genre_id
                        WHERE available = 1;""").fetchall()

    return json.dumps(result)


@app.route('/getbooks/all')
def get_books_all():
    db = get_db()

    result = db.execute("""SELECT title, author, year, genre.name, available, book_id
                        FROM books 
                        JOIN genre
                        ON genre.id = books.genre_id;""").fetchall()

    return json.dumps(result)

#/getbooks/search/<queryGoesHere>
@app.route('/getbooks/search/<query>')
def get_books_query(query):
    db = get_db()

    result0 = db.execute("""SELECT title, author, year, genre.name, available, book_id
                            FROM books 
                            JOIN genre
                            ON genre.id = books.genre_id
                            WHERE title 
                            LIKE '%' || ? || '%';""", (query,)).fetchall()

    result1 = db.execute("""SELECT title, author, year, genre.name, available, book_id
                            FROM books 
                            JOIN genre
                            ON genre.id = books.genre_id
                            WHERE author
                            LIKE '%' || ? || '%';""", (query,)).fetchall()

    result2 = db.execute("""SELECT title, author, year, genre.name, available, book_id
                            FROM books 
                            JOIN genre
                            ON genre.id = books.genre_id
                            WHERE year
                            LIKE '%' || ? || '%';""", (query,)).fetchall()

    result3 = db.execute("""SELECT title, author, year, genre.name, available, book_id
                            FROM books 
                            JOIN genre
                            ON genre.id = books.genre_id
                            WHERE genre.name
                            LIKE '%' || ? || '%';""", (query,)).fetchall()

    result = result0 + result1 + result2 + result3
    resultNew = []

    for book in result:
        id = book['book_id']
        resultNew.append(book)
        result.remove(book)
        for book2 in result:
            if book2["book_id"] != id:
                resultNew.append(book2)
                result.remove(book2)
            else:
                result.remove(book2)

    return json.dumps(resultNew)


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)

