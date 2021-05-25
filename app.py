from flask import Flask, render_template, session, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'bteKwsa7YT'
app.config['MYSQL_PASSWORD'] = 'heSLzH0fvV'
app.config['MYSQL_DB'] = 'bteKwsa7YT'

app.secret_key = 'a'


@app.route('/')
def home():
    if not session.get('loggedin'):
        return render_template('signup.html')
    else:
        cursor = mysql.connection.cursor()
        res = cursor.execute("SELECT * FROM suppliers WHERE user = %s ORDER BY supname", (session['username'], ))
        data = cursor.fetchall()
        cursor.close()
        return render_template('supplier.html', msg = msg)
 
 
#Edit supplier
@app.route('/edit_supplier/<string:supid>', methods = ['GET', 'POST'])
def edit_sup(supid):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM suppliers WHERE supid = %s", (supid, ))
    info = cursor.fetchone()
    cursor.close()
    
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        
        cursor.execute("UPDATE suppliers SET supname = %s, contact = %s, address = %s WHERE supid = %s", (name, contact, address, supid))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('home'))
    
    return render_template('edit_suppliers.html', a = info[2], b = info[3], c = info[4])

#Delete supplier
@app.route('/delete_supplier/<string:supid>', methods = ['POST'])
def delete_sup(supid):
    cursor.execute("DELETE FROM suppliers WHERE supid = %s", (supid, ))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('home'))

#Add supplier
@app.route('/add_supplier', methods = ['POST', 'GET'])
def add_sup():
    if request.method == 'POST':
        name = request.form['name']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO suppliers(user, supname, contact, address) VALUES(%s, %s, %s, %s)", (session['username'], name, contact, address))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('home'))
    
    return render_template('add_supplier.html')
        
        
@app.route('/inventory')
def inventory():
    cursor = mysql.connection.cursor()
    res = cursor.execute("SELECT * FROM inventory WHERE user = %s ORDER BY prodname", (session['username'], ))
    data = cursor.fetchall()
    total1 = cursor.execute("SELECT * FROM inventory WHERE user = %s", (session['username'], ))
    total2 = 0
    cursor.execute("SELECT quantity FROM inventory WHERE user = %s", (session['username'], ))
    q1 = []
    sp1 = []
    for i in q:
        q1.append(i[0])
    for i in sp:
        sp1.append(i[0])
    print(q1)
    print(sp1)
    for i in  range(len(q1)):
        total2 += (q1[i] * sp1[i])
    print(total2)
    cursor.close()
    
    if res > 0:
        return render_template('inventory.html', data = data, total1 = total1, total2 = total2)
    else:
        msg = "No stock found."
        return render_template('inventory.html', msg = msg, total1 = total1, total2 = total2)

#Add product
@app.route('/add_product', methods = ['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        measure = request.form['measurement']
        supplier = request.form['supplier']
        sp = int(cp) + int(profit)
        
        cursor.execute("INSERT INTO transactions1(user, supplier, product, quantity, measurement, price) VALUES(%s, %s, %s, %s, %s, %s)", (session['username'], supplier, name, quantity, measure, cp))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('inventory'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT supname FROM suppliers WHERE user = %s", (session['username'], ))
    sup = cursor.fetchall()
    cursor.close()
        
    return render_template('add_product.html', sup = sup)

#Edit product
@app.route('/edit_products/<string:prodid>', methods = ['POST', 'GET'])
def edit_product(prodid):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM inventory WHERE prodid = %s", (prodid, ))
    info = cursor.fetchone()
    cursor.close()
    
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        measure = request.form['measurement']
        cp = request.form['cprice']
        profit = request.form['profit']
        
        return redirect(url_for('inventory'))
    
    cursor.execute("SELECT supname FROM suppliers WHERE user = %s", (session['username'], ))
    sup = cursor.fetchall()
    cursor.close()
    
    return render_template('edit_product.html', a = info[2], b = info[3], c = info[5], d = info[7], sup = sup)

#Delete product
@app.route('/delete_product/<string:prodid>', methods = ['POST'])
def delete_prod(prodid):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM inventory WHERE prodid = %s", (prodid, ))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('inventory'))

@app.route('/checkout')
def checkout():
    cursor = mysql.connection.cursor()
    res1 = cursor.execute("SELECT * FROM inventory WHERE user = %s ORDER BY prodname", (session['username'], ))
    proddata = cursor.fetchall()
    res2 = cursor.execute("SELECT * FROM cart WHERE user = %s", (session['username'], ))
    cartdata = cursor.fetchall()
    cursor.close()
    
    change = request.args.get("ch", 0)
    tender = request.args.get("tend", 0)
    
    sale = 0
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT price FROM cart WHERE user = %s", (session['username'], ))
    s = cursor.fetchall()
    
    sale = sum(salelist)
    
    if res1 > 0 and res2 > 0:
        return render_template('checkout.html', proddata = proddata, cartdata = cartdata, items = res2, sale = sale, ch = change, tend = tender)
    elif res1 > 0 and res2 <= 0:
        cartmsg = "No items in the cart."
        return render_template('checkout.html', proddata = proddata, cartmsg = cartmsg, items = res2, ch = change, tend = tender)
    elif res2 > 0 and res1 <= 0:
        prodmsg = "No products found."
        return render_template('checkout.html', prodmsg = prodmsg, items = res2, sale = sale, ch = change, tend = tender)
    else:
        cartmsg = "No items in the cart."
        prodmsg = "No products found."
        return render_template('checkout.html', cartmsg = cartmsg, prodmsg = prodmsg, items = res2, ch = change, tend = tender)

#tender
@app.route('/tender/<string:total>', methods = ['POST', 'GET'])
def tender(total):
    c = 0
    if request.method == 'POST':
        t = request.form['tender']
        c = int(t) - int(total)
    return redirect(url_for('checkout', ch = c, tend = t))

#Add to cart
@app.route('/add_to_cart/<string:prodid>', methods = ['GET', 'POST'])
def add_to_cart(prodid):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM inventory WHERE prodid = %s", (prodid, ))
    info = cursor.fetchone()
    cursor.close()
    
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['req_quantity']
        if int(quantity) > info[3]:
            qmsg = "Value for quantity exceeded the limit!"
            return render_template('add_to_cart.html', a = info[2], b = info[3], c = info[4], d = info[6], e = info[8], qmsg = qmsg)
        measurement = request.form['measurement']
        customer = request.form['cust']
        price = int(quantity) * int(info[6])
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO cart(user, custname, prodname, quantity, measurement, price) VALUES(%s, %s, %s, %s, %s, %s)", (session['username'], customer, name, quantity, measurement, price))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('checkout'))
    
    return render_template('add_to_cart.html', a = info[2], b = info[3], c = info[4], d = info[6], e = info[8])

#Delete product from cart
@app.route('/delete_cart_product/<string:cartid>', methods = ['POST'])
def delete_cart_product(cartid):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM cart WHERE cartid = %s", (cartid, ))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('checkout'))   

#Checkout button
@app.route('/cart_checkout', methods = ['POST', 'GET'])     
def cart_checkout():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        count = cursor.execute("SELECT * FROM cart WHERE user = %s", (session['username'], ))
        cart = cursor.fetchall();
        
        print("The cart:")
        print(cart)
        
        for i in range(count):
            cursor.execute("SELECT quantity FROM inventory WHERE prodname = %s AND user = %s", (cart[i][3], session['username']))
            q = cursor.fetchone()
            print("Available quantity: ", q)
            resq = q[0] - cart[i][4]
            print("Remaining:", resq)
            cursor.execute("INSERT INTO transactions(user, custname, prodname, quantity, measurement, price) VALUES(%s, %s, %s, %s, %s, %s)", (session['username'], cart[i][2], cart[i][3], cart[i][4], cart[i][5], cart[i][6]))
            mysql.connection.commit()
            
            #Send mail if resq == 0
            if resq <= 0:
                prod = cart[i][3]
                sgemail = Mail(from_email = "tempsonika@gmail.com",
                               to_emails = session['email'],
                               subject = "Alert! Out of Stock",
                               plain_text_content = f"Dear {session['username']}, " + "\n\n" + f"You are receiving this mail as the item {prod} is out of stock! Please order new stock soon." + "\n\n\n" + "Thank you" + "\n" + "Inventory Management System")
                
                try:
                    sg = SendGridAPIClient(sgAPI)
                    response = sg.send(sgemail)
                    print(response.status_code)
                except Exception as e:
                    print(e)
            
        cursor.execute("DELETE FROM cart WHERE user = %s", (session['username'], ))
        
        return redirect(url_for('checkout'))

@app.route('/transactions')
def transactions():
    cursor = mysql.connection.cursor()
    res1 = cursor.execute("SELECT * FROM transactions WHERE user = %s", (session['username'], ))
    data1 = cursor.fetchall()
    res2 = cursor.execute("SELECT * FROM transactions1 WHERE user = %s", (session['username'], ))
    data2 = cursor.fetchall()
    cursor.close()
    
    cashin = cashout = 0
    if res1 > 0:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT price FROM transactions WHERE user = %s", (session['username'], ))
        cin = cursor.fetchall()
        inlist = []
        for i in cin:
            inlist.append(i[0])
        cashin = sum(inlist)
    
    if res1 > 0 or res2 > 0:
        return render_template('transactions.html', data1 = data1, data2 = data2, cashin = cashin, cashout = cashout)
    else:
        msg = "No transaction details found."
        return render_template('transactions.html', msg = msg, cashin = cashin, cashout = cashout)

#Delete all transactions
@app.route('/delete_all_transactions')
def delete_all_transactions():
    cursor.execute("DELETE FROM transactions WHERE user = %s", (session['username'], ))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('transactions'))

#Delete all transactions1
@app.route('/delete_all_transactions1')
def delete_all_transactions1():
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('transactions'))
    
#Delete a transaction
@app.route('/delete_transaction/<string:transid>', methods = ['POST'])
def delete_transaction(transid):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM transactions WHERE transid = %s", (transid, ))
    mysql.connection.commit()
    cursor.close()

#Delete a transaction1
@app.route('/delete_transaction1/<string:transid>', methods = ['POST'])
def delete_transaction1(transid):
    cursor.execute("DELETE FROM transactions1 WHERE transid = %s", (transid, ))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('transactions'))

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM retailers WHERE username = %s', (username, ))
        if account:
            msg = 'Username already exists.'
        else:
            cursor.execute("INSERT INTO retailers VALUE(%s, %s, %s)", (username, email, password))
            mysql.connection.commit()
            msg = 'You have successfully registered! You can login now.'
            
            sgemail = Mail(from_email = "tempsonika@gmail.com",
                           to_emails = email,
                           subject = "Registration sucessful",
                           plain_text_content = f"Hello {username}!" + "\n\n" + "Thank you for registering for the Inventory Management System application." + "\n" + "I hope you will have a great experience here." + "\n\n\n" + "Thank you" + "\n" + "Inventory Management System")
            
            try:
                sg = SendGridAPIClient(sgAPI)
                response = sg.send(sgemail)
                print(response.status_code)
            except Exception as e:
                print(e)
                
        cursor.close()
        
    return render_template('signup.html', msg = msg)

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM retailers WHERE username = %s AND password = %s', (username, password, ))
        account = cursor.fetchone()
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('email', None)
    msg = 'Logged out successfully!'
    print(msg)
    return redirect(url_for('signup'))

 

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080, debug = True)
