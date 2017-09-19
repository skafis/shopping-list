from flask import Flask
from flask import (
    render_template,
    redirect,
    session,
    request,
    url_for,
    flash)
from flask.ext.login import LoginManager
from flask.ext.login import (
    login_user,
    logout_user, 
    current_user, 
    login_required)

from models import User




app = Flask(__name__)
app.secret_key = 'asdfzxcvqwer'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)


@app.route('/sign-up', methods=['POST','GET'])
def create_account():
    print(User.email_index.keys())
    user_name = None
    email = None
    user_password = None
    error = None

    """
    GET request displays sign-up form. 
    POST request registers the current user
    """

    # if request.method == 'GET':
    #     return render_template('sign-up.html')
    # user = User(request.form['username'] , request.form['password'],request.form['email'])
    # # session[username] = request.form['username']
    # # session.commit()
    # flash('User successfully registered')
    # return redirect(url_for('login'))
    if request.method == "POST":
        user_name = request.form['username']
        user_password = request.form['password']
        email = request.form['email']

        if email in User.email_index:
            flash('User with the email already exists')
            return render_template('sign-up.html', error=error)
        else:
            user = User(user_name, user_password, email)
            k = User.email_index[email] = user_name
            print(k)
            # redirect to the login page
            return redirect(url_for('login'))
    else:
        return render_template('sign-up.html', error=error)



@app.route('/login', methods=['POST', 'GET'])
def login():
    email = None
    password = None
    error = None

    """For GET requests, display the login form. For POSTS, login the current user
        by processing the form."""
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        try:
            user = User.find_by_email(email)
            print user
            if user.check_password(user.user_password, password):
                user.authenticated = True

                # Login and validate the user.
                # user should be an instance of your `User` class
                login_user(user, remember=True)

                # redirect to the home page
                return redirect(url_for('index'))
            else:
                error = 'You have entered invalid credentials'
                return render_template('sign-in.html', error=error)

        except:
            error = 'The email does not exist'
            return render_template('sign-in.html', error=error)

    return render_template('sign-in.html', error=error)

@app.route('/logout')
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    logout_user()
    return render_template("logout.html")
    
if __name__ =='__main__':
    app.run( debug=True)