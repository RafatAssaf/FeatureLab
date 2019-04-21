from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired, Length, Email
from wtforms.widgets.html5 import NumberInput
from datetime import date


class NoValidationSelectField(SelectField):
    """
        Create a version of that do not pre-validate the options
        This is necessary to implement dynamic choices
    """
    def pre_validate(self, form):
        pass


class CreateRequestForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(), Length(min=8, max=50)])
    description = TextAreaField('Description',
                                validators=[DataRequired()])
    client = NoValidationSelectField('Client',
                         choices=[])
    product = NoValidationSelectField('Product',
                                      choices=[])
    product_area = NoValidationSelectField('Product Area',
                                           choices=[])
    created_at = DateField('Created At',
                           validators=[DataRequired()],
                           default=date.today())
    target_date = DateField('Target Date',
                            validators=[DataRequired()])
    submit = SubmitField('Create')


class CreateProductForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=8, max=50)])
    description = TextAreaField('Description',
                                validators=[DataRequired()])
    areas = StringField('Areas',
                        validators=[DataRequired()],
                        render_kw={'placeholder': 'comma separated. i.e. "Search,Profile, ... etc"'})
    submit = SubmitField('Create')


class CreateClientForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=8, max=50)])
    bio = TextAreaField('Bio',
                        validators=[DataRequired()])
    email = EmailField('Email',
                       validators=[DataRequired(), Email()])
    phone_number = IntegerField('Phone Number',
                                widget=NumberInput(min=8, max=13),
                                validators=[DataRequired()])
    priority = IntegerField('Priority', widget=NumberInput(min=1),
                            validators=[DataRequired()])
    submit = SubmitField('Create')
