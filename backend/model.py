# model.py - Binary Image Classifier (Real vs AI-Generated)
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

class ImageClassifierModel:
    def __init__(self, model_path, device=None):
        """
        Initialize the binary image classifier
        
        Args:
            model_path: Path to the saved model weights (.pt or .pth)
            device: torch device (cuda/cpu)
        """
        self.device = device if device else torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load ResNet50 model (matching your training setup)
        self.model = models.resnet50(weights=None)  # Updated API
        
        # Modify the final layer for binary classification (1 output)
        num_features = self.model.fc.in_features
        self.model.fc = nn.Linear(num_features, 1)
        
        # Load trained weights
        checkpoint = torch.load(model_path, map_location=self.device)
        
        # Handle different save formats
        if isinstance(checkpoint, dict):
            if 'state_dict' in checkpoint:
                self.model.load_state_dict(checkpoint['state_dict'])
            elif 'model_state_dict' in checkpoint:
                self.model.load_state_dict(checkpoint['model_state_dict'])
            else:
                self.model.load_state_dict(checkpoint)
        else:
            self.model.load_state_dict(checkpoint)
        
        self.model.to(self.device)
        self.model.eval()
        
        # Define image preprocessing (matching your training transforms)
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
        
        # Class names based on your training
        self.class_names = ['AI-Generated Images', 'Real Images']
    
    def preprocess_image(self, image_path):
        """Preprocess image for model input"""
        img = Image.open(image_path).convert('RGB')
        img_tensor = self.transform(img)
        img_tensor = img_tensor.unsqueeze(0)  # Add batch dimension
        return img_tensor.to(self.device)
    
    def predict(self, image_path):
        """
        Predict if image is real or AI-generated
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with prediction and confidence score
        """
        with torch.no_grad():
            # Preprocess image
            img_tensor = self.preprocess_image(image_path)
            
            # Get model output
            output = self.model(img_tensor)
            
            # Apply sigmoid to get probability
            probability = torch.sigmoid(output).item()
            
            # Convert to prediction (threshold at 0.5)
            prediction = 1 if probability > 0.5 else 0
            predicted_class = self.class_names[prediction]
            
            # Calculate confidence
            # If probability > 0.5, confidence is probability itself
            # If probability < 0.5, confidence is (1 - probability)
            confidence = probability if prediction == 1 else (1 - probability)
            
            return {
                'success': True,
                'prediction': predicted_class,
                'confidence': float(confidence),
                'percentage': f"{float(confidence) * 100:.2f}%",
                'raw_probability': float(probability),
                'details': {
                    'ai_generated_probability': float(1 - probability),
                    'real_image_probability': float(probability)
                }
            }

# Global model instance
model_instance = None

def load_model(model_path):
    """Load model once when server starts"""
    global model_instance
    if model_instance is None:
        model_instance = ImageClassifierModel(model_path)
    return model_instance

def get_prediction(image_path):
    """Get prediction from loaded model"""
    if model_instance is None:
        raise Exception("Model not loaded. Call load_model() first.")
    return model_instance.predict(image_path)