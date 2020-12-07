from flask import Flask, g, request, render_template
import sqlite3
import json

app = Flask(__name__)

DATABASE = 'C:\\Work\\Training\\Databases\\Library\\library.db'

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
        return genre_id


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET','POST'])
def serve_index():
    db = get_db()

    result = db.execute("""SELECT title, author, year, genre.name, available , book_id
                        FROM books 
                        JOIN genre
                        ON genre.id = books.genre_id
                        WHERE available = 1;""").fetchall()

    return render_template('index.html', books=result)

@app.route('/bookadd')
def book_add():
    db = get_db()

    result = db.execute("""SELECT * FROM genre""")

    return render_template('add-book.html', genres=result)

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

    return render_template('index.html', books=result, message="Book added.")

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
    return render_template('index.html', books=result)

@app.route('/getbooks/available')
def get_books():
    db = get_db()

    result = db.execute("""SELECT title, author, year, genre.name, available , book_id
                        FROM books 
                        JOIN genre
                        ON genre.id = books.genre_id
                        WHERE available = 1;""").fetchall()

    return json.dumps(result)


@app.route('/getbooks/all', methods=['GET','POST'])
def get_books_all():
    db = get_db()

    result = db.execute("""SELECT title, author, year, genre.name, available, book_id
                        FROM books 
                        JOIN genre
                        ON genre.id = books.genre_id;""").fetchall()

    return render_template('index.html', books=result, showChecked=True)

#/getbooks/search/<queryGoesHere>
@app.route('/getbooks/search', methods=['POST'])
def get_books_query():
    order_by = request.form['filter_by']
    query = request.form['query']
    db = get_db()
    db.set_trace_callback(print)

    result = []

    if order_by == 'title':
        result = db.execute("""SELECT title, author, year, genre.name, available, book_id
                                FROM books 
                                JOIN genre
                                ON genre.id = books.genre_id
                                WHERE title LIKE '%' || ? || '%'
                                OR author LIKE '%' || ? || '%'
                                OR year LIKE '%' || ? || '%'
                                OR genre.name LIKE '%' || ? || '%'
                                ORDER BY title ASC;""", (query, query, query, query)).fetchall()

    elif order_by == 'author':
        result = db.execute("""SELECT title, author, year, genre.name, available, book_id
                                FROM books 
                                JOIN genre
                                ON genre.id = books.genre_id
                                WHERE title LIKE '%' || ? || '%'
                                OR author LIKE '%' || ? || '%'
                                OR year LIKE '%' || ? || '%'
                                OR genre.name LIKE '%' || ? || '%'
                                ORDER BY author ASC;""", (query, query, query, query)).fetchall()

    elif order_by == 'year':
        result = db.execute("""SELECT title, author, year, genre.name, available, book_id
                                FROM books 
                                JOIN genre
                                ON genre.id = books.genre_id
                                WHERE title LIKE '%' || ? || '%'
                                OR author LIKE '%' || ? || '%'
                                OR year LIKE '%' || ? || '%'
                                OR genre.name LIKE '%' || ? || '%'
                                ORDER BY year ASC;""", (query, query, query, query)).fetchall()

    elif order_by == 'genre.name':
        result = db.execute("""SELECT title, author, year, genre.name, available, book_id
                                FROM books 
                                JOIN genre
                                ON genre.id = books.genre_id
                                WHERE title LIKE '%' || ? || '%'
                                OR author LIKE '%' || ? || '%'
                                OR year LIKE '%' || ? || '%'
                                OR genre.name LIKE '%' || ? || '%'
                                ORDER BY genre.name ASC;""", (query, query, query, query)).fetchall()

    return render_template('index.html', books=result)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)

