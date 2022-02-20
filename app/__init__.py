from flask import Flask
from app.config import Config, current_path
from app.models import db, Category, Meal, Order, User
from app.admin import DashboardView
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_moment import Moment

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'auth'
migrate = Migrate(app, db, render_as_batch=True)
moment = Moment(app)
admin = Admin(app, index_view=DashboardView())
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Order, db.session))

@app.before_first_request
def create_tables():
    db.create_all()

    # db.session.query(User).filter(User.mail=='asdasd1234@gmail.com').is_admin = True
    # db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app.views import *
