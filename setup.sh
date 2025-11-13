#!/bin/bash

# ============================================
# AI Face Detector - Setup Script
# ============================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_header() {
    echo ""
    echo "======================================================================"
    echo "$1"
    echo "======================================================================"
    echo ""
}

# Check if conda is installed
check_conda() {
    if ! command -v conda &> /dev/null; then
        print_error "Conda is not installed. Please install Miniconda or Anaconda first."
        echo "Visit: https://docs.conda.io/en/latest/miniconda.html"
        exit 1
    fi
    print_success "Conda found: $(conda --version)"
}

# Check if node is installed
check_node() {
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js first."
        echo "Visit: https://nodejs.org/"
        exit 1
    fi
    print_success "Node.js found: $(node --version)"
}

# Setup backend
setup_backend() {
    print_header "SETTING UP BACKEND"
    
    cd backend
    
    # Check if conda environment exists
    if conda env list | grep -q "face-recognizer"; then
        print_warning "Conda environment 'face-recognizer' already exists."
        read -p "Remove and recreate? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Removing existing environment..."
            conda deactivate 2>/dev/null || true
            conda env remove -n face-recognizer -y
        else
            print_info "Using existing environment..."
        fi
    fi
    
    # Create conda environment
    if ! conda env list | grep -q "face-recognizer"; then
        print_info "Creating conda environment..."
        conda create -n face-recognizer python=3.11 -y
        print_success "Conda environment created"
    fi
    
    # Activate environment
    print_info "Activating environment..."
    eval "$(conda shell.bash hook)"
    conda activate face-recognizer
    
    # Install PyTorch
    print_info "Installing PyTorch..."
    conda install pytorch torchvision cpuonly numpy pillow -c pytorch -c conda-forge -y
    
    # Install pip packages
    print_info "Installing Python packages..."
    pip install -r requirements.txt
    
    # Check for model file
    if [ ! -f "models/ai_face_detector_final.pth" ]; then
        print_warning "Model file not found: models/ai_face_detector_final.pth"
        print_info "Please copy your trained model to backend/models/"
        echo ""
        read -p "Enter path to your model file (or press Enter to skip): " MODEL_PATH
        if [ ! -z "$MODEL_PATH" ] && [ -f "$MODEL_PATH" ]; then
            mkdir -p models
            cp "$MODEL_PATH" models/ai_face_detector_final.pth
            print_success "Model copied successfully"
        else
            print_warning "Skipping model copy. Remember to add it later!"
        fi
    else
        print_success "Model file found"
    fi
    
    cd ..
    print_success "Backend setup complete!"
}

# Setup frontend
setup_frontend() {
    print_header "SETTING UP FRONTEND"
    
    cd frontend
    
    # Check if node_modules exists
    if [ -d "node_modules" ]; then
        print_warning "node_modules already exists"
        read -p "Remove and reinstall? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Removing node_modules..."
            rm -rf node_modules package-lock.json
        fi
    fi
    
    # Install dependencies
    print_info "Installing Node.js packages..."
    npm install
    
    # Install lucide-react if not in package.json
    if ! grep -q "lucide-react" package.json; then
        print_info "Installing lucide-react..."
        npm install lucide-react
    fi
    
    cd ..
    print_success "Frontend setup complete!"
}

# Create necessary directories
create_directories() {
    print_header "CREATING DIRECTORIES"
    
    mkdir -p backend/models
    mkdir -p backend/uploads
    touch backend/models/.gitkeep
    touch backend/uploads/.gitkeep
    
    print_success "Directories created"
}

# Test backend
test_backend() {
    print_header "TESTING BACKEND"
    
    cd backend
    eval "$(conda shell.bash hook)"
    conda activate face-recognizer
    
    print_info "Testing Python imports..."
    python -c "import torch; print(f'✓ PyTorch {torch.__version__}')" || print_error "PyTorch import failed"
    python -c "import timm; print('✓ timm imported')" || print_error "timm import failed"
    python -c "import flask; print('✓ Flask imported')" || print_error "Flask import failed"
    
    if [ -f "models/ai_face_detector_final.pth" ]; then
        print_info "Testing model loading..."
        python -c "from model import load_model; load_model('models/ai_face_detector_final.pth'); print('✓ Model loaded')" || print_warning "Model loading failed"
    else
        print_warning "Skipping model test (model file not found)"
    fi
    
    cd ..
    print_success "Backend tests completed"
}

# Print instructions
print_instructions() {
    print_header "SETUP COMPLETE!"
    
    echo "Next steps:"
    echo ""
    echo "1. Start Backend (Terminal 1):"
    echo "   ${GREEN}cd backend${NC}"
    echo "   ${GREEN}conda activate face-recognizer${NC}"
    echo "   ${GREEN}python app.py${NC}"
    echo ""
    echo "2. Start Frontend (Terminal 2):"
    echo "   ${GREEN}cd frontend${NC}"
    echo "   ${GREEN}npm start${NC}"
    echo ""
    echo "3. Open browser:"
    echo "   ${GREEN}http://localhost:3000${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "   • Backend logs: Check terminal 1"
    echo "   • Frontend logs: Check terminal 2"
    echo "   • API test: ${YELLOW}curl http://localhost:5000/health${NC}"
    echo ""
}

# Main execution
main() {
    print_header "AI FACE DETECTOR - SETUP SCRIPT"
    
    # Checks
    check_conda
    check_node
    
    # Setup
    create_directories
    setup_backend
    setup_frontend
    
    # Test
    test_backend
    
    # Instructions
    print_instructions
    
    print_success "All done! 🎉"
}

# Run main function
main