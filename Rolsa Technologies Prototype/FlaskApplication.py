from flask import Flask, render_template, request, redirect, session
import sqlite3
import hashlib

conn = sqlite3.connect("Technology Database.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS ProductTBL(
               ProductID INTEGER PRIMARY KEY NOT NULL,
               ProductName STRING NOT NULL,
               ProductDesc STRING NOT NULL,
               ProductPrice FLOAT NOT NULL,
               ProductImage STRING NOT NULL
)
'''
)
cursor.execute('''CREATE TABLE IF NOT EXISTS BookingTBL(
               BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
               BookingType STRING NOT NULL,
               ProductName STRING NOT NULL,
               ProductPrice FLOAT NOT NULL,
               BookingDate DATE NOT NULL,
               BookingAddress STRING NOT NULL,
               Email STRING NOT NULL,
               FOREIGN KEY (ProductPrice) REFERENCES ProductTBL (ProductPrice),
               FOREIGN KEY (ProductName) REFERENCES ProductTBL (ProductName),
               FOREIGN KEY (Email) REFERENCES AccountTBL (Email)
)
'''
)
cursor.execute('''CREATE TABLE IF NOT EXISTS AccountTBL(
               UserID INTEGER PRIMARY KEY AUTOINCREMENT,
               Email STRING NOT NULL,
               Username STRING NOT NULL,
               Password STRING NOT NULL
)
'''
)

many_products = {
        (0, "Solar Panel", "A Solar Panel", 499.99, "https://energyeducation.ca/wiki/images/thumb/2/2c/Fixed_Tilt_Solar_panel_at_Canterbury_Municipal_Building_Canterbury_New_Hampshire.jpg/1200px-Fixed_Tilt_Solar_panel_at_Canterbury_Municipal_Building_Canterbury_New_Hampshire.jpg"),
        (1, "Electric Vehicle Charging Station", "An Electric Vehicle Charging Station", 750, "https://www.dot.nm.gov/wp-content/uploads/2022/05/Charging-Stations.jpg"),
        (2, "Smart Home Energy Managment System", "A Smart Home Energy Management System", 150, "https://denso-x.com/wp-content/uploads/2022/07/shutterstock_1333935968-scaled.jpg"),
    }
#cursor.executemany('INSERT INTO ProductTBL (ProductID, ProductName, ProductDesc, ProductPrice, ProductImage) VALUES (?,?,?,?,?)', many_products)

cursor.execute('''SELECT * FROM ProductTBL''')
products = cursor.fetchall()

conn.commit()
conn.close()

consultationPrice = "49.99"


def hashPassword(password):
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hashedPassword = hash_object.hexdigest()
    return hashedPassword

def checkUsername(username, password):
    hashedPassword = hashPassword(password)
    conn = sqlite3.connect("Technology Database.db")
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM AccountTBL WHERE Username == "{username}"''')
    checkedUser = cursor.fetchone()
    conn.close()
    if checkedUser is None:
        return False
    else:
        if hashedPassword == checkedUser[3]:
            return True
        else:
            return False
        
def checkEmail(email, password):
    hashedPassword = hashPassword(password)
    conn = sqlite3.connect("Technology Database.db")
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM AccountTBL WHERE Email == "{email}"''')
    checkedUser = cursor.fetchone()
    conn.close()
    if checkedUser is None:
        return False
    else:
        if hashedPassword == checkedUser[3]:
            return True
        else:
            return False


def addAccount(email, username, password):
    hashedPassword = hashPassword(password)
    conn = sqlite3.connect("Technology Database.db")
    cursor = conn.cursor()
    EnergyTrackingDate = ("01/25", "02/25", "03/25")
    EnergyTrackingUsage = (572, 536, 632)
    cursor.execute('INSERT INTO AccountTBL (Email, Username, Password) VALUES (?,?,?)', (email, username, hashedPassword))
    conn.commit()
    conn.close()

def getAccountByUsername(username):
    conn = sqlite3.connect("Technology Database.db")
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM AccountTBL WHERE Username == "{username}"''')
    account = cursor.fetchone()
    conn.close()
    return account

def getUsername(email):
    conn = sqlite3.connect("Technology Database.db")
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM AccountTBL WHERE Email == "{email}"''')
    account = cursor.fetchone()
    username = account[2]
    conn.close()
    return username

def getEmail(username):
    conn = sqlite3.connect("Technology Database.db")
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM AccountTBL WHERE Username == "{username}"''')
    account = cursor.fetchone()
    username = account[1]
    conn.close()
    return username

def getProduct(productName):
    conn = sqlite3.connect("Technology Database.db")
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM ProductTBL WHERE ProductName == "{productName}"''')
    product = cursor.fetchone()
    conn.close()
    return product

def addBooking(bookingType, bookingProduct, bookingDate, bookingAddress):
    email = getEmail(session['username'])
    product = getProduct(bookingProduct)
    conn = sqlite3.connect("Technology Database.db")
    cursor = conn.cursor()
    if bookingType == "Consultation":
        price = "50"
    else:
        price = product[3]
    cursor.execute('INSERT INTO BookingTBL (BookingType, ProductName, ProductPrice, BookingDate, BookingAddress, Email) VALUES (?,?,?,?,?,?)', (bookingType, bookingProduct, price, bookingDate, bookingAddress, email))
    conn.commit()
    conn.close()

def getBooking(username):
    email = getEmail(username)
    conn = sqlite3.connect("Technology Database.db")
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM BookingTBL WHERE Email == "{email}"''')
    product = cursor.fetchall()
    conn.close()
    return product

def getBookingPrice(bookingProduct):
    conn = sqlite3.connect("Technology Database.db")
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM ProductTBL WHERE ProductName == "{bookingProduct}"''')
    product = cursor.fetchone()
    price = product[3]
    conn.close()
    return price

def changePassword(prevPassword, newPassword):
    conn = sqlite3.connect("Technology Database.db")
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM AccountTBL WHERE Username == "{session['username']}"''')
    account = cursor.fetchone()
    currentPassword = account[3]
    prevPassword = hashPassword(prevPassword)
    newPassword = hashPassword(newPassword)
    if prevPassword == currentPassword:
        cursor.execute(f'''UPDATE AccountTBL SET Password="{newPassword}" WHERE Username = "{session['username']}"''')
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

def checkUsernameExists(username):
    conn = sqlite3.connect("Technology Database.db")
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM AccountTBL WHERE Username == "{username}"''')
    account = cursor.fetchone()
    conn.close()
    if account == None:
        return False
    else: 
        return True

def checkEmailExists(email):
    conn = sqlite3.connect("Technology Database.db")
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM AccountTBL WHERE Email == "{email}"''')
    account = cursor.fetchone()
    conn.close()
    if account == None:
        return False
    else: 
        return True

def cancelBooking(bookingID):
    email = getEmail(session['username'])
    conn = sqlite3.connect("Technology Database.db")
    cursor = conn.cursor()
    cursor.execute(f'''SELECT * FROM BookingTBL WHERE BookingID == "{bookingID}"''')
    booking = cursor.fetchone()
    if booking == None:
        conn.close()
        return False
    elif booking[6] == email:
        cursor.execute(f'''DELETE FROM BookingTBL WHERE BookingID == "{bookingID}"''')
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/')
def renderHomePage():
        return render_template('Homepage.html', products = products, length = len(products))

@app.route('/CarbonFootprint')
def renderCarbonPage():
    return render_template('Carbonfootprint.html')

@app.route('/EnergyUsage')
def renderEnergyPage():
    return render_template('Energyusage.html')

@app.route('/Order', methods=['POST','GET'])
def renderOrderPage():
    if request.method == 'POST':
        bookingDate = request.form['date']
        bookingAddress = request.form['address']
        addBooking(session['bookingType'], session['bookingProduct'], bookingDate, bookingAddress)
        return redirect("/PaymentComplete")
    if session['bookingType'] == 'Consultation':
        price = consultationPrice
    else:
        price = getBookingPrice(session['bookingProduct'])
    return render_template('Paymentpage.html', product = session['bookingProduct'], type = session['bookingType'], price = price)

@app.route('/Booking', methods=['POST','GET'])
def renderBookingPage():
    if request.method == 'POST':
        bookingType = request.form['option']
        bookingProduct = request.form['products']
        session['bookingType'] = bookingType
        session['bookingProduct'] = bookingProduct
        return redirect("/Order")
    else:
        if session.get('Logged_In'):
            return render_template('Bookingpage.html', products = products, length = len(products))
        else:
            return redirect("/Account")

@app.route('/Account')
def renderAccountPage():
    if session.get("Logged_In"):
        account = getAccountByUsername(session['username'])
        if account is None:
            return render_template('Accountpage.html', loggedIn = True)
        else:
            return render_template('Accountpage.html', loggedIn = True, username = session['username'], email = account[1], bookings = getBooking(session['username']))
    else:
        return redirect('/Login')

@app.route('/Login', methods=['POST', 'GET'])
def renderLoginPage():
    if request.method == 'POST':
        isEmail = False
        username = request.form['username']
        password = request.form['password']
        for i in range(0, len(username)):
            if username[i] == "@":
                isEmail = True
        if (isEmail):
            email = username
            if (checkEmail(email, password)):
                session["Logged_In"] = True
                session["username"] = getUsername(email)
                return redirect('/Account')
            else:
                return render_template('Login.html', loggedIn = False)
        else:
            if (checkUsername(username, password)):
                session["Logged_In"] = True
                session["username"] = username
                return redirect('/Account')
            else:
                return render_template('Login.html', loggedIn = False)
    else:
        return render_template('Login.html')

@app.route('/Signup', methods=['POST', 'GET'])
def renderSignupPage():
    if request.method == 'POST':
        usernameExists = False
        emailExists = False
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        if (checkUsernameExists(username)):
            usernameExists = True
        elif (checkEmailExists(email)):
            emailExists = True
        else:
            addAccount(email, username, password)
            return redirect("/Login")
        return render_template('Signup.html', usernameExists = usernameExists, emailExists = emailExists)
    else:
        return render_template('Signup.html')

@app.route("/Logout")
def logout():
    session["Logged_In"] = None
    session['username'] = None
    session['bookingType'] = None
    session['bookingProduct'] = None
    return redirect("/Login")

@app.route("/PaymentComplete")
def paymentCompletePage():
    return render_template("PaymentComplete.html")

@app.route("/ChangePassword", methods=['POST', 'GET'])
def changePasswordPage():
    if request.method == 'POST':
        prevPassword = request.form['prevPassword']
        newPassword = request.form['password']
        if (changePassword(prevPassword, newPassword)):
            return redirect("/Login")
        else:
            account = getAccountByUsername(session['username'])
            return render_template('Accountpage.html', loggedIn = True, username = session['username'], email = account[1], bookings = getBooking(session['username']), changepass = False)

@app.route("/CancelBooking", methods=['POST', 'GET'])
def cancelBookingPage():
    if request.method == 'POST':
        account = getAccountByUsername(session['username'])
        bookingID = request.form['cancelBookingID']
        cancelled = cancelBooking(bookingID)
        if (cancelled):
            return render_template('Accountpage.html', loggedIn = True, username = session['username'], email = account[1], bookings = getBooking(session['username']), bookingCancelled = True)
        else:
            return render_template('Accountpage.html', loggedIn = True, username = session['username'], email = account[1], bookings = getBooking(session['username']), incorrectID = True)


app.debug = True
app.run()
