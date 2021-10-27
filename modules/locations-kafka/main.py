from kafka import KafkaConsumer
from json import loads
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_Point
from datetime import datetime
import os


DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

#Database connection
db = create_engine(SQLALCHEMY_DATABASE_URI)
base = declarative_base()

class Location(base):  
    __tablename__ = 'location'

    id = Column(BigInteger, primary_key=True)
    person_id = Column(Integer)
    coordinate = Column(Geometry("POINT"))
    creation_time = Column(DateTime)

Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)

#Kafka Parameters
TOPIC_NAME = 'udaconnect-locations'
KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9092'

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER, auto_offset_reset='latest', value_deserializer=lambda x: loads(x.decode('utf-8')))
while True:
    for message in consumer:
        location = message.value
        new_location = Location(person_id=location["person_id"], 
                            coordinate=ST_Point(location["latitude"], location["longitude"]),
                            creation_time=location["creation_time"])

        session.add(new_location)  
        session.commit()
        print('{}'.format(new_location))
