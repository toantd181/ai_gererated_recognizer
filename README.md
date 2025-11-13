# 🤖 AI Face Detector

A full-stack web application to detect if a face image is real or AI-generated using deep learning with EfficientNet-B3.

![Accuracy](https://img.shields.io/badge/Accuracy-90.24%25-success)
![Model](https://img.shields.io/badge/Model-EfficientNet--B3-blue)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-18.2-61dafb)
![PyTorch](https://img.shields.io/badge/PyTorch-2.5-red)

## 📸 Features

- ✅ **Automatic Face Detection** - Upload any photo, system detects and crops faces automatically using MTCNN
- ✅ **High Accuracy** - 90.24% validation accuracy on 85,000+ images
- ✅ **Real-time Predictions** - Instant AI face detection results
- ✅ **Confidence Scores** - Detailed probability breakdown for each class
- ✅ **Modern UI** - Beautiful React frontend with gradient design
- ✅ **GPU Support** - Automatic CUDA acceleration when available

## 🏗️ Project Structure

```
face-recognizer/
├── backend/                    # Flask API Server
│   ├── models/                 # Model weights directory
│   │   └── ai_face_detector_final.pth
│   ├── uploads/                # Temporary upload folder (auto-created)
│   ├── app.py                  # Flask server
│   ├── model.py                # Model loader & inference
│   ├── test_model.py           # CLI test script
│   └── requirements.txt        # Python dependencies
│
├── frontend/                   # React Web Application
│   ├── public/                 # Static assets
│   ├── src/
│   │   ├── App.jsx             # Main component
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── package-lock.json
│
├── img/                        # Images for README
├── intro-ml-v1.ipynb          # Model training notebook (Kaggle)
├── intro-ml-v2.ipynb          # Model training notebook v2
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11
- Node.js 14+
- Conda (Miniconda/Anaconda)
- Your trained model: `ai_face_detector_final.pth`

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/face-recognizer.git
cd face-recognizer
```

### 2️⃣ Backend Setup

```bash
# Navigate to backend
cd backend

# Create conda environment
conda create -n face-recognizer python=3.11 -y
conda activate face-recognizer

# Install dependencies
conda install pytorch torchvision cpuonly numpy pillow -c pytorch -c conda-forge
pip install -r requirements.txt

# Copy your trained model to models folder
cp /path/to/ai_face_detector_final.pth models/
```

### 3️⃣ Frontend Setup

```bash
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install
```

### 4️⃣ Run the Application

**Terminal 1 - Start Backend:**
```bash
cd backend
conda activate face-recognizer
python app.py
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm start
```

### 5️⃣ Access the Application

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## 📦 Installation Details

### Backend Dependencies

```bash
# Core packages
flask>=3.0.0           # Web framework
flask-cors>=4.0.0      # CORS support
torch>=2.0.0           # PyTorch
torchvision>=0.15.0    # Vision utilities
timm>=0.9.0            # Model library
numpy>=1.24.0          # Numerical computing
pillow>=10.0.0         # Image processing

# Face detection (optional)
opencv-python>=4.8.0   # Computer vision
lz4>=4.0.0             # Compression
mtcnn>=0.1.1           # Face detection
tensorflow>=2.15.0     # MTCNN dependency
```

### Frontend Dependencies

```bash
react>=18.2.0          # UI framework
lucide-react>=0.294.0  # Icon library
react-scripts>=5.0.1   # Build tools
```

## ⚙️ Configuration

### Enable/Disable Face Detection

Edit `backend/app.py` line 12:

```python
# Automatic face detection (recommended)
USE_FACE_DETECTION = True

# Process full images (faster, no TensorFlow needed)
USE_FACE_DETECTION = False
```

### Change Model Path

Edit `backend/app.py` line 10:

```python
MODEL_PATH = 'models/ai_face_detector_final.pth'
```

### Change API URL

Edit `frontend/src/App.jsx` line 12:

```javascript
const API_URL = 'http://localhost:5000';
```

## 🎯 Usage

### Web Interface

1. Open http://localhost:3000
2. Check green "Server Connected" badge
3. Click upload area or drag & drop image
4. Click "Detect AI Face" button
5. View results with confidence scores

### Command Line Testing

```bash
cd backend
python test_model.py path/to/image.jpg
```

### API Endpoints

#### Health Check
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "message": "AI Face Detector is running",
  "model": "EfficientNet-B3",
  "face_detection": true
}
```

#### Predict
```bash
curl -X POST -F "file=@image.jpg" http://localhost:5000/predict
```

Response:
```json
{
  "success": true,
  "prediction": "Real",
  "confidence": 0.9234,
  "percentage": "92.34%",
  "raw_probability": 0.9234,
  "details": {
    "ai_generated_probability": 0.0766,
    "real_probability": 0.9234
  }
}
```

#### Configuration
```bash
curl http://localhost:5000/config
```

## 📊 Model Information

| Metric | Value |
|--------|-------|
| Architecture | EfficientNet-B3 |
| Input Size | 384x384 |
| Training Accuracy | 89.86% |
| Validation Accuracy | **90.24%** |
| Training Samples | ~85,000 images |
| Classes | Real Face, AI-Generated Face |
| Framework | PyTorch + timm |
| Optimizer | AdamW |
| Loss Function | BCE with Label Smoothing |

### Training Details

- **Datasets**: CIFAKE, FFHQ, UTKFace, CelebA, 140k Real/Fake Faces
- **Augmentation**: Rotation, flip, color jitter, affine transforms, random erasing
- **Training Strategy**: 
  - Stage 1: Train classification head (10 epochs)
  - Stage 2: Fine-tune entire model (40 epochs with early stopping)
- **Hardware**: Kaggle GPU (Tesla P100)
- **Training Time**: ~12 hours

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check if model file exists
ls backend/models/ai_face_detector_final.pth

# Check Python version
python --version  # Should be 3.11

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### "Server Disconnected" in frontend

```bash
# Check if backend is running
curl http://localhost:5000/health

# Restart backend
cd backend
python app.py
```

### PyTorch import error

```bash
# Reinstall PyTorch via pip
pip uninstall torch torchvision -y
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### MTCNN/TensorFlow errors

```bash
# Install TensorFlow
pip install tensorflow

# Or disable face detection in app.py
USE_FACE_DETECTION = False
```

### Frontend build errors

```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Port already in use

```bash
# Kill process on port 5000 (backend)
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Test health endpoint
curl http://localhost:5000/health

# Test with sample image
curl -X POST -F "file=@test.jpg" http://localhost:5000/predict

# CLI test
python test_model.py ../img/sample_face.jpg
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📝 Development

### Adding New Features

1. **Backend**: Edit `backend/app.py` or `backend/model.py`
2. **Frontend**: Edit `frontend/src/App.jsx`
3. **Model**: Retrain using notebooks in project root

### Code Style

- **Python**: Follow PEP 8
- **JavaScript**: ESLint + Prettier
- **Git**: Conventional Commits

## 🚢 Deployment

### Backend (Flask)

```bash
# Using Gunicorn (production)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend (React)

```bash
# Build for production
cd frontend
npm run build

# Serve static files
npx serve -s build
```

### Docker (Coming Soon)

```bash
docker-compose up
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is for educational purposes. Please respect the licenses of all datasets used for training:

- CIFAKE: [License](https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images)
- FFHQ: [License](https://github.com/NVlabs/ffhq-dataset)
- UTKFace: [License](https://susanqq.github.io/UTKFace/)
- CelebA: [License](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)

## 🙏 Acknowledgments

- **Datasets**: CIFAKE, FFHQ, UTKFace, CelebA, 140k Real/Fake Faces
- **Model**: EfficientNet-B3 via timm library
- **Face Detection**: MTCNN
- **Icons**: Lucide React
- **Training Platform**: Kaggle Notebooks

## 📧 Contact

For questions or issues:
- Open an issue on GitHub
- Check troubleshooting section above
- Test with CLI script first

---

Made with ❤️ using PyTorch, Flask, and React

**Model Performance**: 90.24% validation accuracy
**Training Time**: ~12 hours on Kaggle GPU
**Total Parameters**: ~12M (EfficientNet-B3)