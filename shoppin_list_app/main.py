from flask import Flask
from flask import (
    render_template,
    redirect,
    request,
    url_for)
from models import User

app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "hello world"

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
    if request.method == "POST":
        user_name = request.form['user_name']
        email = request.form['email']
        user_password = request.form['user_password']

        if email in User.email_index:
            error = "A user with that email already exist"
            return render_template('sign-up.html', error=error)
        else:
            user = User(user_name, email, user_password)
            return redirect(url_for('login'))
    else:
        return render_template('sign-up.html', error=error)