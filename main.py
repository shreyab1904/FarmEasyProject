import flask
from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
import os.path
from instamojo_wrapper import Instamojo
from datetime import date

API_KEY = "test_ae0ed2ba0300671b76829da7965"
AUTH_TOKEN = "test_4da4849c457db419475e7b97b4c"
api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')
import sqlite3

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['UPLOAD_FOLDER'] = "static/uploads"

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()
listOfTables = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='USER'").fetchall()
listOfTables1 = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='PRODUCT'").fetchall()
listofTables2 = conn.execute("select * from sqlite_master where type = 'table' and name = 'CART'").fetchall()
listofTables3 = conn.execute("select * from sqlite_master where type = 'table' and name = 'ORDERS'").fetchall()

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
                        productid TEXT, bname TEXT, pname TEXT, category TEXT, image TEXT,
                        price INT); ''')
print("Table Product has created")

if listofTables2 !=[]:
    print("Table already exists")
else:
    conn.execute('''create table CART(
                                user_id TEXT,
                                product_id INT,
                                date TEXT);''')
print("Table Cart has created")

if listofTables3 !=[]:
    print("Table already exists")
else:
    conn.execute(''' CREATE TABLE ORDERS(
                                user_id TEXT,
                                product_id INT,
                                date TEXT);''')
print("Table ORDER has created")

@app.route("/")
def homepage():
    return render_template("/homepage.html")

@app.route("/dashboard", methods = ['GET','POST'])
def dashboard():
    if not session.get("name"):
        return redirect("/userlogin")
    else:
        return render_template("/dashboard.html")

@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    global userid
    if request.method == 'POST':
        getemail = request.form['email']
        getpass = request.form['pass']
        print(getemail)
        print(getpass)
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
            userid = str(session["id"])
            return redirect("/dashboard")
        else:
            return redirect("userlogin")
    else:
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

@app.route("/editprofile")
def editprofile():
    cursor.execute("SELECT * FROM USER where ID="+str(session['id']))
    result = cursor.fetchall()
    return render_template("updateuser.html", user=result)

@app.route("/updateuser", methods=['GET', 'POST'])
def updateprofile():
    if request.method == "POST":
        try:
            getfirstname = request.form['firstname']
            print(getfirstname)
            getlastname = request.form['lastname']
            print(getlastname)
            getDOB = request.form['DOB']
            print(getDOB)
            getemail = request.form['email']
            print(getemail)
            getphone = request.form['phone']
            print(getphone)
            getpass = request.form['pass']
            print(getpass)
            getcnfpass = request.form['cnfpass']
            print(getcnfpass)
            conn.execute("UPDATE USER SET firstname = '"+getfirstname+"',lastname = '"+getlastname+"',DOB = '"+getDOB+"',email = '"+getemail+"',phone = '"+getphone+"',password = '"+getpass+"',confirmpassword = '"+getcnfpass+"' WHERE ID="+str(session['id']))
            conn.commit()
            return redirect("/dashboard")
        except Exception as e:
            print(e)
    return render_template("/updateuser.html")

@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        getname = request.form["name"]
        getpass = request.form["pass"]
    try:
        if getname == 'admin' and getpass == "12345":
            return redirect("/productmanagement")
        else:
            print("Invalid username and password")
    except Exception as e:
        print(e)
    return render_template("/adminlogin.html")


@app.route("/productmanagement")
def adminproductmanagement():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCT")
    result = cursor.fetchall()
    return render_template("/adminproductmanagement.html", product=result)

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
        if getimage!= '':
           filepath = os.path.join(app.config['UPLOAD_FOLDER'],getimage.filename)
           getimage.save(filepath)
        query = "INSERT INTO PRODUCT(productid, bname, pname, category, image, price)VALUES(?, ?, ?, ?, ?, ?)"
        data = (getpid, getbname, getpname, getcategory, getimage.filename, getprice)
        cursor.execute(query, data)
        conn.commit()
        print("SUCCESSFULLY ADDED!")
    except Exception as e:
        print(e)

    return render_template("/adminproductentry.html")
    
@app.route("/productdisplay", methods=['GET', 'POST'])
def userproductdisplay():
    cursor = conn.cursor()
    query = cursor.execute("SELECT * FROM PRODUCT")
    result = cursor.fetchall()
    return render_template("/userproductdisplay.html", product=result)


@app.route('/delete/<getpid>/', methods=['GET', 'POST'])
def delete(getpid):
    data = "DELETE FROM PRODUCT WHERE productid='" + getpid + "'"
    cursor.execute(data)
    conn.commit()
    return redirect("/productmanagement")


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

@app.route("/edit")
def edit():
    getid = str(request.args.get('id'))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCT where productid=" + getid)
    result = cursor.fetchall()
    return render_template("update.html", product=result)

@app.route("/update",methods = ["GET","POST"])
def update():
    if request.method == "POST":
        try:
            getpid = request.form['pid']
            print(getpid)
            getbname = request.form['bname']
            print(getbname)
            getpname = request.form['pname']
            print(getpname)
            getcategory = request.form['category']
            print(getcategory)
            getimage = request.files['img']
            print(getimage)
            getprice = request.form['price']
            print(getprice)
            if getimage != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], getimage.filename)
                getimage.save(filepath)
            conn.execute("UPDATE PRODUCT SET productid = '"+getpid+"',bname = '"+getbname+"',pname = '"+getpname+"',category = '"+getcategory+"',image = '"+getimage.filename+"',price = '"+getprice+"' WHERE productid = "+getpid)
            conn.commit()
            return redirect("/productmanagement")
        except Exception as e:
            print(e)
    return render_template("update.html")

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
    query = "SELECT PRODUCT.productid, PRODUCT.pname, PRODUCT.bname, PRODUCT.price, PRODUCT.image FROM PRODUCT, CART WHERE PRODUCT.productid = CART.product_id AND CART.user_id ='"+str(session['id'])+"'"
    print(query)
    cursor.execute(query)
    print("Added!")
    result = cursor.fetchall()
    print(result)
    totalprice = 0
    for row in result:
        totalprice += row[3]
    return render_template('/payment.html', totalprice = totalprice)

@app.route('/success')
def success():
    getdate = str(date.today())
    query = "INSERT INTO ORDERS SELECT * FROM CART"
    cursor.execute(query)
    conn.commit()
    query1 = "DELETE FROM CART WHERE user_id = '"+str(session['id'])+"'"
    cursor.execute(query1)
    conn.commit()
    return render_template('success.html')

@app.route('/pay', methods=['POST', 'GET'])
def pay():
    if not session.get("name"):
        return redirect("/userlogin")
    else:    
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

@app.route("/userlogout", methods=["GET", "POST"])
def userlogout():

    if not session.get("name"):
        return redirect("/userlogin")
    else:
        session["name"] = None
        return redirect("/")

@app.route("/addtocart", methods = ['GET','POST'])
def addtocart():
    if not session.get("name"):
        return redirect("/userlogin")
    else:
        getdate = str(date.today())
        product_id = request.args.get('productid')
        try:
            cursor.execute("INSERT INTO CART(product_id,user_id,date)values("+product_id+",'"+str(session['id'])+"','"+getdate+"')")
            conn.commit()
            print("PRODUCT ADDED!")

        except Exception as e:
            print(e)
    return redirect(url_for('userproductdisplay'))

@app.route("/cart")
def cart():
    if not session.get("name"):
        return redirect("/userlogin")
    else:
        query = "SELECT PRODUCT.productid, PRODUCT.pname, PRODUCT.bname, PRODUCT.price, PRODUCT.image FROM PRODUCT, CART WHERE PRODUCT.productid = CART.product_id AND CART.user_id ='"+str(session['id'])+"'"
        print(query)
        cursor.execute(query)
        print("Added!")
        result = cursor.fetchall()
        print(result)
        totalprice = 0
        for row in result:
            totalprice += row[3]
    return render_template("/cart.html", product = result, totalprice = totalprice)

@app.route('/remove/<getpid>/', methods=['GET', 'POST'])
def remove(getpid):
    data = "DELETE FROM CART WHERE product_id='" + getpid + "'"
    cursor.execute(data)
    conn.commit()
    return redirect("/cart")

@app.route("/order")
def order():
    if not session.get("name"):
        return redirect("/userlogin")
    else:
        try:
            query = "SELECT PRODUCT.productid, PRODUCT.pname, PRODUCT.bname, PRODUCT.price, PRODUCT.image, ORDERS.date FROM PRODUCT JOIN ORDERS on ORDERS.product_id = PRODUCT.productid WHERE ORDERS.user_id ='"+str(session['id'])+"'"
            print(query)
            cursor.execute(query)
            print("Order Added!")
            result = cursor.fetchall()
            print(result)
            return render_template("/order.html",product=result,status=True)
        except Exception as e:
            print(e)
    return render_template("/order.html",product=[],status=False)

@app.route("/orderstatus")
def orderstatus():
    try:
        query = "SELECT ORDERS.date, PRODUCT.pname, PRODUCT.bname, PRODUCT.image, PRODUCT.price FROM PRODUCT JOIN ORDERS on ORDERS.product_id = PRODUCT.productid WHERE ORDERS.user_id = '"+str(session['id'])+"'"
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        return render_template("/orderstatus.html", product = result)
    except Exception as e:
        print(e)
    return render_template("/orderstatus.html", product =[])

@app.route("/adminorder")
def adminorder():
    query = "SELECT USER.firstname, USER.lastname, USER.email, ORDERS.date, PRODUCT.pname, PRODUCT.price FROM USER JOIN ORDERS ON USER.ID = ORDERS.user_id JOIN PRODUCT ON ORDERS.product_id = PRODUCT.productid ORDER BY ORDERS.date DESC"
    print(query)
    cursor.execute(query)
    result= cursor.fetchall()
    print(result)
    return render_template("/adminorder.html", product = result)

if __name__ == "__main__":
    app.run(debug=True)
