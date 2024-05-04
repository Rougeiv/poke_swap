from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField   
from wtforms.validators import Length, DataRequired

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')