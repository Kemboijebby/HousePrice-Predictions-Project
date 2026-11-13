# Nairobi Metropolitan House Price Prediction

A small end-to-end machine-learning application for estimating a Nairobi property price from user-selected property attributes and location. The repository includes model-training notebooks, a serialized model, a Flask application, a web interface, and SQL for the MySQL locations lookup table.

## Application flow

```text
User inputs (location, bedrooms, bathrooms, amenities)
        |
        v
Flask application ----> MySQL locations lookup
        |
        v
Feature vector aligned to training columns
        |
        v
Serialized model (model.pkl)
        |
        v
Predicted property price displayed in UI
```

## Repository components

- `Buyrentke_model.ipynb` and `model.ipynb` — model exploration/training notebooks.
- `Backend/model.pkl` — serialized model artifact.
- `Backend/app.py` — Flask prediction route and feature-vector construction.
- `Backend/data/dataset_columns.csv` — feature-column reference used by inference.
- `Backend/data/locations.csv` and `housePrediction.sql` — location lookup setup.
- `Backend/templates/` and `Backend/static/` — application interface assets.
- `AppFrontend/` — separate frontend prototype assets.

## Technology

Python · pandas · NumPy · scikit-learn model artifact · Flask · Flask-SQLAlchemy · MySQL · HTML/CSS/JavaScript

## Local configuration

Set the MySQL connection variables before starting the backend:

```powershell
$env:MYSQL_USER = "your_mysql_user"
$env:MYSQL_PASSWORD = "your_mysql_password"
$env:MYSQL_HOST = "localhost"
$env:MYSQL_PORT = "3306"
$env:MYSQL_DATABASE = "housePrediction"
```

Run `housePrediction.sql` in MySQL to create the lookup database and table. The setup script creates the database if it does not exist; it no longer drops an existing database.

From the `Backend/` directory, install the application dependencies and run:

```bash
python app.py
```

Use package versions compatible with the serialized model in `model.pkl`; scikit-learn model serialization can be version-sensitive.

## Portability and safety improvements

- Replaced the machine-specific absolute path in the prediction route with a path relative to the backend directory.
- Load the model relative to the backend directory.
- Read MySQL credentials from environment variables rather than embedding them in source code.
- Removed the destructive database-drop statement from the SQL setup script.

## Known limitations

- The repository does not document a reproducible model evaluation report or validated accuracy/error metric. No performance score is claimed here.
- The inference route expects location names to exist in the MySQL lookup table.
- Model input order and preprocessing must remain consistent with the training notebook and serialized model.
- This is a portfolio prototype, not a production deployment. Add input validation, model/version metadata, automated tests, logging, and deployment security before production use.

## Next steps

1. Document dataset sources, target definition, and cleaning decisions.
2. Re-run training and report baseline and holdout metrics (MAE, RMSE, and R² where appropriate).
3. Record the Python and scikit-learn versions used to train the model.
4. Add tests for feature construction and prediction inputs.
5. Provide a reproducible environment and screenshots of the working application.
