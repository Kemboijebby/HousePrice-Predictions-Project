from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from urllib import parse
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
import pandas as pd
import pickle


app = Flask(__name__)
pwd = parse.quote('')

# with open('model.pkl', 'rb') as f:
#     model = pickle.load(f)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://root:{pwd}@localhost:3306/housePrediction"
db = SQLAlchemy(app)

@app.route('/', methods=["GET", "POST"])
def predictPrice():
    """Endpoint to predict house rent price"""
    if request.method == 'POST':
        location = request.form['uilocation'].capitalize().strip()
        locations = text("SELECT location FROM locations")
        locations = db.session.execute(locations).scalars()
        
        location_list = [ loc for loc in locations]
        print(location_list)
        print(location in location_list)
        if location not in location_list:
            return render_template('index.html', location_missing=f"cannot find {location}, please try searching for a ward in Nairobi")

        
        bedrooms = request.form['uiBHK']
        bathrooms = request.form['uiBathrooms']
        alarm = request.form.get('Alarm')
        bbq = request.form.get('BBQ')
        balcony = request.form.get('Balcony')
        en_suite = request.form.get('En-Suite')
        internet = request.form.get('Internet')
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

        import pandas as pd

        model = load_model('./model.h5')
        


        data = {
            'Bedrooms': [float(bedrooms)],
            'Bathrooms': [float(bathrooms)],
            '\'Borehole\'': [0],
            '\'Bus Stop\'': [1],
            '\'Golf Course\'': [0],
            '\'Gym\'': [1],
            '\'Hospital\'': [0],
            '\'Lift/Elevator\'': [1],
            '\'Scenic View\'': [0],
            '\'School\'': [1],
            '\'Shopping Centre\'': [0],
            '\'Swimming Pool\'': [1]
        }


        
        sample_data = pd.DataFrame(data)
        # Convert dictionary to DataFrame
        sample_df = pd.DataFrame(sample_data)

        # Clean up column names
        sample_df.columns = sample_df.columns.str.strip().str.replace("'", "")

        # Predict using the model
        input_data = sample_df.values.reshape(1, -1)  # Reshape to (1, num_features)
        prediction = model.predict(input_data)
        pred = prediction[0][0]

        return render_template('index.html', prediction=pred)

    return render_template('index.html')
