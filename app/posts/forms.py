from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=['python', 'Category No.2', 'Category No.3',
                                                'Category No.4', 'Category No.5'])
    submit = SubmitField('Submit', validators=[DataRequired()])


class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=['Category No.1', 'Category No.2', 'Category No.3',
                                                'Category No.4', 'Category No.5'])
    submit = SubmitField('Edit', validators=[DataRequired()])
