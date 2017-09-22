from flask import Flask
from flask import (
    render_template,
    redirect,
    session,
    request,
    url_for,
    flash,
    current_app)
from flask.ext.login import LoginManager
from flask.ext.login import (
    login_user,
    logout_user, 
    current_user, 
    login_required)

from models import User, ShoppingList, Items




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

@app.route('/')
def home():
    user = current_user
    return render_template('home.html', username=user)

@app.route('/sign-up', methods=['POST','GET'])
def create_account():
    print (User)
    # print vars(User)
    user_name = None
    email = None
    user_password = None
    error = None

    """
    GET request displays sign-up form. 
    POST request registers the current user
    """

    if request.method == "POST":
        user_name = request.form['username']
        user_password = request.form['password']
        email = request.form['email']



        if email in User.email_index:
            flash('User with the email already exists')
            return render_template('sign-up.html', error=error)
        else:
            user = User(user_name, user_password, email)
            name = session['username'] = user_name
            password = session['password'] = user_password

            # redirect to the login page
            return redirect(url_for('home'))
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
                return redirect(url_for('home'))
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

@app.route('/add-list', methods=['POST', 'GET'])
# @login_required
def add_shopping_list():
    title = None
    error = None
    user = current_user

    """For GET requests, display the registraion form. For POSTS, register the current user
            by processing the form."""
    if request.method == "POST":
        title = request.form['title']

        try:
            # u = User.find_by_email(user.email)
            # print(u)
            shopping_list = ShoppingList(title)
            shopping_list.add_list(title)
            
            # shopping_list.add_user(u)
            # u.add_shopping_list(shopping_list)
            return redirect(url_for('home'))
        except KeyError:
            error = "No user found"
            return render_template('add_shopping_list.html', error=error)
    else:
        return render_template('add_shopping_list.html', error=error)

@app.route('/update-list', methods=['POST', 'GET'])
@login_required
def update_shopping_list():
    title = None
    description = None
    error = None
    user = current_user
    list_id = request.args.get('id')
    shopping_list = None

    """For GET requests, display the registraion form. For POSTS, register the current user
            by processing the form."""
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        id = request.form['id']
        try:
            u = User.find_by_email(user.email)
            for b in u.shopping_list:
                if b.id == int(id):
                    b.title = title
                    b.description = description
            return redirect(url_for('home'))
        except KeyError:
            error = "No user found"
            return render_template('home.html')
    else:
        u = User.find_by_email(user.email)
        shopping_list = u.shopping_list
        for b in shopping_list:
            if b.id == int(list_id):
                shopping_list = b
        return render_template('update-list.html', shopping_list=shopping_list)

@app.route('/list-delete', methods=['POST', 'GET'])
def delete_shoping_list():
    id = None
    user = current_user

    """For GET requests, display the login form. For POSTS, login the current user
        by processing the form."""
    if request.method == "POST":
        id = request.form['id']
        u = User.find_by_email(user.email)
        try:
            for i, b in enumerate(u.shopping_list):
                if b.id == int(id):
                    del u.shopping_list[i]
                    break
            return redirect(url_for('home'))
        except:
            return render_template('home.html')
    else:
        return render_template('home.html')


@app.route('/add-item', methods=['GET', 'POST'])
# @login_required
def add_item():
    """Display entries list page."""
    title = None
    content = None
    error = None

    """For GET requests, display the registraion form. For POSTS, register the current user
                by processing the form."""
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        list_id = request.form['list_id']
        try:
            shopping_list = ShoppingList.find_by_id(int(list_id))
            item = Items(title, content, int(list_id))
            shopping_list.add_item(item)
            return redirect(url_for('show_items', id=[int(list_id)]))
        except KeyError:
            error = "No list found"
            return render_template('add_items.html', error=error)
    else:
        list_id = request.args.get('id')
        return render_template('add_items.html', list_id=list_id)

@app.route('/items')
@login_required
def show_items():
    items = []
    list_id = request.args.get('id')

    try:
        shopping_list = ShoppingList.find_by_id(int(list_id))
        items = shopping_list.items
    except KeyError:
        items = []

    return render_template('show_items.html', items=items, list_id=list_id)

@app.route('/update-items', methods=['GET', 'POST'])
@login_required
def update_items():
    """Display entries list page."""
    title = None
    content = None
    error = None
    item_id = None
    list_id = None
    item = None

    item_id = request.args.get('item_id')
    list_id = request.args.get('list_id')

    """For GET requests, display the registraion form. For POSTS, register the current user
                by processing the form."""
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        item_id = request.form['item_id']
        list_id = request.form['list_id']
        try:
            shopping_list = ShoppingList.find_by_id(int(list_id))
            items = shopping_list.items

            for e in items:
                if e.id == int(item_id):
                    e.title = title
                    e.content = content
                    break
            shopping_list.items = items

            return redirect(url_for('entry_detail', entry_id=[int(entry_id)], list_id=[int(list_id)]))
        except KeyError:
            error = "No item found"
            return render_template('item-update.html', error=error)
    else:
        shopping_list = ShoppingList.find_by_id(int(list_id))
        items = shopping_list.items
        for e in items:
            if e.id == int(item_id):
                item = e
        return render_template('entry_update.html', item=item)

if __name__ =='__main__':
    app.run( debug=True)