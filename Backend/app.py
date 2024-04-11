from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from urllib import parse
import pickle
import pandas as pd
import numpy as np


app = Flask(__name__)
pwd = parse.quote('') # replace with your DB password


app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://root:{pwd}@localhost:3306/housePrediction"
db = SQLAlchemy(app)

model = pickle.load(open('model.pkl' , 'rb'))

@app.route('/', methods=["GET", "POST"])
def predictPrice():
    """Endpoint to predict house rent price"""
    if request.method == 'POST':
        location = request.form['uilocation'].strip()
        locations = text("SELECT location FROM locations")
        locations = db.session.execute(locations).scalars()
        
        location_list = [ loc for loc in locations]
        print(location_list)
        print(location in location_list)
        if location == "":
            return render_template('index.html', location_missing=f"Please enter the location in order to continue with the prediction")
        if location not in location_list:
            return render_template('index.html', location_missing=f"cannot find {location}, please try searching for a ward in Nairobi")


        bedrooms = request.form['uiBHK']
        bathrooms = request.form['uiBathrooms']
        alarm = request.form.get('Alarm')
        bbq = request.form.get('BBQ')
        balcony = request.form.get('Balcony')
        en_suite = request.form.get('En-Suite')
        internet = request.form.get('Internet')
        garden = request.form.get('Garden')
        closet = request.form.get('Closet')
        golf_course = request.form.get('GolfCourse')
        staff_quarters = request.form.get('StaffQuarters')
        wheelchair = request.form.get('WheelChair Access')

        if alarm:
            alarm = 1
        else:
            alarm = 0
        if bbq:
            bbq = 1
        else:
            bbq = 0
        if balcony:
            balcony = 1
        else:
            balcony = 0
        if en_suite:
            en_suite = 1
        else:
            en_suite = 0
        if internet:
            internet = 1
        else:
            internet = 0
        if garden:
            garden = 1 
        else:
            garden = 0
        if closet:
            closet = 1
        else:
            closet = 0
        if golf_course:
            golf_course = 1
        else:
            golf_course = 0
        if staff_quarters:
            staff_quarters = 1
        else:
            staff_quarters = 0
        if wheelchair:
            wheelchair = 1
        else:
            wheelchair = 0
        my_columns=pd.read_csv('/home/crackygeek/Desktop/HousePrice-Predictions-Project/Backend/data/dataset_columns.csv')

        pred=predict_price(data=my_columns,location=location,bed=bedrooms,bath=bathrooms,balcony=balcony,
                    ensiut=en_suite,alarm=alarm,bbq=bbq,fibreinternet=internet,garden=garden,StaffQuarters=staff_quarters,
                    Closet=closet,WheelchairAccess=wheelchair,GolfCourse=golf_course)


        return render_template('index.html', prediction=round(pred, 0)) 

    return render_template('index.html')

def predict_price(data,location,bed,bath,balcony,ensiut,alarm,bbq,fibreinternet,garden,StaffQuarters,Closet,
       WheelchairAccess,GolfCourse):
    print(data.head())
    loc_index=np.where(data.columns==location)[0][0]
    x=np.zeros(len(data.columns))
    x[0] = bed
    x[1] = bath
    x[2] = balcony
    x[3] = ensiut
    x[4] = alarm
    x[5] = bbq
    x[6] = fibreinternet
    x[7] = garden
    x[8] = StaffQuarters
    x[9] = Closet
    x[10]= WheelchairAccess
    x[11]= GolfCourse

    if loc_index >=0:
        x[loc_index]=1
    return model.predict([x])[0]