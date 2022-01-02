from re import search
from flask import Flask, render_template, request, redirect, url_for, flash
from flask.json import jsonify
from flask_mysqldb import MySQL
import pymysql
# from app import app
# from config import mysql
from flask import jsonify
from werkzeug.wrappers import response

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'film'

mysql = MySQL(app)



@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM film")
    data = cur.fetchall()
    cur.close()
    return render_template('index2.html', film=data )

@app.route('/search',methods=['POST','GET'])
def search():
    cur = mysql.connection.cursor()
    if request.method == "POST":
        search = request.form['search']
        cur.execute("SELECT * FROM film WHERE title LIKE %s OR genre LIKE %s ", ('%'+search+'%','%'+search+'%'))
        data = cur.fetchall()
        return render_template('index2.html', film=data )

@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        title = request.form['title']
        genre = request.form['genre']
        rating = request.form['rating']
        duration = request.form['duration']
        quality = request.form['quality']
        trailer = request.form['trailer']
        watch = request.form['watch']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO film (title, genre, rating, duration, quality, trailer, watch) VALUES ( %s, %s, %s, %s, %s, %s, %s)", (title, genre, rating, duration, quality,trailer,watch))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['GET'])
def delete(id):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM film WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('Index'))

@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        genre = request.form['genre']
        rating = request.form['rating']
        duration = request.form['duration']
        quality = request.form['quality']
        trailer = request.form['trailer']
        watch = request.form['watch']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE film
               SET title=%s, genre=%s, rating=%s, duration=%s, quality=%s, trailer=%s, watch=%s
               WHERE id=%s
            """, (title, genre, rating, duration, quality, trailer, watch, id))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))

#API
		
@app.route('/api/insert', methods=['POST'])
def api_insert():
    cur = mysql.connection.cursor()
    if request.method == "POST":
        _title = request.form['title']
        _genre = request.form['genre']
        _rating = request.form['rating']
        _duration = request.form['duration']
        _quality = request.form['quality']
        _trailer = request.form['trailer']
        _watch = request.form['watch']		
        sqlQuery = "INSERT INTO film (title,genre,rating,duration,quality,trailer,watch) VALUES(%s, %s, %s, %s, %s,%s,%s)"
        bindData = (_title, _genre,_rating, _duration,_quality,_trailer,_watch)
        cur.execute(sqlQuery, bindData)
        mysql.connection.commit()
        respone = jsonify('Film added successfully!')
        respone.status_code = 200
        cur.close()
        return respone
    else:
        return not_found()
    # except Exception as e:
    #     return {'Error': str(e)}
		
@app.route('/api/get')
def api_film():
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT id, title, genre, rating, duration, quality,trailer,watch FROM film")
        data = cur.fetchall()
        respone = jsonify(data)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cur.close() 
		
@app.route('/api/get/<int:id>')
def api_select(id):
    cur = mysql.connection.cursor()
    try:
        # cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT id, title, genre, rating, duration, quality,trailer,watch FROM film WHERE id =%s", id)
        empRow = cur.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cur.close() 

@app.route('/api/delete/<int:id>', methods=['DELETE'])
def api_delete(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM film WHERE id =%s", (id,))
        mysql.connection.commit()
        respone = jsonify('Film deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cur.close() 
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    app.run(debug=True)
