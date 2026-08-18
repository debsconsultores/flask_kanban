from flask import (
    render_template,
    redirect,
    url_for, 
    flash
)

from flask_login import current_user
from src.extensions import db, bcrypt
from src.auth import bp
from src.auth.forms import RegisterForm
from src.models import User


@bp.route('/register', methods=['GET','POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')

        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash= hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        flash(
            'Cuenta Creada Satisfactoriamente. Ya puedes iniciar sesión',
            'success'
            )
        return redirect(url_for('auth.login'))

    return render_template(
        'auth/register.html',
        title ='Registro',
        form=form
    )