from flask import render_template, Blueprint, request, flash, redirect, url_for, session, current_app
from travel import db, photos
from .forms import CountryForm, ContinentForm, LeisureForm, LandmarksForm, FoodForm, CultureForm, AdventureForm, UpdateCountryForm, UpdateFoodForm, UpdateLeisureForm, UpdateLandmarksForm, UpdateCultureForm, UpdateAdventureForm
from .models import Country, Continent, Leisure, Landmarks, Food, Culture, Adventure
from flask_login import current_user
import secrets, os

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    india = Country.query.filter_by(id=1).first()
    china = Country.query.filter_by(id=2).first()
    italy = Country.query.filter_by(id=3).first()
    france = Country.query.filter_by(id=4).first()
    indonesia = Country.query.filter_by(id=5).first()
    japan = Country.query.filter_by(id=6).first()
    ireland = Country.query.filter_by(id=7).first()
    mexico = Country.query.filter_by(id=8).first()
    portugal = Country.query.filter_by(id=9).first()
    spain = Country.query.filter_by(id=10).first()
    thailand = Country.query.filter_by(id=11).first()
    usa = Country.query.filter_by(id=12).first()
    uae = Country.query.filter_by(id=13).first()
    return render_template('index.html', india=india, china=china, italy=italy, france=france, indonesia=indonesia, japan=japan, ireland=ireland, mexico=mexico, portugal=portugal, spain=spain, thailand=thailand, usa=usa, uae=uae, user=current_user)

@views.route('/explore')
def explore():
    countries = Country.query.all()
    return render_template('explore.html', countries=countries, user=current_user)

@views.route('/destinations')
def destinations():
    return render_template('destinations.html', user=current_user)

@views.route('/country/<id>')
def getcountry(id):
    getcountry = Country.query.filter_by(id=id).first_or_404()
    leisure = Leisure.query.filter_by(country=getcountry)
    landmarks = Landmarks.query.filter_by(country=getcountry)
    food = Food.query.filter_by(country=getcountry)
    culture = Culture.query.filter_by(country=getcountry)
    adventure = Adventure.query.filter_by(country=getcountry)
    return render_template('countries/country.html', user=current_user, getcountry=getcountry, leisure=leisure, landmarks=landmarks, food=food, culture=culture, adventure=adventure, id=id)