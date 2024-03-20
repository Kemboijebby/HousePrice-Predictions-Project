from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from urllib import parse


app = Flask(__name__)
pwd = parse.quote('')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://root:{pwd}@localhost:3306/housePrediction"
db = SQLAlchemy(app)

@app.route('/', methods=["GET", "POST"])
def predictPrice():
    """Endpoint to predict house rent price"""
    if request.method == 'POST':
        location = request.form['uilocation']
        locations = text("SELECT location FROM locations")
        locations = db.session.execute(locations).scalars()
        
        location_list = [ loc for loc in locations]
        print(location_list)
        if location not in locations:
            return render_template('index.html', location_missing=f"cannot find {location}, please try searching for a ward in Nairobi")

        
        bedrooms = request.form['uiBHK']
        bathrooms = request.form['uiBathrooms']
        alarm = request.form.get('Alarm')
        bbq = request.form.get('BBQ')
        balcony = request.form.get('Balcony')
        en_suite = request.form.get('En-Suite')
        internet = request.form.get('Internet')
        print(location, bedrooms, bathrooms, alarm, bbq, balcony, en_suite, internet)
    return render_template('index.html')