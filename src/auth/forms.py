from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     SubmitField,
                     BooleanField
                     )
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


class RegisterForm(FlaskForm):
    username = StringField(
        'Usuario',
         validators=[
            DataRequired(),
            Length(min=3, max=80)
            ]
         )
    email = StringField('Correo Electrónico',
                        validators=[DataRequired(), Email()])
    password = PasswordField(
        'Contraseña',
         validators=[
             DataRequired(),
             Length(min=6)
             ]
         )
    
    confirm_password = PasswordField('Confirmar Contraseña',
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')


class LoginForm(FlaskForm):
    email = StringField(
        'Correo Electrónico',
        validators= [
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField('Iniciar Sesión')

    submit = SubmitField('Iniciar Sesión')


class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField(
        'Contraseña Actual',
        validators=[ DataRequired()]
    )

    new_password = PasswordField(
        'Contraseña Nueva',
        validators=[ DataRequired()]
    )

    confirm_new_password = PasswordField(
            'Confirmar Contraseña Nueva',
            validators=[
                DataRequired(),
                EqualTo(
                    'new_password',
                    message='Las Contraseñas no coinciden'
                )
            ]
        )

    submit = SubmitField('Actualizar Contraseña')

