from flask_admin import Admin, BaseView, AdminIndexView, expose
from flask_login import current_user
from app.models import User
from app import db


class DashboardView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_admin == True:
            return self.render('admin/dashboard_index.html')
        else:
            return 'Вы не администратор'