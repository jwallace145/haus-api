from flask_login import LoginManager
from models.user.user import User

login_manager = LoginManager()


@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None
