from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



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



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        id = request.form['id']
        title = request.form['title']
        genre = request.form['genre']
        rating = request.form['rating']
        duration = request.form['duration']
        quality = request.form['quality']
        trailer = request.form['trailer']
        watch = request.form['watch']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO film (id,title, genre, rating, duration, quality, trailer, watch) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (id,title, genre, rating, duration, quality,trailer,watch))
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


if __name__ == "__main__":
    app.run(debug=True)
