from datetime import date
from flask import Flask, render_template, request
import sqlite3 as sql
import hashlib
import datetime

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

max_listing_num=-1

def encrypt(password):
    return hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest()

@app.route('/')
def login():
    return render_template('UserLogIn.html')


@app.route('/main', methods=['POST', 'GET'])
def loginmain():
    if request.method == 'POST':
        result = checkPassword(request.form['email'], request.form['password'])
        if result==0:
            connection = sql.connect('database.db')
            cursor=connection.cursor()
            cursor.execute('select * from Sellers where email=?;',(request.form['email'],))
            row=cursor.fetchone()
            if row==None:
                seller=0
            else:
                seller=1
            print("seller:",seller)
            return render_template('main.html',email=request.form['email'],seller=seller)
        else:
            print("UserLogInFailed")
            return render_template('UserLogInFailed.html')

@app.route('/main/<email>',methods=['POST'])
def Main(email):
    connection = sql.connect('database.db')
    cursor=connection.cursor()
    cursor.execute('select * from Sellers where email=?;',(email,))
    row=cursor.fetchone()
    if row==None:
        seller=0
    else:
        seller=1
    print("seller:",seller)
    return render_template('main.html',email=email,seller=seller)

@app.route("/user/<email>",methods=['POST'])
def user(email):
    connection = sql.connect('database.db')
    cursor=connection.cursor()
    cursor.execute('SELECT * FROM User_Profile WHERE email=?;',(email,))
    row=cursor.fetchone()
    print(row)
    return render_template('user.html',profile=row)

@app.route('/seller/<email>',methods=['POST'])
def product(email):
    connection = sql.connect('database.db')
    cursor=connection.cursor()
    cursor.execute('select Title,Listing_ID from Product_Listing where Seller_Email=?;',(email,))
    row=cursor.fetchall()
    print(row)
    return render_template('addproduct.html',email=email,products=row)

@app.route('/addsuccess/<email>',methods=['POST'])
def addsuccess(email):
    connection = sql.connect('database.db')
    cursor=connection.cursor()
    cursor.execute('insert into Product_Listing values (?,?,?,?,?,?,?,?)',(email,request.form['listing_id'],request.form['category'],request.form['title'],request.form['name'],request.form['description'],request.form['price'],request.form['quantity']))
    cursor.execute('insert into Product_Periods (email,Listing_ID,Add_Time) values (?,?,?)',(email,request.form['listing_id'],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    connection.commit()
    return render_template('addsuccess.html',email=email)

@app.route('/removesuccess/<email>/<id>',methods=['POST'])
def remove(email,id):
    connection = sql.connect('database.db')
    cursor=connection.cursor()
    cursor.execute('delete from Product_Listing where Seller_Email=? and Listing_ID=?',(email,id))
    cursor.execute('select * from Product_Periods where email=? and Listing_ID=?',(email,id))
    row=cursor.fetchall()
    print(row)
    if len(row)==0:
        cursor.execute('insert into Product_Periods (email,Listing_ID,Remove_Time) values (?,?,?)',(email,id,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    else:
        cursor.execute('update Product_Periods set Remove_Time=? where email=? and Listing_ID=?',(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),email,id))
    cursor.execute('select * from Product_Periods where email=? and Listing_ID=?',(email,id))
    row=cursor.fetchone()
    print(row)
    connection.commit()
    return render_template('removesuccess.html',email=email)

@app.route('/changepassword/<email>', methods=['POST'])
def changepassword(email):
    connection = sql.connect('database.db')
    cursor=connection.cursor()
    cursor.execute('UPDATE Users SET encrypt=? WHERE email=?;',(encrypt(request.form['password']),email))
    connection.commit()
    return render_template('/changepassword.html',email=email)

@app.route('/categories/<name>',methods=['POST'])
def get_categories(name):
    connection = sql.connect('database.db')
    cursor=connection.cursor()
    row2=[]
    row1=[]
    if name=="all":
        cursor.execute('select category_name from Categories where parent_category="Root";')
        row1=cursor.fetchall()
    else:
        cursor.execute('select category_name from Categories where parent_category=?;',(name,))
        row1=cursor.fetchall()
        cursor.execute('select distinct * from Product_Listing where Category=?;',(name,))
        row2=cursor.fetchall()
    print(len(row1))
    print(row1)
    return render_template('/categories.html',categoryName=name,subcategories=row1,products=row2)

@app.route('/product/<email>/<id>',methods=['POST'])
def get_product(email,id):
    connection = sql.connect('database.db')
    cursor=connection.cursor()
    cursor.execute('select * from Product_Listing where Seller_Email=? and Listing_ID=?',(email,id))
    row=cursor.fetchone()
    print(row)
    return render_template('/product.html',product=row)

def checkPassword(email, password):
    connection = sql.connect('database.db')
    encrypt_password=encrypt(password)
    print(encrypt_password)
    cursor=connection.cursor()
    cursor.execute('SELECT * FROM Users WHERE email=?;',(email,))
    row=cursor.fetchone()
    print(row)
    if row is None or row[2] != encrypt_password:
        return -1
    return 0

if __name__ == "__main__":
    app.run()


