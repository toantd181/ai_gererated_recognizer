# AI Image Detector

A full-stack web application that detects whether an image is real or AI-generated using a ResNet50 deep learning model.

## 🎯 Features

- Upload images (PNG, JPG, JPEG)
- Real-time AI detection
- Confidence scores and detailed probabilities
- Beautiful gradient UI with animations
- Error handling and validation
- Responsive design

## 🏗️ Project Structure
```
face-recognizer/
├── backend/                    # Flask Backend
│   ├── app.py                 # Main Flask application
│   ├── model.py               # AI model integration
│   ├── requirements.txt       # Python dependencies
│   ├── models/
│   │   └── my_face_classifier.pth  # Trained ResNet50 model
│   └── uploads/               # Temporary upload folder
│
└── frontend/                   # React Frontend
    ├── public/
    ├── src/
    │   ├── App.jsx            # Main React component
    │   ├── index.js           # Entry point
    │   └── index.css          # Global styles
    ├── package.json           # Node dependencies
    └── package-lock.json
```

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- pip
- npm

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Verify model file exists
ls models/my_face_classifier.pth

# Start Flask server
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start development server
npm start
```

Frontend will open at `http://localhost:3000`

## 📦 Dependencies

### Backend (Python)

- Flask 3.0.0 - Web framework
- flask-cors 4.0.0 - CORS support
- torch >=2.0.0 - PyTorch deep learning
- torchvision >=0.15.0 - Image transformations
- Pillow >=10.0.0 - Image processing
- numpy >=1.24.0 - Numerical computing

### Frontend (JavaScript/React)

- react 18.2.0 - UI framework
- react-dom 18.2.0 - React DOM rendering
- react-scripts 5.0.1 - Build tooling
- lucide-react 0.263.1 - Icon library

## 🎓 Model Information

- **Architecture**: ResNet50 (Transfer Learning)
- **Task**: Binary Classification
- **Classes**: 
  - AI-Generated Images (Class 0)
  - Real Images (Class 1)
- **Input Size**: 256x256 RGB
- **Output**: Sigmoid activation with 0.5 threshold
- **Training**: BCEWithLogitsLoss, Adam optimizer

## 🔧 Configuration

### Backend Configuration

Edit `backend/app.py`:
```python
MODEL_PATH = 'path/to/your/model.pth'  # Update model path
UPLOAD_FOLDER = 'uploads'              # Temp upload folder
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max 16MB
```

### Frontend Configuration

Edit `frontend/src/App.jsx`:
```javascript
const API_URL = 'http://localhost:5000';  // Backend URL
```

## 🧪 Testing

### Test Backend API
```bash
# Health check
curl http://localhost:5000/health

# Should return: {"status":"healthy","message":"Server is running"}
```

### Test Model Prediction

Create `test_model.py`:
```python
from model import ImageClassifierModel

model = ImageClassifierModel('models/my_face_classifier.pth')
result = model.predict('test_image.jpg')
print(result)
```

## 📊 API Endpoints

### GET /health

Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "message": "Server is running"
}
```

### POST /predict

Upload image for prediction

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (image file)

**Response:**
```json
{
  "success": true,
  "prediction": "Real Images",
  "confidence": 0.9523,
  "percentage": "95.23%",
  "raw_probability": 0.9523,
  "details": {
    "ai_generated_probability": 0.0477,
    "real_image_probability": 0.9523
  }
}
```

## 🚨 Troubleshooting

### Backend Issues

**Model not loading:**
- Verify model path is correct
- Check model file exists and is not corrupted
- Ensure PyTorch is installed correctly

**CORS errors:**
- Verify flask-cors is installed
- Check CORS is enabled in app.py

### Frontend Issues

**Blank page:**
- Check browser console (F12) for errors
- Verify all dependencies are installed
- Clear cache: `rm -rf node_modules && npm install`

**Can't connect to backend:**
- Ensure backend is running on port 5000
- Check API_URL in App.jsx
- Verify no firewall blocking

## 🎨 UI Features

- **Upload Area**: Drag-and-drop image preview
- **Loading State**: Animated spinner during analysis
- **Results Display**: 
  - Purple theme for AI-generated images
  - Green theme for real images
  - Confidence progress bar
  - Detailed probability breakdown
- **Error Handling**: User-friendly error messages

## 📈 Performance

- **Cold Start**: ~3-5 seconds (model loading)
- **Inference Time**: ~0.5-2 seconds per image
- **Memory Usage**: ~500MB-1GB RAM
- **Max Upload Size**: 16MB

## 🔐 Security

- File type validation (PNG, JPG, JPEG only)
- File size limits (16MB max)
- Temporary file cleanup after processing
- CORS configured for local development

## 🚀 Deployment

### Backend Deployment

For production, use gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend Deployment

Build production version:
```bash
npm run build
```

Deploy `build/` folder to:
- Netlify
- Vercel
- AWS S3 + CloudFront
- GitHub Pages

## 📝 License

MIT License

## 👨‍💻 Author

@toantd181 + Google Gemini + Claude AI + ChatGPT

## 🙏 Acknowledgments

- ResNet50 architecture by Microsoft Research
- Flask framework
- React library
- PyTorch deep learning framework
