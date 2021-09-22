from flask import render_template, Blueprint, request, flash, redirect, url_for, session, current_app
from travel import db, photos
from travel.countries.models import Country, Leisure, Adventure, Landmarks, Culture, Continent, Food
from travel.countries.forms import CountryForm, ContinentForm, LeisureForm, LandmarksForm, FoodForm, CultureForm, AdventureForm, UpdateCountryForm, UpdateFoodForm, UpdateLeisureForm, UpdateLandmarksForm, UpdateCultureForm, UpdateAdventureForm
from flask_login import current_user
import secrets, os

admin_views = Blueprint('admin_views', __name__)

@admin_views.route('/', methods=['GET', 'POST'])
def index():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    countries = Country.query.order_by(Country.id.desc()).all()
    return render_template('admin/admin.html', countries=countries)

@admin_views.route('/continents', methods=['GET', 'POST'])
def continents():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    continents = Continent.query.order_by(Continent.id.desc()).all()
    return render_template('admin/display_continents.html', continents=continents)

@admin_views.route('/countries', methods=['GET', 'POST'])
def countries():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    countries = Country.query.order_by(Country.id.desc()).all()
    return render_template('admin/display.html', countries=countries)

@admin_views.route('/leisure', methods=['GET', 'POST'])
def leisure():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    leisure_items = Leisure.query.order_by(Leisure.id.desc()).all()
    return render_template('admin/display.html', leisure_items=leisure_items)

@admin_views.route('/landmarks', methods=['GET', 'POST'])
def landmarks():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    landmarks_items = Landmarks.query.order_by(Landmarks.id.desc()).all()
    return render_template('admin/display.html', landmarks_items=landmarks_items)

@admin_views.route('/adventure', methods=['GET', 'POST'])
def adventure():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    adventure_items = Adventure.query.order_by(Adventure.id.desc()).all()
    return render_template('admin/display.html', adventure_items=adventure_items)

@admin_views.route('/culture', methods=['GET', 'POST'])
def culture():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    culture_items = Culture.query.order_by(Culture.id.desc()).all()
    return render_template('admin/display.html', culture_items=culture_items)

@admin_views.route('/food', methods=['GET', 'POST'])
def food():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    food_items = Food.query.order_by(Food.id.desc()).all()
    return render_template('admin/display.html', food_items=food_items)

@admin_views.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'email' in session:
        return redirect(url_for('admin_auth.login'))
    flash('A problem has occurred!', 'danger')
    return redirect(url_for('admin_views.index'))

@admin_views.route('/add_country', methods=['GET', 'POST'])
def add_country():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    continents = Continent.query.all()
    form = CountryForm(request.form)
    if request.method == 'POST':
        image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
        continent = request.form.get('continent')
        country = Country(name=form.name.data, description = form.description.data, image=image, continent_id=continent)
        db.session.add(country)
        db.session.commit()
        flash(f'Country {form.name.data} is added!', 'success')
        return redirect(url_for('admin_views.add_country'))
    return render_template('countries/add_country.html', form=form, continents=continents)

@admin_views.route('/update_country/<int:id>', methods=['GET', 'POST'])
def update_country(id):
    continents = Continent.query.all()
    country = Country.query.get_or_404(id)
    country_continent = request.form.get('continent')
    form = UpdateCountryForm(request.form)
    if request.method == 'POST':
        country.name = form.name.data
        country.description = form.description.data
        country.continent_id = country_continent
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/img/' + country.image))
                country.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
            except:  
                country.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
        db.session.commit()
        flash('Country has been updated!', 'success')
        return redirect(url_for('admin_views.index'))
    form.name.data = country.name
    form.description.data = country.description
    country_name = request.form.get('country')
    return render_template('countries/update_country.html', form=form, item='Update', continents=continents, country=country, country_continent=country_continent)

@admin_views.route('/delete_country/<int:id>', methods=['POST'])
def delete_country(id):
    country = Country.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(country)
        db.session.commit()
        flash(f'Country {country.name} is deleted!', 'success')
        return redirect(url_for('admin_views.index'))
    flash(f'Country {country.name} cannot be deleted!', 'danger')
    return redirect(url_for('admin_views.index'))

@admin_views.route('add_continent', methods=['GET', 'POST'])
def add_continent():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    form = ContinentForm(request.form)
    if request.method == 'POST':
        continent = Continent(name=form.name.data)
        db.session.add(continent)
        db.session.commit()
        flash(f'Continent {form.name.data} is added!', 'success')
        return redirect(url_for('admin_views.add_continent'))
    return render_template('countries/continent.html', form=form, item='Add')

@admin_views.route('/update_continent/<int:id>', methods=['GET', 'POST'])
def update_continent(id):
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    update_continent = Continent.query.get_or_404(id)
    form = ContinentForm(request.form)
    form.name.data = update_continent.name
    if request.method == 'POST':
        update_continent.name = form.name.data
        db.session.commit()
        flash(f'The Continent {update_continent.name} has been updated!', 'success')
        return redirect(url_for('admin_views.continents'))
    return render_template('countries/continent.html', item='Update', form=form)

@admin_views.route('/delete_continent/<int:id>', methods=['POST'])
def delete_continent(id):
    continent = Continent.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(continent)
        db.session.commit()
        flash(f'Continent {continent.name} is deleted!', 'success')
        return redirect(url_for('admin_views.continents'))
    flash(f'Continent {continent.name} cannot be deleted!', 'danger')
    return redirect(url_for('admin_views.continents'))

@admin_views.route('add_leisure', methods=['GET', 'POST'])
def add_leisure():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    form = LeisureForm(request.form)
    countries = Country.query.all()
    if request.method == 'POST':
        image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
        country = request.form.get('country')
        leisure = Leisure(name=form.name.data, description = form.description.data, image=image, country_id=country)
        db.session.add(leisure)
        db.session.commit()
        flash(f'Leisure Item {form.name.data} is added!', 'success')
        return redirect(url_for('admin_views.add_leisure'))
    return render_template('countries/add_items.html', form=form, countries=countries, item='Leisure')

@admin_views.route('/update_leisure/<int:id>', methods=['GET', 'POST'])
def update_leisure(id):
    countries = Country.query.all()
    leisure = Leisure.query.get_or_404(id)
    country = request.form.get('country')
    form = UpdateLeisureForm(request.form)
    if request.method == 'POST':
        leisure.name = form.name.data
        leisure.description = form.description.data
        leisure.country_id = country
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/img/' + leisure.image))
                leisure.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
            except:  
                leisure.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
        db.session.commit()
        flash('Country has been updated!', 'success')
        return redirect(url_for('admin_views.leisure'))
    form.name.data = leisure.name
    form.description.data = leisure.description
    country_name = request.form.get('country')
    return render_template('countries/update_leisure.html', form=form, countries=countries, leisure=leisure, country=country)

@admin_views.route('/delete_leisure/<int:id>', methods=['POST'])
def delete_leisure(id):
    leisure = Leisure.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/img/' + leisure.image))
        except Exception as e:
            print(e)
        db.session.delete(leisure)
        db.session.commit()
        flash(f'Leisure Item {leisure.name} is deleted!', 'success')
        return redirect(url_for('admin_views.leisure'))
    flash(f'Leisure Item {leisure.name} cannot be deleted!', 'danger')
    return redirect(url_for('admin_views.leisure'))

@admin_views.route('add_landmarks', methods=['GET', 'POST'])
def add_landmarks():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    form = LandmarksForm(request.form)
    countries = Country.query.all()
    if request.method == 'POST':
        image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
        country = request.form.get('country')
        landmarks = Landmarks(name=form.name.data, description = form.description.data, image=image, country_id=country)
        db.session.add(landmarks)
        db.session.commit()
        flash(f'Landmarks Item {form.name.data} is added!', 'success')
        return redirect(url_for('admin_views.add_landmarks'))
    return render_template('countries/add_items.html', form=form, countries=countries, item='Landmarks')

@admin_views.route('/update_landmarks/<int:id>', methods=['GET', 'POST'])
def update_landmarks(id):
    countries = Country.query.all()
    landmarks = Landmarks.query.get_or_404(id)
    country = request.form.get('country')
    form = UpdateLandmarksForm(request.form)
    if request.method == 'POST':
        landmarks.name = form.name.data
        landmarks.description = form.description.data
        landmarks.country_id = country
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/img/' + landmarks.image))
                landmarks.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
            except:  
                landmarks.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
        db.session.commit()
        flash('Country has been updated!', 'success')
        return redirect(url_for('admin_views.landmarks'))
    form.name.data = landmarks.name
    form.description.data = landmarks.description
    country_name = request.form.get('country')
    return render_template('countries/update_landmarks.html', form=form, countries=countries, landmarks=landmarks, country=country)

@admin_views.route('/delete_landmarks/<int:id>', methods=['POST'])
def delete_landmarks(id):
    landmarks = Landmarks.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/img/' + landmarks.image))
        except Exception as e:
            print(e)
        db.session.delete(landmarks)
        db.session.commit()
        flash(f'Landmarks Item {landmarks.name} is deleted!', 'success')
        return redirect(url_for('admin_views.landmarks'))
    flash(f'Landmarks Item {landmarks.name} cannot be deleted!', 'danger')
    return redirect(url_for('admin_views.landmarks'))

@admin_views.route('add_food', methods=['GET', 'POST'])
def add_food():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    form = FoodForm(request.form)
    countries = Country.query.all()
    if request.method == 'POST':
        image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
        country = request.form.get('country')
        food = Food(name=form.name.data, description = form.description.data, image=image, country_id=country)
        db.session.add(food)
        db.session.commit()
        flash(f'Food Item {form.name.data} is added!', 'success')
        return redirect(url_for('admin_views.add_food'))
    return render_template('countries/add_items.html', form=form, countries=countries, item='Food')

@admin_views.route('/update_food/<int:id>', methods=['GET', 'POST'])
def update_food(id):
    countries = Country.query.all()
    food = Food.query.get_or_404(id)
    country = request.form.get('country')
    form = UpdateFoodForm(request.form)
    if request.method == 'POST':
        food.name = form.name.data
        food.description = form.description.data
        food.country_id = country
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/img/' + food.image))
                food.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
            except:  
                food.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
        db.session.commit()
        flash('Country has been updated!', 'success')
        return redirect(url_for('admin_views.food'))
    form.name.data = food.name
    form.description.data = food.description
    country_name = request.form.get('country')
    return render_template('countries/update_food.html', form=form, countries=countries, food=food, country=country)

@admin_views.route('/delete_food/<int:id>', methods=['POST'])
def delete_food(id):
    food = Food.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/img/' + food.image))
        except Exception as e:
            print(e)
        db.session.delete(food)
        db.session.commit()
        flash(f'Food Item {food.name} is deleted!', 'success')
        return redirect(url_for('admin_views.food'))
    flash(f'Food Item {food.name} cannot be deleted!', 'danger')
    return redirect(url_for('admin_views.food'))

@admin_views.route('add_culture', methods=['GET', 'POST'])
def add_culture():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    form = CultureForm(request.form)
    countries = Country.query.all()
    if request.method == 'POST':
        image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
        country = request.form.get('country')
        culture = Culture(name=form.name.data, description = form.description.data, image=image, country_id=country)
        db.session.add(culture)
        db.session.commit()
        flash(f'Culture Item {form.name.data} is added!', 'success')
        return redirect(url_for('admin_views.add_culture'))
    return render_template('countries/add_items.html', form=form, countries=countries, item='Culture')

@admin_views.route('/update_culture/<int:id>', methods=['GET', 'POST'])
def update_culture(id):
    countries = Country.query.all()
    culture = Culture.query.get_or_404(id)
    country = request.form.get('country')
    form = UpdateCultureForm(request.form)
    if request.method == 'POST':
        culture.name = form.name.data
        culture.description = form.description.data
        culture.country_id = country
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/img/' + culture.image))
                culture.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
            except:  
                culture.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
        db.session.commit()
        flash('Country has been updated!', 'success')
        return redirect(url_for('admin_views.culture'))
    form.name.data = culture.name
    form.description.data = culture.description
    country_name = request.form.get('country')
    return render_template('countries/update_culture.html', form=form, countries=countries, culture=culture, country=country)

@admin_views.route('/delete_culture/<int:id>', methods=['POST'])
def delete_culture(id):
    culture = Culture.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/img/' + culture.image))
        except Exception as e:
            print(e)
        db.session.delete(culture)
        db.session.commit()
        flash(f'Culture Item {culture.name} is deleted!', 'success')
        return redirect(url_for('admin_views.culture'))
    flash(f'Culture Item {culture.name} cannot be deleted!', 'danger')
    return redirect(url_for('admin_views.culture'))

@admin_views.route('add_adventure', methods=['GET', 'POST'])
def add_adventure():
    if 'email' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_auth.login'))
    form = AdventureForm(request.form)
    countries = Country.query.all()
    if request.method == 'POST':
        image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
        country = request.form.get('country')
        adventure = Adventure(name=form.name.data, description = form.description.data, image=image, country_id=country)
        db.session.add(adventure)
        db.session.commit()
        flash(f'Adventure Item {form.name.data} is added!', 'success')
        return redirect(url_for('admin_views.add_adventure'))
    return render_template('countries/add_items.html', form=form, countries=countries, item='Adventure')

@admin_views.route('/update_adventure/<int:id>', methods=['GET', 'POST'])
def update_adventure(id):
    countries = Country.query.all()
    adventure = Adventure.query.get_or_404(id)
    country = request.form.get('country')
    form = UpdateAdventureForm(request.form)
    if request.method == 'POST':
        adventure.name = form.name.data
        adventure.description = form.description.data
        adventure.country_id = country
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/img/' + adventure.image))
                adventure.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
            except:  
                adventure.image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + '.')
        db.session.commit()
        flash('Country has been updated!', 'success')
        return redirect(url_for('admin_views.adventure'))
    form.name.data = adventure.name
    form.description.data = adventure.description
    country_name = request.form.get('country')
    return render_template('countries/update_adventure.html', form=form, countries=countries, adventure=adventure, country=country)

@admin_views.route('/delete_adventure/<int:id>', methods=['POST'])
def delete_adventure(id):
    adventure = Adventure.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/img/' + adventure.image))
        except Exception as e:
            print(e)
        db.session.delete(adventure)
        db.session.commit()
        flash(f'Adventure Item {adventure.name} is deleted!', 'success')
        return redirect(url_for('admin_views.adventure'))
    flash(f'Adventure Item {adventure.name} cannot be deleted!', 'danger')
    return redirect(url_for('admin_views.adventure'))