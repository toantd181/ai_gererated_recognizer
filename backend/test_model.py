#!/usr/bin/env python3
"""
Quick test script for the binary image classifier
Usage: python test_model.py path/to/test/image.jpg
"""

import sys
import os
from model import ImageClassifierModel

def test_model(image_path, model_path='models/my_face_classifier.pth'):
    """Test the model with a single image"""
    
    print("=" * 60)
    print("AI Image Detection - Model Test")
    print("=" * 60)
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"❌ Error: Image not found at {image_path}")
        return
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"❌ Error: Model not found at {model_path}")
        print(f"Please update MODEL_PATH in the script")
        return
    
    print(f"\n📁 Loading model from: {model_path}")
    
    try:
        # Load model
        model = ImageClassifierModel(model_path)
        print(f"✅ Model loaded successfully!")
        print(f"   Device: {model.device}")
        
        # Run prediction
        print(f"\n🖼️  Analyzing image: {image_path}")
        result = model.predict(image_path)
        
        # Display results
        print("\n" + "=" * 60)
        print("RESULTS")
        print("=" * 60)
        
        prediction = result['prediction']
        confidence = result['confidence']
        percentage = result['percentage']
        
        # Determine icon based on prediction
        if prediction == 'AI-Generated Images':
            icon = "🤖"
            color_start = "\033[95m"  # Purple
        else:
            icon = "✅"
            color_start = "\033[92m"  # Green
        
        color_end = "\033[0m"  # Reset color
        
        print(f"\n{icon} Classification: {color_start}{prediction}{color_end}")
        print(f"📊 Confidence: {color_start}{percentage}{color_end}")
        
        print(f"\n📈 Detailed Probabilities:")
        print(f"   🤖 AI-Generated: {result['details']['ai_generated_probability']:.4f} ({result['details']['ai_generated_probability']*100:.2f}%)")
        print(f"   ✅ Real Image:   {result['details']['real_image_probability']:.4f} ({result['details']['real_image_probability']*100:.2f}%)")
        
        print(f"\n💡 Raw sigmoid output: {result['raw_probability']:.4f}")
        
        # Interpretation
        print("\n" + "=" * 60)
        print("INTERPRETATION")
        print("=" * 60)
        
        if prediction == 'AI-Generated Images':
            if confidence > 0.9:
                print("⚠️  Very high confidence - Likely AI-generated")
            elif confidence > 0.7:
                print("⚠️  High confidence - Probably AI-generated")
            else:
                print("⚠️  Moderate confidence - Possibly AI-generated")
        else:
            if confidence > 0.9:
                print("✓ Very high confidence - Likely authentic")
            elif confidence > 0.7:
                print("✓ High confidence - Probably authentic")
            else:
                print("✓ Moderate confidence - Possibly authentic")
        
        print("\n" + "=" * 60)
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error during prediction: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main function"""
    
    # Default model path (update this to match your setup)
    MODEL_PATH = 'models/my_face_classifier.pth'
    
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python test_model.py <path_to_image>")
        print("\nExample:")
        print("  python test_model.py test_images/sample.jpg")
        print("\nOptional: Specify model path")
        print("  python test_model.py test_images/sample.jpg models/custom_model.pth")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Allow custom model path
    if len(sys.argv) >= 3:
        MODEL_PATH = sys.argv[2]
    
    # Run test
    test_model(image_path, MODEL_PATH)

if __name__ == "__main__":
    main()