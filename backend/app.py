# app.py - Flask Backend Server
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from model import load_model, get_prediction

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load model at startup
MODEL_PATH = '/home/toantd/my-folder/hoc/intro-ml/face-recognizer/backend/model/my_face_classifier.pth'  # Update this path
# NUM_CLASSES = 1  # Update with your number of classes
model = load_model(MODEL_PATH)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Server is running'}), 200

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint for image classification prediction"""
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG allowed'}), 400
    
    try:
        # Save file temporarily
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Get model prediction (FIXED - No more TODO!)
        result = get_prediction(filename)
        
        print("Prediction result:", result)
        
        # Clean up uploaded file
        os.remove(filename)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        # Clean up file if it exists
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)