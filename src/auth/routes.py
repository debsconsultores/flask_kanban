from flask import (
    render_template,
    redirect,
    url_for, 
    flash,
    request
)

from flask_login import current_user, login_user, login_required, logout_user
from src.extensions import db, bcrypt
from src.auth import bp
from src.auth.forms import RegisterForm, LoginForm
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
        # return redirect(url_for('main.index'))

    return render_template(
        'auth/register.html',
        title='Registro',
        form=form
    )


@bp.route('/login', methods=['GET', 'POST'])
def login():

    # Si el usuario ya está autenticado,
    # no necesitamos mostrar nuevamente el login.
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # Creamos una instancia del formulario.
    form = LoginForm()

    # Procesamos el formulario solamente si
    # fue enviado y pasó todas las validaciones.
    if form.validate_on_submit():

        # Buscamos el usuario utilizando su email.
        #user = User.query.filter_by(
        #    email=form.email.data
        #).first()
        # Buscamos el usuario utilizando su email
        user = db.session.scalar(
            db.select(User).filter_by(email=form.email.data)
        )

        # Verificamos que el usuario exista
        # y que la contraseña coincida con su hash.
        if user and bcrypt.check_password_hash(
            user.password_hash,
            form.password.data
        ):

            # Creamos la sesión autenticada.
            login_user(
                user,
                remember=form.remember.data
            )

            # Comprobamos si Flask-Login nos envió
            # a esta página desde una ruta protegida.
            next_page = request.args.get('next')

            # Si existe una URL de destino,
            # regresamos allí.
            # Si no existe, vamos al Dashboard.
            return redirect(
                next_page or url_for('auth.dashboard')
            )

        # Si el usuario no existe o la contraseña
        # no coincide, mostramos un mensaje.
        flash(
            'Credenciales inválidas',
            'danger'
        )

    # Mostramos el formulario.
    return render_template(
        'auth/login.html',
        title='Iniciar sesión',
        form=form
    )



@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template(
        'main/dahsboard.html',
        title='Mi Kanban'
    )


@bp.route('/logout')
def logout():

    # Cerramos la sesión del usuario actual.
    logout_user()

    # Después de cerrar sesión,
    # regresamos al formulario de login.
    return redirect(url_for('auth.login'))