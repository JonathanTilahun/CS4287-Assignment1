import requests
import base64

# Read and convert image to base64
with open('test_image.jpg', 'rb') as img_file:
    img_str = base64.b64encode(img_file.read()).decode('utf-8')

# Send the image to Flask API for inference
response = requests.post('http://127.0.0.1:5000/infer', json={'image': img_str})

# Print the result
print(response.json())

