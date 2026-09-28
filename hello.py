from datetime import datetime, timezone

from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired
import os



class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT email?', validators=[DataRequired()])
    submit = SubmitField('Submit')

    # Custom validator for email field, will be looked up by WTForms automatically based on the method name
    def validate_email(self, field):
        if '@' not in field.data:
            raise ValidationError(f'Please include an "@" in the email address. "{field.data}" is missing an "@".')
        if 'utoronto' not in field.data:
            raise ValidationError('Please enter a valid UofT email address.')


app = Flask(__name__)
secret_key = os.urandom(32)
app.config['SECRET_KEY'] = secret_key
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form =  NameForm()
    old_name = session.get('name')
    old_email = session.get('email')
    form_is_valid = form.validate_on_submit()

    if request.method == 'POST' and form.name.data and not form.name.errors:
        session['name'] = form.name.data

    if request.method == 'POST' and form.email.data and not form.email.errors:
        session['email'] = form.email.data

    if form_is_valid:
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        name = form.name.data
        form.name.data = ''

        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        email = form.email.data
        form.email.data = ''
        return render_template('index.html', form=form, name=name, email=email)
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))

@app.route('/hello/<name>')
def user(name):
    return render_template('user.html', name=name,
                           current_time=datetime.now(timezone.utc))
