from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from wtforms import StringField, SubmitField, PasswordField


class GetStarted(FlaskForm):
    started = SubmitField("Get Started")


class CreateForm1(FlaskForm):
    uid = StringField("UID", validators=[DataRequired()], render_kw={"placeholder": "Your UID"})
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Your Email"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Your Password"})
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()],
                                     render_kw={"placeholder": "Confirm Password"})
    create = SubmitField("Create Entry")


class CreateForm2(FlaskForm):
    uid = StringField("UID", validators=[DataRequired()], render_kw={"placeholder": "Your UID"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Your Password"})
    login = SubmitField("Login Entry")


class ReadForm(FlaskForm):
    read = SubmitField("Read Entry")


class UpdateForm(FlaskForm):
    update = SubmitField("Update Entry")


class DeleteForm(FlaskForm):
    delete = SubmitField("Delete Entry")