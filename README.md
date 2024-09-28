# **CS4287-Assignment1: IoT Data Analytics Pipeline**

## **Overview**

This project implements a cloud-based data pipeline using virtual machines (VMs) on Chameleon Cloud. The scenario emulates an IoT application where surveillance cameras send data to Kafka brokers, which are then processed by machine learning (ML) models and stored in a database. The system consists of producers, consumers, a Kafka broker, a MongoDB database, and an ML inference server.

### **Technologies Used**

* **Apache Kafka**: For streaming and managing the message queue between the producer (IoT devices) and consumers.  
* **MongoDB**: Used for storing the processed image data along with metadata.  
* **Python**: Main programming language, including libraries like `kafka-python`, `pymongo`, and `Flask` for different components.  
* **Flask**: Hosting the machine learning inference model (ResNet50).  
* **TensorFlow**: Used for loading the pre-trained ResNet50 ML model.  
* **Chameleon Cloud**: Cloud platform where we deployed four virtual machines to distribute the different components of the pipeline.

## **Project Architecture**

The project is divided across four VMs:

1. **VM1**: IoT Producer  
2. **VM2**: ML Model (ResNet50) Inference Server  
3. **VM3**: Kafka Broker & Consumers  
4. **VM4**: MongoDB Database

### **VM1: IoT Producer**

* **Role**: Simulates IoT camera devices sending images to Kafka.  
* **Details**:  
  * Python script generates synthetic image data using CIFAR-10.  
  * The data is serialized as JSON and sent to Kafka via the `kafka-python` library.  
  * The message includes an `image_id`, `device_id`, `timestamp`, and a placeholder for the image data (in a real-world setting, this would be an actual image).

### **VM2: ML Inference Server**

* **Role**: Hosts the ResNet50 model using Flask and Gunicorn to perform real-time image inference.  
* **Details**:  
  * Flask API exposes an endpoint that accepts base64-encoded image data and returns a classification label.  
  * The ML model is pre-trained on CIFAR-10 using TensorFlow's ResNet50 architecture.  
  * Flask is deployed in a production environment using Gunicorn with multiple workers for handling concurrent requests.  
  * Flask receives the image from Kafka, runs inference, and returns the predicted class.

### **VM3: Kafka Broker & Consumers**

* **Role**: Hosts the Kafka broker, which is responsible for managing the data pipeline between the IoT producer and the consumers.  
* **Details**:  
  * Kafka Broker version `2.13-3.8.0` is installed and configured.  
  * **Consumers**:  
    1. **DB Consumer**: Consumes the image data and stores it in MongoDB (hosted on VM4).  
    2. **Inference Consumer**: Sends the image data to the Flask API hosted on VM2 for inference, then updates MongoDB with the predicted label.

### **VM4: MongoDB Database**

* **Role**: Stores all incoming data from Kafka, including image metadata and inference results.  
* **Details**:  
  * MongoDB stores data such as the `image_id`, `device_id`, `timestamp`, and the prediction label.  
  * The DB Consumer (on VM3) inserts the image metadata, and the Inference Consumer (on VM3) updates MongoDB with the inference label.

## **Installation & Setup**

### **Prerequisites**

* Ensure you have a Chameleon Cloud account and have created 4 VMs (VM1-VM4) using Ubuntu 22.04.  
* Install Python 3 on each VM.

### **Step-by-Step Setup**

#### **VM1: IoT Producer**

Install Kafka Python Client:  
`pip install kafka-python`

Run the IoT Producer:  
`python iot_producer.py`

#### **VM2: ML Inference Server**

Install the necessary Python libraries:  
`pip install flask tensorflow gunicorn`

Run the Flask app with Gunicorn:  
`gunicorn --workers 4 app:app`


#### **VM3: Kafka Broker & Consumers**

Install Kafka and Python dependencies:  
`tar -xvf kafka_2.13-3.8.0.tgz`  
`cd kafka_2.13-3.8.0`

Start Kafka broker:  
`bin/kafka-server-start.sh config/server.properties`

Run the consumers:  
`python kafka_to_mongo_consumer.py`  
`python kafka_to_ml_consumer.py`

#### **VM4: MongoDB**

Install MongoDB:  
`sudo apt update`  
`sudo apt install -y mongodb`. 

Start MongoDB:  
`sudo systemctl start mongodb`


## **How the System Works**

1. **IoT Producer (VM1)** generates synthetic image data and sends it to the Kafka broker (VM3).  
2. **Kafka Broker (VM3)** stores the messages and distributes them to two consumers: the DB Consumer and the Inference Consumer.  
3. The **DB Consumer (VM3)** inserts the image metadata into **MongoDB (VM4)**.  
4. The **Inference Consumer (VM3)** sends the image to the **ML Inference Server (VM2)**.  
5. The **ML Inference Server (VM2)** processes the image and sends back the inferred label to **Kafka (VM3)**, which then updates **MongoDB (VM4)** with the predicted label.

## **Project Structure**

`Project1Repo/`  
`│`  
`├── VM3/                   # All files related to Kafka Broker and Consumers (VM3)`  
`│   ├── Apps/              # Kafka binaries and dependencies`  
`│   ├── Consumers/         # Consumer scripts for MongoDB and ML Inference`  
`│   └── kafka_to_mongo_consumer.py  # Kafka to MongoDB consumer script`  
`│   └── kafka_to_ml_consumer.py     # Kafka to ML Inference consumer script`  
`├── VM4/                   # All files related to MongoDB (VM4)`  
`│   ├── MongoDB/           # MongoDB setup and configuration files`  
`│   └── iot_images_collection/ # MongoDB collections for IoT data`  
`└── README.md              # Project description and setup guide (this file)`  

