from flask import render_template, flash
from src.main import bp


@bp.route('/')
def index():
    return render_template('index.html',title="Dashboard Kanban::::")


@bp.route('/test-form', methods=['GET','POST'])
def test_form():
    from src.auth.forms import RegisterForm
    form = RegisterForm()

    if form.validate_on_submit():
        flash("Formulario Válido y enviado con exito", "success")

    return render_template("test_form.html", title="Prueba Formulario", form=form)

