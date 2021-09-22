from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileAllowed, FileField, FileRequired
from .models import Country

class ContinentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    submit = SubmitField('Add continent') 

class CountryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=3)])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField('Add country') 
    
    def validate_name(self, name):
        name = Country.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That country is already added!')

    def validate_image(self, image):
        if UploadNotAllowed():
            raise ValidationError('Please attach an image!')

class UpdateCountryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=3)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField('Update country item') 
    
    def validate_name(self, name):
        name = Country.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That leisure is already added!')

    def validate_image(self, image):
        if UploadNotAllowed():
            raise ValidationError('Please attach an image!')


class LeisureForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=3)])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField('Add leisure item') 
    
    def validate_name(self, name):
        name = Country.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That leisure is already added!')

    def validate_image(self, image):
        if UploadNotAllowed():
            raise ValidationError('Please attach an image!')

class UpdateLeisureForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=3)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField('Update leisure item') 
    
    def validate_name(self, name):
        name = Country.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That leisure is already added!')

    def validate_image(self, image):
        if UploadNotAllowed():
            raise ValidationError('Please attach an image!')

class LandmarksForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=3)])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField('Add landmarks item') 
    
    def validate_name(self, name):
        name = Country.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That landmark is already added!')

    def validate_image(self, image):
        if UploadNotAllowed():
            raise ValidationError('Please attach an image!')

class UpdateLandmarksForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=3)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField('Update landmarks item') 
    
    def validate_name(self, name):
        name = Country.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That landmark is already added!')

    def validate_image(self, image):
        if UploadNotAllowed():
            raise ValidationError('Please attach an image!')

class FoodForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=3)])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField('Add food item') 
    
    def validate_name(self, name):
        name = Country.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That food is already added!')

    def validate_image(self, image):
        if UploadNotAllowed():
            raise ValidationError('Please attach an image!')

class UpdateFoodForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=3)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField('Update food item') 
    
    def validate_name(self, name):
        name = Country.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That food is already added!')

    def validate_image(self, image):
        if UploadNotAllowed():
            raise ValidationError('Please attach an image!')

class UpdateFoodForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=3)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField('Update food item') 
    
    def validate_name(self, name):
        name = Country.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That food is already added!')

    def validate_image(self, image):
        if UploadNotAllowed():
            raise ValidationError('Please attach an image!')

class CultureForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=3)])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField('Add culture item') 
    
    def validate_name(self, name):
        name = Country.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That culture is already added!')

    def validate_image(self, image):
        if UploadNotAllowed():
            raise ValidationError('Please attach an image!')

class UpdateCultureForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=3)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField('Update culture item') 
    
    def validate_name(self, name):
        name = Country.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That culture is already added!')

    def validate_image(self, image):
        if UploadNotAllowed():
            raise ValidationError('Please attach an image!')

class AdventureForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=3)])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField('Add adventure item') 
    
    def validate_name(self, name):
        name = Country.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That culture is already added!')

    def validate_image(self, image):
        if UploadNotAllowed():
            raise ValidationError('Please attach an image!')

class UpdateAdventureForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=3)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField('Update adventure item') 
    
    def validate_name(self, name):
        name = Country.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That adventure is already added!')

    def validate_image(self, image):
        if UploadNotAllowed():
            raise ValidationError('Please attach an image!')
