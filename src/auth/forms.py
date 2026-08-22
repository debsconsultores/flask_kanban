from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     SubmitField,
                     BooleanField
                     )
from wtforms.validators import DataRequired, Email, EqualTo, Length


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

