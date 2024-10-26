from flask import Flask, request, jsonify, render_template, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import os
import tempfile
import PIL

app = Flask(__name__)

# Load the model at startup
model = load_model('trained_model.h5')  # Ensure your .h5 file path is correct

# Class labels corresponding to your model's predictions
CLASS_LABELS = ['Basalt', 'Conglomerate', 'Dolostone', 'Gabbro', 'Gneiss', 'Granite', 'Limestone', 'Marble', 'Quartzite', 'Rhyolite', 'Sandstone', 'Shale', 'Slate']

@app.route('/')
def index():
    image_url = url_for('static', filename='images/mars-plex-3e2WNfdBnK0-unsplash.jpg')
    return render_template('index.html', image_url=image_url)

# @app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded!'}), 400

    image = request.files['image']

    if not image.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return jsonify({'error': 'Invalid file format. Please upload an image.'}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            image.save(temp_file.name)
            temp_image_path = temp_file.name

            processed_image = preprocess_image(temp_image_path)
           

            predictions = model.predict(processed_image)
            print(predictions)
            # Check the shape of predictions
            print(f"Predictions shape: {predictions.shape}")

            if predictions.size == 0:
                return jsonify({'error': 'No predictions made.'}), 500

            predicted_class = CLASS_LABELS[np.argmax(predictions[0])]
            print(f"Predicted class: {predicted_class}")

        return jsonify({'predicted_class': predicted_class})

    except Exception as e:
        print(f"Error during prediction: {str(e)}")  # Log the error for debugging
        return jsonify({'error': str(e)}), 500

    finally:
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)



def preprocess_image(image_path):
    """
    Preprocess the image to match the input format required by the model.
    Modify as needed based on your model input (e.g., size, normalization).
    """
    img = load_img(image_path, target_size=(64, 64))  # Adjust target size if needed
    img_array = img_to_array(img)   # Normalize to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

if __name__ == '__main__':
    app.run(debug=True)
