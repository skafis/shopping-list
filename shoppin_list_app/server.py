from flask import Flask
from flask_login import LoginManager

from app import site
from store import Store
from users import get_user


lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')
    app.register_blueprint(site)

    lm.init_app(app)
    lm.login_view = 'site.login_page'


    app.store = Store()
    return app


def main():
    app = create_app()
    debug = app.config['DEBUG']
    port = app.config.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    main()