from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# MongoDB connection setup (ensure this IP is correct)
mongo_client = MongoClient("mongodb://192.168.5.206:27017/")
mongo_db = mongo_client["kafkaDatabase"]  # Database name
mongo_collection = mongo_db["iot_images_collection"]  # Collection name

# Kafka consumer setup
consumer = KafkaConsumer(
    'iot_images',  # Kafka topic
    bootstrap_servers=['192.168.5.22:9092'],  # Kafka broker on VM3
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Consume messages from Kafka and insert into MongoDB
for message in consumer:
    print(f"Consumed message: {message.value}")  # Debug message to confirm
    
    try:
        mongo_collection.insert_one(message.value)  # Insert into MongoDB
        print(f"Inserted into MongoDB: {message.value}")
    except Exception as e:
        print(f"Error inserting into MongoDB: {e}")  # Catch any insertion error
