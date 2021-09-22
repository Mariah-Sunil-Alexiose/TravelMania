from travel import db
from travel.user.models import Post, Comment

class Continent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150), nullable=False)

    continent_id = db.Column(db.Integer, db.ForeignKey('continent.id'), nullable=False)
    continent = db.relationship('Continent', backref=db.backref('continent', lazy=True))
    
    leisure = db.relationship('Leisure', backref='leisure_country',overlaps="leisure,leisure_country")
    landmarks = db.relationship('Landmarks', backref='landmarks_country',overlaps="landmarks,landmarks_country")
    food = db.relationship('Food', backref='food_country',overlaps="food,food_country")
    culture = db.relationship('Culture', backref='culture_country',overlaps="culture,culture_country")
    adventure = db.relationship('Adventure', backref='adventure_country',overlaps="adventure,adventure_country")
    posts = db.relationship('Post', backref='post_country',overlaps="country,post_country", passive_deletes=True)

class Leisure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150), nullable=False)
    
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country', backref=db.backref('leisure_country',overlaps="leisure,leisure_country", lazy=True))

class Landmarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150), nullable=False)
    
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country', backref=db.backref('landmarks_country', lazy=True),overlaps="landmarks,landmarks_country")

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150), nullable=False)
    
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country', backref=db.backref('food_country', lazy=True),overlaps="food,food_country")

class Culture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150), nullable=False)
    
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country', backref=db.backref('culture_country', lazy=True),overlaps="culture,culture_country")

class Adventure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150), nullable=False)
    
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country', backref=db.backref('adventure_country', lazy=True),overlaps="adventure,adventure_country")