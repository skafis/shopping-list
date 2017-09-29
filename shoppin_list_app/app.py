'''
This file contains all the logic, routes and functonality of the app
'''
from flask import Blueprint, redirect, render_template, url_for, flash
from flask import current_app, request, session

from models import ShoppingList

from forms import LoginForm, SignUpForm
from users import User
site = Blueprint('site', __name__)

user_db = {}

@site.route('/')
def home_page():
    '''list every item on the dictonary'''

    if 'user' not in session:
        flash('you have to login first')
        return redirect(url_for('site.login_page'))

    if 'user' in session:
        name = session.get('user')

    shop_lists = current_app.store.get_all_slist()

    return render_template('home.html', shop_lists=sorted(shop_lists.items()), name=name)

@site.route('/app/<int:slist_id>')
def product_page(slist_id):
    '''
    if request is GET show list detail
    '''
    if request.method == 'GET':

        slist = current_app.store.get_slist(slist_id)

        return render_template('shop_list_detail.html', slist=slist)

    return redirect(url_for('site.product_page'))

# add shopping list method
@site.route('/app/add', methods=['GET', 'POST'])
def slist_add_page():
    '''
    The get method will create a new form

    '''
    if 'user' in session:
        name = session.get('user')

        if request.method == 'GET':
            form = {'title': ''}

        else:
            # validate the data in the forms
            valid = validate_data(request.form)

            if valid:
                title = request.form.data['title']
                # assign a variable to class instance
                slist = ShoppingList(title, name)
                # add the instance to the dictonary
                current_app.store.add_slist(slist)

                flash('new list added')

                return redirect(url_for('site.product_page', slist_id=slist._id))

            form = request.form
        return render_template('add_shopping_list.html', form=form)
    else:
        flash('please sign in first to add list')
        return redirect(url_for('site.create_account'))

@site.route('/app/<int:slist_id>/edit', methods=['GET', 'POST'])

def slist_edit_page(slist_id):
    '''get the id of the list and load it i a form to update it'''

    #fetch the value of the id provided
    slist = current_app.store.get_slist(slist_id)

    if request.method == 'GET':

        # assign the form the current value
        form = {'title': slist.title}
        return render_template('add_shopping_list.html', form=form)

    else:
        # get the value in the form
        slist.title = request.form['title']

        # add the value to the dictonary
        current_app.store.update_slist(slist)

        flash('list  data updated.')

        return redirect(url_for('site.product_page', slist_id=slist._id))

@site.route('/app/<int:slist_id>/del', methods=['GET'])
def slist_delete_page(slist_id):
    '''
    this method will delete a list if passed the ID
    '''

    # delete the value in the dictonary of the id provided
    current_app.store.delete_slist(int(slist_id))

    flash("list deleted")

    return redirect(url_for('site.home_page'))

@site.route('/app/<int:slist_id>/add-list')
def add_items_page(slist_id):

    if 'user' in session:
        name = session.get('user')

        if request.method == 'GET':
            form = {'title': ''}

        else:
            # validate the data in the forms
            valid = validate_data(request.form)

            if valid:
                item = request.form.data['title']
                # assign a variable to class instance
                slist = ShoppingList(item)
                # add the instance to the dictonary
                current_app.store.add_list_item(slist)

                return redirect(url_for('site.product_page', slist_id=slist._id))

            form = request.form
        return render_template('add_item.html', form=form)
    else:
        flash('please sign in first to add list')
    return redirect(url_for('site.login_page'))


@site.route('/signup', methods=['GET', 'POST'])
def create_account():
    """
    GET request displays sign-up form. POST request registers the current user
    """
    if 'user' in session:
        flash('you are already logged in!')
        return redirect(url_for('site.home_page'))

    form = SignUpForm(request.form)

    if form.validate_on_submit():
       
        for user in user_db.keys():
            if user == form.username.data:
                flash(u'a user already exists')
                return redirect(url_for('site.create_account'))


        user_db[form.username.data] = User().create_accounts(form.username.data, form.password.data)

        flash(u'You have logged in succesfully', 'success')
        session['user'] = form.username.data

        return redirect(url_for('site.home_page'))

    return render_template('sign-up.html', form=form)

@site.route('/login', methods=['GET', 'POST'])
def login_page():
    '''
    This method will be responsible for handling the user loginfunction
    '''
    form = LoginForm(request.form)
    if 'user' in session:
        flash(u'you are already logged in!', 'info')
        return redirect(url_for('site.home_page'))

    if request.method == 'POST':
        if not form.validate():
            flash(u'Please check the errors below', 'warning')

        username = form.username.data
        password = form.password.data

        if username not in user_db.values():
            flash('user is not correct')

        for user in user_db.values():
            flash('user is not correct')
            if not user.verify_password(username, password):
                flash('username or password is incorrect', 'warning')
                return redirect(url_for('site.login_page'))

            else:
                flash(u'Success!! you are now logged in', 'success')
                session['user'] = username

                return redirect(url_for('site.home_page'))
    return render_template('sign-in.html', form=form)

@site.route('/logout')
def logout_page():
    '''
    This method will handle the the user log
    out funtionality
    '''
    if 'user' in session:
        session.pop('user')
        return redirect(url_for('site.login_page'))

    return redirect(url_for('site.home_page'))


def validate_data(form):
    '''
    this method validates the inputs for adding
    list
    '''

    form.data = {}

    form.errors = {}

    if len(form['title'].strip()) == 0:
        form.errors['title'] = 'Title can not be blank.'
    else:
        form.data['title'] = form['title']


    return len(form.errors) == 0
