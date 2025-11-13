# app.py - Flask Backend Server for AI Face Detector
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from model import load_model, get_prediction

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
MODEL_PATH = 'models/ai_face_detector_final.pth'  # UPDATE THIS PATH!
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
USE_FACE_DETECTION = True  # Set to False to process full images

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model at startup
print("=" * 70)
print(" AI FACE DETECTOR - Starting Server ".center(70, "="))
print("=" * 70)
print(f"Model path: {MODEL_PATH}")
print(f"Face detection: {'Enabled' if USE_FACE_DETECTION else 'Disabled'}")
print(f"Upload folder: {UPLOAD_FOLDER}")
print("-" * 70)

try:
    model = load_model(MODEL_PATH, use_face_detection=USE_FACE_DETECTION)
    print("=" * 70)
    print("✓ Server ready to accept requests!".center(70))
    print("=" * 70)
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("Please check the MODEL_PATH in app.py")
    exit(1)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'message': 'AI Face Detector is running',
        'model': 'EfficientNet-B3',
        'face_detection': USE_FACE_DETECTION
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint for AI face detection prediction"""
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({
            'success': False, 
            'error': 'Invalid file type. Only PNG, JPG, JPEG allowed'
        }), 400
    
    filename = None
    try:
        # Save file temporarily
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        print(f"Processing: {file.filename}")
        
        # Get model prediction
        result = get_prediction(filename)
        
        if result.get('success', False):
            print(f"  ✓ Prediction: {result['prediction']} ({result['percentage']})")
        else:
            print(f"  ✗ Prediction failed: {result.get('error', 'Unknown error')}")
        
        # Clean up uploaded file
        if os.path.exists(filename):
            os.remove(filename)
        
        return jsonify(result), 200 if result.get('success', False) else 500
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        import traceback
        traceback.print_exc()
        
        # Clean up file if it exists
        if filename and os.path.exists(filename):
            os.remove(filename)
        
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/config', methods=['GET'])
def get_config():
    """Get server configuration"""
    return jsonify({
        'model_type': 'EfficientNet-B3',
        'input_size': '384x384',
        'classes': ['AI-Generated', 'Real'],
        'face_detection_enabled': USE_FACE_DETECTION,
        'max_file_size_mb': 16
    }), 200

if __name__ == '__main__':
    print("\n🚀 Starting Flask server...")
    print("📍 Access at: http://localhost:5000")
    print("📍 Health check: http://localhost:5000/health")
    print("\n⚠️  Make sure React frontend is running on http://localhost:3000")
    print("-" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)