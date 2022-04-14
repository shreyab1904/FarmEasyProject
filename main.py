import flask
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import sqlite3

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()
listOfTables= conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='USER'").fetchall()
listOfTables1 = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='PRODUCT'").fetchall()

if listOfTables!=[]:
    print("Table User Already Exists ! ")
else:
    conn.execute(''' CREATE TABLE USER(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            firstname TEXT, lastname TEXT, DOB TEXT, email TEXT,   
                            phone INTEGER, password TEXT,
                            confirmpassword TEXT); ''')
print("Table User has created")

if listOfTables1!=[]:
    print("Product Table Already exists ! ")
else:
    conn.execute(''' CREATE TABLE PRODUCT(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        bname TEXT, pname TEXT, category TEXT, image BLOB,
                        price TEXT); ''')
print("Table Product has created")

@app.route("/")
def index():
    return render_template("/index.html")

@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        getemail = request.form['email']
        getpass = request.form['pass']
        print(getemail)
        print(getpass)
    try:
        query = "SELECT * FROM USER WHERE email='" + getemail + "' AND password='" + getpass + "'"
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        if len(result) > 0:
            for i in result:
                getname = i[1]
                getid = i[0]

            session["name"] = getname
            session["id"] = getid
            return redirect("/productdisplay")
    except Exception as e:
        print(e)

    return render_template("/userlogin.html")

@app.route("/usersignup", methods = ['GET','POST'])
def usersignup():

    if request.method == 'POST':
        getfirstname = request.form['firstname']
        getlastname = request.form['lastname']
        getDOB = request.form['DOB']
        getemail = request.form['email']
        getphone = request.form['phone']
        getpass = request.form['pass']
        getcnfpass = request.form['cnfpass']

        print(getfirstname)
        print(getlastname)
        print(getDOB)
        print(getemail)
        print(getphone)
        print(getpass)
        print(getcnfpass)

    try:
        query = cursor.execute("INSERT INTO USER(firstname,lastname,DOB,email,phone,password,confirmpassword)VALUES('"+getfirstname+"','"+getlastname+"','"+getDOB+"','"+getemail+"','"+getphone+"','"+getpass+"','"+getcnfpass+"')")
        conn.commit()
        print("SUCCESSFULLY ADDED")
        return redirect("/userlogin")
    except Exception as e:
        print(e)

    return render_template("/usersignup.html")

@app.route("/payment")
def userpaymentpage():
    return render_template("/userpaymentpage.html")


@app.route("/adminlogin", methods = ['GET','POST'])
def adminlogin():
    if request.method == 'POST':
        getname = request.form["name"]
        getpass = request.form["pass"]
    try:
        if getname == 'admin' and getpass == "12345":
            return redirect("/productentry")
        else:
            print("Invalid username and password")
    except Exception as e:
        print(e)
    return render_template("/adminlogin.html")

@app.route("/productentry", methods = ['GET','POST'])
def adminproductentry():
    if request.method == 'POST':
        getbname = request.form['bname']
        getpname = request.form['pname']
        getcategory = request.form['category']
        getimage = request.form['image']
        getprice = request.form['price']

        print(getbname)
        print(getpname)
        print(getcategory)
        print(getimage)
        print(getprice)

    try:
        query = "INSERT INTO PRODUCT(bname, pname, category, image, price)VALUES(?, ?, ?, ?, ?)"
        photo = convertToBinaryData(getimage)
        data = (getbname, getpname, getcategory, photo, getprice)
        cursor.execute(query, data)
        conn.commit()
        print("SUCCESSFULLY ADDED!")
    except Exception as e:
        print(e)

    return render_template("/adminproductentry.html")

@app.route("/productdisplay", methods = ['GET','POST'])
def userproductdisplay():
    cursor = conn.cursor()
    query="SELECT * FROM PRODUCT"
    cursor.execute(query)
    result = cursor.fetchall()

    return render_template("/userproductdisplay.html",product = result)

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

if __name__ == "__main__":
    app.run(debug=True)