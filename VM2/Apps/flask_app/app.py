from flask import Flask, request, jsonify
from keras.applications import ResNet50
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.preprocessing import image
import numpy as np
import base64
from PIL import Image
import io

app = Flask(__name__)

# Load the pre-trained ResNet50 model
model = ResNet50(weights='imagenet')

def preprocess_image(img):
    """ Preprocess the image for ResNet50 """
    img = img.resize((224, 224))  # ResNet50 expects images of this size
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

@app.route('/', methods=['POST'])
def infer():
    try:
        # Ensure the request has JSON data
        if not request.is_json:
            return jsonify({'error': 'Invalid input. Expected JSON data.'}), 400

        data = request.get_json()

        # Ensure the image field is present
        if 'image' not in data:
            return jsonify({'error': 'No image data provided.'}), 400

        # Decode the image from base64
        img_data = base64.b64decode(data['image'])
        img = Image.open(io.BytesIO(img_data))

        # Preprocess the image and make prediction
        processed_img = preprocess_image(img)
        preds = model.predict(processed_img)

        # Decode the predictions into readable labels
        decoded_preds = decode_predictions(preds, top=1)[0][0]
        inferred_value = decoded_preds[1]  # Get the name of the predicted class

        return jsonify({'inferred': inferred_value})

    except Exception as e:
        # Catch any errors and return a detailed message
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
