from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Optional, StopValidation
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
