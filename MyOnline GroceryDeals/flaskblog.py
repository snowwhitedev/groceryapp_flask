from flask import Flask, render_template, url_for, request
from flask import flash, redirect, session
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import mysql.connector
from ProductTable import ProductTable
from ProductManagment import matching,Sort


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="rof11223344",  # don't forget to change it
    database="GroceryDeals"

)
#----------------------------------------------------->>>MySQL connection
app = Flask(__name__)

class RegisterForm(Form):
    email = StringField('البريد الإلكتروني', [
        validators.DataRequired(),
        validators.Length(min=6, max=50)
    ])
    password = PasswordField('إنشاء كلمة المرور', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('تأكيد كلمة المرور',[
        validators.DataRequired()
    ])
#----------------------------------------------------->>>class
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
#----------------------------------------------------->>>method

@app.route("/", methods=['GET', 'POST'])
def HomePage():
    if request.method == 'GET':
        productsList = ProductTable.get_all_product()
        return render_template('HomePage.html', productsList=productsList)
    else:
        id = request.form['product']
        similarProduct = matching(id)
        orderProduct = Sort(similarProduct)
        return render_template('ProductDetails.html', title='تفاصيل المنتجات', orderProduct=orderProduct)
#----------------------------------------------------->>>page
@app.route("/wishlist")
def WishList():
    return render_template('WishList.html', title='المفضلة')

#----------------------------------------------------->>>page
@app.route("/admin", methods=['GET', 'POST'])
def admin():
    return render_template('AdminPage.html')
#----------------------------------------------------->>>page
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        # Create cursor
        cur = mydb.cursor()
        # Execute query
        cur.execute("INSERT INTO coustmer(email, password) VALUES(%s, %s)", (email, password))
        # Commit to DB
        mydb.commit()
        # Close connection
        cur.close()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('Registration.html',title='تسجيل جديد', form=form)
#----------------------------------------------------->>>page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']

        # Create cursor
        cur = mydb.cursor(buffered=True)

        # Get user by username
        result = cur.execute("SELECT * FROM coustmer WHERE email = %s", [email])

        if result != 0:
            # Get stored hash
            data = cur.fetchone()
            password = data[2]
            id = data[0]
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['email'] = email
                flash('You are now logged in', 'success')
                # Close connection
                cur.close()
                return render_template('HomePage.html')
            else:
                error = 'Invalid login'
                # Close connection
                cur.close()
                return render_template('Login.html',title='تسجيل دخول', error=error)
        else:
            error = 'Username not found'
            # Close connection
            cur.close()
            return render_template('Login.html',title='تسجيل دخول', error=error)
    return render_template('Login.html',title='تسجيل دخول')
#----------------------------------------------------->>>page
@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return render_template('HomePage.html')
#----------------------------------------------------->>>page
#@app.route("/", methods=['GET', 'POST'])
#def ProuductDetails():
  #  if request.method == 'GET':
       # id = request.form['product']
        #similarProduct = matching(id)
        #return render_template('ProductDetails.html', title='تفاصيل المنتجات', similarProduct=similarProduct)
    #else:
       #idp = request.form['product']

         # Execute query
       #idc= CoustmerTable.get_Coustmer_id(email)


    #mycursor = mydb.cursor()

    #mycursor.execute("INSERT INTO wishlist_prouduct(idc, idp) VALUES(%s, %s)", (idc, idp))
    # Commit to DB
    #mydb.commit()
    # Close connection
    #mycursor.close()

if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)
