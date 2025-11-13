import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import timm
import cv2
import numpy as np
from mtcnn import MTCNN

class AIFaceDetectorModel:
    def __init__(self, model_path, device=None, use_face_detection=True):
        """
        Initialize the AI face detector
        
        Args:
            model_path: Path to the saved model weights (.pth)
            device: torch device (cuda/cpu)
            use_face_detection: Whether to detect and crop faces before classification
        """
        self.device = device if device else torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.use_face_detection = use_face_detection
        
        # Initialize face detector if needed
        if self.use_face_detection:
            try:
                self.face_detector = MTCNN()
                print("✓ Face detector initialized")
            except Exception as e:
                print(f"⚠️ Could not initialize face detector: {e}")
                print("   Will process full images instead")
                self.use_face_detection = False
        
        # Load EfficientNet-B3 model (matching your training setup)
        print("Loading EfficientNet-B3 model...")
        self.model = timm.create_model('efficientnet_b3', pretrained=False, num_classes=1)
        
        # Load trained weights
        checkpoint = torch.load(model_path, map_location=self.device, weights_only=False)
        
        # Handle different checkpoint formats
        if isinstance(checkpoint, dict):
            if 'model_state_dict' in checkpoint:
                self.model.load_state_dict(checkpoint['model_state_dict'])
                print(f"✓ Model loaded from checkpoint (epoch {checkpoint.get('epoch', 'unknown')})")
            elif 'state_dict' in checkpoint:
                self.model.load_state_dict(checkpoint['state_dict'])
            else:
                self.model.load_state_dict(checkpoint)
        else:
            self.model.load_state_dict(checkpoint)
        
        self.model.to(self.device)
        self.model.eval()
        print(f"✓ Model loaded successfully on {self.device}")
        
        # Define image preprocessing (matching your training transforms)
        # Image size: 384x384 (from Config.IMG_SIZE)
        self.transform = transforms.Compose([
            transforms.Resize((384, 384)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        # Class names based on your ImageFolder structure
        # ImageFolder sorts alphabetically: ai_generated (0), real (1)
        self.class_names = ['AI-Generated', 'Real']
    
    def detect_and_crop_face(self, image_path):
        """
        Detect and crop the largest face in the image
        
        Args:
            image_path: Path to image file
            
        Returns:
            PIL Image of cropped face, or original image if no face detected
        """
        if not self.use_face_detection:
            return Image.open(image_path).convert('RGB')
        
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                return Image.open(image_path).convert('RGB')
            
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            faces = self.face_detector.detect_faces(img_rgb)
            
            if not faces:
                print("⚠️ No face detected, using full image")
                return Image.open(image_path).convert('RGB')
            
            # Get the largest face
            largest_face = max(faces, key=lambda f: f['box'][2] * f['box'][3])
            x, y, w, h = largest_face['box']
            
            # Add padding (20%)
            padding = int(max(w, h) * 0.2)
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = w + 2 * padding
            h = h + 2 * padding
            
            # Ensure we don't go out of bounds
            x2 = min(img_rgb.shape[1], x + w)
            y2 = min(img_rgb.shape[0], y + h)
            
            # Crop face
            face_img = img_rgb[y:y2, x:x2]
            
            print(f"✓ Face detected and cropped: {w}x{h}")
            return Image.fromarray(face_img)
            
        except Exception as e:
            print(f"⚠️ Error during face detection: {e}")
            print("   Using full image instead")
            return Image.open(image_path).convert('RGB')
    
    def preprocess_image(self, image_path):
        """Preprocess image for model input"""
        # Detect and crop face (or use full image)
        img = self.detect_and_crop_face(image_path)
        
        # Apply transforms
        img_tensor = self.transform(img)
        img_tensor = img_tensor.unsqueeze(0)  # Add batch dimension
        return img_tensor.to(self.device)
    
    def predict(self, image_path):
        """
        Predict if face image is real or AI-generated
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with prediction and confidence score
        """
        try:
            with torch.no_grad():
                # Preprocess image
                img_tensor = self.preprocess_image(image_path)
                
                # Get model output (logit)
                output = self.model(img_tensor)
                
                # Apply sigmoid to get probability
                # probability represents P(real)
                probability = torch.sigmoid(output).item()
                
                # Determine prediction based on threshold
                # If probability > 0.5: Real (class 1)
                # If probability <= 0.5: AI-Generated (class 0)
                prediction_idx = 1 if probability > 0.5 else 0
                predicted_class = self.class_names[prediction_idx]
                
                # Calculate confidence (distance from decision boundary)
                confidence = probability if prediction_idx == 1 else (1 - probability)
                
                return {
                    'success': True,
                    'prediction': predicted_class,
                    'confidence': float(confidence),
                    'percentage': f"{float(confidence) * 100:.2f}%",
                    'raw_probability': float(probability),
                    'details': {
                        'ai_generated_probability': float(1 - probability),
                        'real_probability': float(probability)
                    }
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'prediction': None,
                'confidence': 0.0
            }

# Global model instance
model_instance = None

def load_model(model_path, use_face_detection=True):
    """
    Load model once when server starts
    
    Args:
        model_path: Path to model weights
        use_face_detection: Whether to enable face detection
    """
    global model_instance
    if model_instance is None:
        model_instance = AIFaceDetectorModel(model_path, use_face_detection=use_face_detection)
    return model_instance

def get_prediction(image_path):
    """Get prediction from loaded model"""
    if model_instance is None:
        raise Exception("Model not loaded. Call load_model() first.")
    return model_instance.predict(image_path)