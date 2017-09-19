from flask import Flask
from flask import (
    render_template,
    redirect,
    session,
    request,
    url_for,
    flash)

from models import User

app = Flask(__name__)
app.secret_key = 'asdfzxcvqwer'

@app.route("/")
def hello_world():
    user = session.get('email')
    print(user)
    return render_template('home.html')

# @app.route('/register' , methods=['GET','POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('register.html')
#     user = User(request.form['username'] , request.form['password'],request.form['email'])
#     print(request.form['username'])
#     # session[username] = request.form['username']
#     # session.commit()
#     flash('User successfully registered')
#     return redirect(url_for('hello_world'))

@app.route('/sign-up', methods=['POST','GET'])
def create_account():
    user_name = None
    email = None
    user_password = None
    error = None

    """
    GET request displays sign-up form. 
    POST request registers the current user
    """

    if request.method == 'GET':
        return render_template('sign-up.html')
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    # session[username] = request.form['username']
    # session.commit()
    flash('User successfully registered')
    return redirect(url_for('hello_world'))


    # if request.method == "POST":
    #     user_name = request.form['user_name']
    #     email = request.form['email']
    #     user_password = request.form['user_password']

    #     if email in User.email_index:
    #         error = "A user with that email already exist"
    #         return render_template('sign-up.html', error=error)
    #     else:

    #         user = User(user_name, email, user_password)
    #         print(user)
    #         return "done"
    #         # return redirect(url_for('hello_world'))
    # else:
    #     return render_template('sign-up.html', error=error)

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     pass

if __name__ =='__main__':
    app.run( debug=True)