from flask import Blueprint, redirect, render_template, url_for, flash
from flask import current_app, request
from flask_login import LoginManager, login_user
from passlib.apps import custom_app_context as pwd_context


from models import ShoppingList
from forms import LoginForm

from users import get_user

from datetime import datetime


site = Blueprint('site', __name__)


@site.route('/shop')
def product():
    now = datetime.now()
    day = now.strftime('%A')
    return render_template('home.html', day_name=day)


@site.route('/')
def home_page():
    # list every item on the dictonary
    shop_lists = current_app.store.get_all_slist()

    print(shop_lists.items())
    return render_template('home.html', shop_lists=sorted(shop_lists.items()))

@site.route('/shop/<int:slist_id>')
def product_page(slist_id):
    '''
    if request is GET show list detail
    else get the list is and delete
    '''
    if request.method == 'GET':

        slist = current_app.store.get_slist(slist_id)

        return render_template('home.html', slist=slist)

    else:
		slist_ids = request.form.getlist('slist_ids')

		for slist_id in slist_ids:

			current_app.store.delete_slist(int(slist_id))

		flash('%d movies deleted.' % len(slist_ids))

    return redirect(url_for('site.product_page'))

@site.route('/shop/add', methods=['GET', 'POST'])
def slist_add_page():
    '''
    The get method will create a new form

    '''
    if request.method == 'GET':
        form = {'title': ''}

    else:
        # validat the data in the forms
        valid = validate_data(request.form)

        if valid:
            title = request.form.data['title']
            # add to class
            slist = ShoppingList(title)

            current_app.store.add_slist(slist)

            return redirect(url_for('site.home_page'))

        form = request.form
    return render_template('add_shopping_list.html', form=form)

@site.route('/shop/<int:slist_id>/edit', methods=['GET', 'POST'])
# @login_required
def slist_edit_page(slist_id):

    slist = current_app.store.get_slist(slist_id)

    if request.method == 'GET':

        form = {'title': slist.title}

        return render_template('add_shopping_list.html.html', form=form )

    else:

        slist.title = request.form['title']

        current_app.store.update_movie(slist)
        flash('list  data updated.')
        return redirect(url_for('site.product_page', slist_id=slist._id))


@site.route('/login', methods=['GET', 'POST'])
def login_page():

    form = LoginForm()

    if form.validate_on_submit():

        username = form.data['username']

        user = get_user(username)

        if user is not None:

            password = form.data['password']

            if pwd_context.verify(password, user.password):

                login_user(user)

                flash('You have logged in.')

                next_page = request.args.get('next', url_for('site.home_page'))

                return redirect(next_page)

        flash('Invalid credentials.')

    return render_template('sign-in.html', form=form)

@site.route('/logout')
def logout_page():

    logout_user()

    flash('You have logged out.')

    return redirect(url_for('site.home_page'))


def validate_data(form):
    form.data = {}

    form.errors = {}

    if len(form['title'].strip()) == 0:
        form.errors['title'] = 'Title can not be blank.'
    else:
        form.data['title'] = form['title']

    return len(form.errors) == 0