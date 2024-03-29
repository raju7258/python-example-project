import configparser
from flask import Flask, render_template, request
import mysql.connector
import os

# Read configuration from file.
config = configparser.ConfigParser()
config.read('config.ini')

# Fetch connection credentails to a variable
USER_NAME = os.environ.get('MYSQLCONNSTR_mysql_server_username')
PASSWORD = os.environ.get('MYSQLCONNSTR_mysql_server_password')
FQDN = os.environ.get('MYSQLCONNSTR_mysql_server_fqdn')

# Set up application server.
app = Flask(__name__)

# Create a function for fetching data from the database.
def sql_query(sql):
    # db = mysql.connector.connect(**config['mysql.connector'])
    db = mysql.connector.connect(user=USER_NAME, password=PASSWORD, host=FQDN, database='web_database_project'
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def sql_execute(sql):
    db = mysql.connector.connect(user=USER_NAME, password=PASSWORD, host=FQDN, database='web_database_project'
    # db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

# For this example you can select a handler function by
# uncommenting one of the @app.route decorators.

#@app.route('/')
def basic_response():
    return "It works!" #example

#@app.route('/')
def template_response():
    return render_template('home.html')

@app.route('/', methods=['GET', 'POST'])
def template_response_with_data():
    print(request.form)
    if "buy-book" in request.form:
        book_id = int(request.form["buy-book"])
        sql = "delete from book where id={book_id}".format(book_id=book_id)
        sql_execute(sql)
    template_data = {}
    sql = "select id, title from book order by title"
    books = sql_query(sql)
    template_data['books'] = books
    return render_template('home-w-data.html', template_data=template_data)

if __name__ == '__main__':
    app.run(**config['app'])
