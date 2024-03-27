from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
import urllib


pwd = urllib.parse.quote('') # replace with your db password
engine = create_engine(f"mysql+mysqldb://root:{pwd}@localhost:3306/housePrediction")

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    location = Column(String(256), nullable=False, unique=True)

    def __repr__(self):
        return "<Location = '%s'>"  % (self.location)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

data = pd.read_csv('/home/crackygeek/Desktop/HousePrice-Predictions-Project/data/locations.csv')
data = data.dropna(subset=['Location'])


locations = set(data['Location'])

for location in locations:
    existing_loc = session.query(Location).filter_by(location=location).first()
    if existing_loc is None:
        loc_instance = Location(location=location)
        session.add(loc_instance)
session.commit()
session.close()