import json
import time
import random
import base64
import cv2
from kafka import KafkaProducer
from tensorflow.keras.datasets import cifar10

# trainX: Contains training images from Cifar10 dataset (50000, 32, 32, 3)
# trainY: Ground truth for data set (50000, 1)
# testX: Contains test images from Cifar10 dataset (10000, 32, 32, 3)
# testY Ground truth for test images in test dataset (10000, 1)
(trainX, trainY), (testX, testY) = cifar10.load_data()
imageTypes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# Function to get a random image and its label
def get_random_image():
    i = random.randint(0, len(trainX) - 1)
    image = apply_blur(trainX[i])  # Get the image
    imageType = imageTypes[trainY[i][0]]  # Get the label
    return image, imageType

# Function to apply blurriness to the image
def apply_blur(image):
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    return blurred_image

# Connect to Kafka broker running on VM 3 (replace <VM_3_IP> with the actual IP of VM 3)
producer = KafkaProducer(bootstrap_servers="192.168.5.22:9092",
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Produce and send images
for i in range(100):

    image, label = get_random_image()

    _, buffer = cv2.imencode(".jpg", image)  # Convert to JPEG format
    imageBase64 = base64.b64encode(buffer).decode("utf-8")

    data = {
        "ID": i,
        "GroundTruth": label,
        "Data": imageBase64
    }

    # Send the data to the Kafka topic 'iot_images'
    producer.send('iot_images', value=data)
    producer.flush()
    
    print(f"Sent image {i} with label {label}")
    
    # Sleep for 1 second before sending the next image
    time.sleep(1)

# Close the producer
producer.close()
