from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField
from wtforms.fields.html5 import DateField, EmailField, TelField
from wtforms.validators import DataRequired, Length, Email
from wtforms.widgets.html5 import NumberInput, TelInput
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
    client = SelectField('Client',
                         choices=[])
    product = NoValidationSelectField('Product',
                                      choices=[])
    product_area = NoValidationSelectField('Product Area',
                                           choices=[])
    priority = IntegerField('Priority', widget=NumberInput(min=0),
                            validators=[DataRequired()])
    created_at = DateField('Created At',
                           validators=[DataRequired()],
                           default=date.today())
    target_date = DateField('Target Date',
                            validators=[DataRequired()])
    submit = SubmitField('Create')


class CreateClientForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=8, max=50)])
    bio = TextAreaField('Bio',
                        validators=[DataRequired()])
    email = EmailField('Email',
                       validators=[DataRequired(), Email()])
    phone_number = IntegerField('Phone Number',
                                widget=NumberInput(min=0),
                                validators=[DataRequired()])
    submit = SubmitField('Create')
