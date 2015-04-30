# -*- coding: utf-8 -*-
from flask import url_for, redirect
from flask.ext.login import LoginManager, login_user, logout_user, login_required
from tuesday import app
from user import user_manager
from form import LoginForm


login_manager = LoginManager()
login_manager.setup_app(app)


@login_manager.user_loader
def load_user(id):
    return user_manager.get_user(id)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if user_manager.get_current_user():
        # someone is using
        return redirect(url_for('index'))
    else:
        if form.validate_on_submit():
            user = user_manager.create_user(form.name.data)
            login_user(user)
            return redirect(url_for('index'))
        return redirect(url_for('index'))


@app.route("/logout/")
@login_required
def logout():
    user_manager.clear()
    logout_user()
    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))
