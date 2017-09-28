'''
This file contains all the logic, routes and functonality of the app
'''
from flask import Blueprint, redirect, render_template, url_for, flash
from flask import current_app, request, session
from flask_login import login_user

from models import ShoppingList
from forms import LoginForm, SignUpForm
from users import User
site = Blueprint('site', __name__)



@site.route('/')
def home_page():
    '''list every item on the dictonary'''

    name = session.get('user')

    
    shop_lists = current_app.store.get_all_slist()
    return render_template('home.html', shop_lists=sorted(shop_lists.items()))

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

        if request.method == 'GET':
            form = {'title': ''}

        else:
            # validate the data in the forms
            valid = validate_data(request.form)

            if valid:
                title = request.form.data['title']
                # assign a variable to class instance
                slist = ShoppingList(title)
                # add the instance to the dictonary
                current_app.store.add_slist(slist)

                return redirect(url_for('site.product_page', slist_id=slist.id))

            form = request.form
        return render_template('add_shopping_list.html', form=form)
    else:
        flash('please sign in first to add list')
    return redirect(url_for('site.login_page'))

@site.route('/app/<int:slist_id>/edit', methods=['GET', 'POST'])
# @login_required
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

@site.route('/signup', methods=['GET', 'POST'])
def create_account():
    """
    GET request displays sign-up form. POST request registers the current user
    """
    form = SignUpForm(request.form)

    if form.validate_on_submit():
        user = User(form.username.data, form.password.data)

        user.create_accounts(form.username.data, form.password.data)
        session['user'] = form.username.data

        return redirect(url_for('site.login_page'))
    return render_template('sign-up.html', form=form)

@site.route('/login', methods=['GET', 'POST'])
def login_page():
    '''
    This method will be responsible for handling the user loginfunction
    '''
    form = LoginForm(request.form)

    if form.validate_on_submit():

        user = str(form.username.data)
        pas = str(form.password.data)
        add_ = User()

        if user in add_.accounts_db:
            add_.verify_password(user, pas)
            login_user(user)

            flash('You have logged in.')

        next_page = request.args.get('next', url_for('site.home_page'))

        return redirect(next_page)

    flash('Invalid credentials.')

    return render_template('sign-in.html', form=form)

@site.route('/logout')
def logout_page():
    '''
    This method will handle the the user log 
    out funtionality
    '''

    #logout_user(user)

    flash('You have logged out.')

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
