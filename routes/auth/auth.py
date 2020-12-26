import os

import bcrypt
from flask import Blueprint, request, session
from flask_login import current_user, login_required, login_user, logout_user
from models.user.user import User
from services.clients import s3_client
from services.database import db
from werkzeug.utils import secure_filename

auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    avatar = request.files['avatar']

    hashed_password = bcrypt.hashpw(
        str(password).encode('utf-8'), bcrypt.gensalt())

    user = User(
        email=email,
        username=username,
        password=hashed_password
    )

    filename = secure_filename(avatar.filename)
    avatar.save(filename)

    s3_client.upload_file(
        Bucket='jwalls-fun-bucket',
        Filename=filename,
        Key=f'profile-pics/{filename}',
        ExtraArgs={'ACL': 'public-read'}
    )

    os.remove(filename)

    user.avatar_url = f'https://jwalls-fun-bucket.s3.amazonaws.com/profile-pics/{filename}'
    db.session.add(user)
    db.session.commit()

    user = db.session.query(User).filter_by(username=username).first()

    user.authenticated = True
    db.session.commit()

    login_user(user)

    return {
        'register': True,
        'user': user.to_dict()
    }


@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = bytes(request.form['password'], 'utf-8')

    user = db.session.query(User).filter_by(username=username).first()

    authenticate = bcrypt.checkpw(password, user.password)

    if authenticate:
        user.authenticated = True
        db.session.add(user)
        db.session.commit()

        login_user(user)

        return {
            'login': True,
            'user': user.to_dict()
        }
    else:
        return {
            'login': False
        }


@auth_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():

    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    session.clear()

    return {'logout': True}
