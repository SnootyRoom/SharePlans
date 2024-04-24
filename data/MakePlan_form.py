from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class PlanForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    about = TextAreaField("О плане", validators=[DataRequired()])
    private = BooleanField('Сделать приватным')
    submit = SubmitField('Создать')