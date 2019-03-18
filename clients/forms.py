from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, Form, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from clients.models import Customer


class RegistrationForm(FlaskForm):
    region = StringField('Region', 
                            validators=[DataRequired(), Length(min=2)])
    company_name = StringField('Company name', 
                            validators=[DataRequired(), Length(min=2)])
    specialization = StringField('Specialization', 
                            validators=[DataRequired(), Length(min=2)])
    email = StringField('Contact Email',
                        validators=[DataRequired(), Email()])
    phone_number = StringField('Contact Phone number', 
                            validators=[DataRequired(), Length(min=8)])
    company_data = StringField('Info about company', 
                            validators=[DataRequired(), Length(min=2)])
    picture = FileField('Upload photo',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload Data')

    def validate_company_name(self, company_name):
        company_name = Customer.query.filter_by(company_name=company_name.data).first()
        if company_name:
            raise ValidationError('This company already in database.')

    def validate_email(self, email):
        email = Customer.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email already in database.')

    def validate_phone_number(self, phone_number):
        phone_number = Customer.query.filter_by(phone_number=phone_number.data).first()
        if phone_number:
            raise ValidationError('This phone number already in database.')


class UpdatePostForm(FlaskForm):
    region = StringField('Region', 
                            validators=[DataRequired(), Length(min=2)])
    company_name = StringField('Company name', 
                            validators=[DataRequired(), Length(min=2)])
    specialization = StringField('Specialization', 
                            validators=[DataRequired(), Length(min=2)])
    email = StringField('Contact Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Contact Phone number', 
                            validators=[DataRequired(), Length(min=8)])
    company_data = StringField('Info about company', 
                            validators=[DataRequired(), Length(min=2)])
    picture = FileField('Update photo', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Data')

    def validate_company_name(self, company_name):
        if company_name != company_name:
            company_name = Customer.query.filter_by(company_name=company_name.data).first()
            if company_name:
                raise ValidationError('This company already in database.')

    def validate_email(self, email):
        if email != email:
            email = Customer.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('This email already in database.')

    def validate_phone_number(self, phone_number):
        if phone_number != phone_number:
            phone_number = Customer.query.filter_by(phone_number=phone_number.data).first()
            if phone_number:
                raise ValidationError('This phone number already in database.')