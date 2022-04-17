import flask
from flask import Flask, render_template, request, redirect, session
from flask_session import Session

from instamojo_wrapper import Instamojo

API_KEY = "test_ae0ed2ba0300671b76829da7965"
AUTH_TOKEN = "test_4da4849c457db419475e7b97b4c"
api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')
import sqlite3

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()
listOfTables = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='USER'").fetchall()
listOfTables1 = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='PRODUCT'").fetchall()

if listOfTables != []:
    print("Table User Already Exists ! ")
else:
    conn.execute(''' CREATE TABLE USER(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            firstname TEXT, lastname TEXT, DOB TEXT, email TEXT,   
                            phone INTEGER, password TEXT,
                            confirmpassword TEXT); ''')
print("Table User has created")

if listOfTables1 != []:
    print("Product Table Already exists ! ")
else:
    conn.execute(''' CREATE TABLE PRODUCT(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        productid TEXT, bname TEXT, pname TEXT, category TEXT, image BLOB,
                        price TEXT); ''')
print("Table Product has created")


@app.route("/")
def homepage():
    return render_template("/homepage.html")


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


@app.route("/usersignup", methods=['GET', 'POST'])
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
        query = cursor.execute(
            "INSERT INTO USER(firstname,lastname,DOB,email,phone,password,confirmpassword)VALUES('" + getfirstname + "','" + getlastname + "','" + getDOB + "','" + getemail + "','" + getphone + "','" + getpass + "','" + getcnfpass + "')")
        conn.commit()
        print("SUCCESSFULLY ADDED")
        return redirect("/userlogin")
    except Exception as e:
        print(e)

    return render_template("/usersignup.html")


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        getname = request.form["name"]
        getpass = request.form["pass"]
    try:
        if getname == 'admin' and getpass == "12345":
            return redirect("/dashboard")
        else:
            print("Invalid username and password")
    except Exception as e:
        print(e)
    return render_template("/adminlogin.html")


@app.route("/dashboard")
def admindashoard():
    return render_template("/admindashboard.html")


@app.route("/productmanagement")
def adminproductmanagement():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCT")
    result = cursor.fetchall()
    return render_template("/adminproductmanagement.html", product=result)


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


@app.route("/productentry", methods=['GET', 'POST'])
def adminproductentry():
    if request.method == 'POST':
        getpid = request.form['pid']
        getbname = request.form['bname']
        getpname = request.form['pname']
        getcategory = request.form['category']
        getimage = request.files['img']
        getprice = request.form['price']

        print(getpid)
        print(getbname)
        print(getpname)
        print(getcategory)
        print(getimage)
        print(getprice)

    try:
        if getimage.filename != '':
            getimage.save(getimage.filename)
        photo = convertToBinaryData(getimage.filename)
        query = "INSERT INTO PRODUCT(productid, bname, pname, category, image, price)VALUES(?, ?, ?, ?, ?, ?)"
        data = (getpid, getbname, getpname, getcategory, photo, getprice)
        cursor.execute(query, data)
        conn.commit()
        print("SUCCESSFULLY ADDED!")
    except Exception as e:
        print(e)

    return render_template("/adminproductentry.html")


def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


@app.route("/productdisplay", methods=['GET', 'POST'])
def userproductdisplay():
    cursor = conn.cursor()
    query = cursor.execute("SELECT * FROM PRODUCT")
    result = cursor.fetchall()
    for x in result:
        pname = x[3]
        image = x[5]

    photopath = "C:\\Users\\yashi\\PycharmProjects\\FarmEasy\\uploads\\" + pname + ".png"
    print(photopath)
    writeTofile(image, photopath)

    return render_template("/userproductdisplay.html", product=result)


@app.route('/delete/<getpid>/', methods=['GET', 'POST'])
def delete(getpid):
    data = "DELETE FROM PRODUCT WHERE productid='" + getpid + "'"
    cursor.execute(data)
    conn.commit()
    return redirect("/productmanagement")


@app.route("/update/<getpid>/", methods=['GET', 'POST'])
def update(getpid):
    data = cursor.execute("SELECT * FROM PRODUCT WHERE productid = '" + getpid + "'")
    result = cursor.fetchall()
    if len(result) == 0:
        print("Invalid Data")
    else:
        if request.method == 'POST':
            getpid = request.form['pid']
            getbname = request.form['bname']
            getpname = request.form['pname']
            getcategory = request.form['category']
            getimage = request.files['img']
            getprice = request.form['price']

        try:
            query = "UPDATE PRODUCT SET productid = '" + getpid + "', bname = '" + getbname + "', pname = '" + getpname + "', category ='" + getcategory + "', image='" + getimage + "', price = '" + getprice + "'"
            cursor.execute(query)
            result = cursor.fetchall()
            conn.commit()
            return redirect("/productmanagement")

        except Exception as e:
            print(e)

        return render_template("/update.html", product=result)


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        getpid = request.form["pid"]
        print(getpid)
        try:
            query = "SELECT * FROM PRODUCT WHERE productid=" + getpid
            cursor.execute(query)
            print("SUCCESSFULLY SELECTED!")
            result = cursor.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid Product")
            else:
                return render_template("search.html", product=result, status=True)

        except Exception as e:
            print(e)

    return render_template("search.html", product=[], status=False)


@app.route("/display-snacks", methods=['GET', 'POST'])
def snacks():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCT WHERE category='Snacks'")
    result = cursor.fetchall()
    return render_template("/userproductdisplay.html", product=result)


@app.route("/display-beverages", methods=['GET', 'POST'])
def beverages():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCT WHERE category='Beverages'")
    result = cursor.fetchall()
    return render_template("/userproductdisplay.html", product=result)


@app.route("/display-bakery", methods=['GET', 'POST'])
def bakery():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCT WHERE category='Bakery'")
    result = cursor.fetchall()
    return render_template("/userproductdisplay.html", product=result)


@app.route("/display-fruits", methods=['GET', 'POST'])
def fruits():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCT WHERE category='Fruits'")
    result = cursor.fetchall()
    return render_template("/userproductdisplay.html", product=result)


@app.route("/display-vegetables", methods=['GET', 'POST'])
def vegetables():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCT WHERE category='Vegetables'")
    result = cursor.fetchall()
    return render_template("/userproductdisplay.html", product=result)


@app.route("/display-nonveg", methods=['GET', 'POST'])
def nonveg():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCT WHERE category='Nonveg'")
    result = cursor.fetchall()
    return render_template("/userproductdisplay.html", product=result)

@app.route('/payment')
def home():
    return render_template('payment.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/pay', methods=['POST', 'GET'])
def pay():
    if request.method == 'POST':
        name = request.form.get('name')
        product = request.form.get('product')
        email = request.form.get('email')
        amount = request.form.get('amount')

        response = api.payment_request_create(
            amount=amount,
            purpose=product,
            buyer_name=name,
            send_email=True,
            email=email,
            redirect_url="http://localhost:5000/success"
        )

        return redirect(response['payment_request']['longurl'])

    else:

        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
