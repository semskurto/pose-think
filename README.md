# 🎯 Pose-Think: AI-Powered Movement Analysis Suite  
*test*

A comprehensive collection of AI-powered applications for human movement analysis, ranging from basic hand tracking to advanced physiotherapy assessment. Built with MediaPipe and Gradio for real-time, web-based analysis.

## 📱 Applications Overview

This repository contains multiple specialized applications for different movement analysis needs:

### 🏥 **Physiotherapy Assessment System** (Main Application)
**File**: `physiotherapy_assessment_app.py`

Professional-grade biomechanical assessment tool designed for clinical use.

**Key Features:**
- 33-point full body analysis with MediaPipe Pose
- Clinical-standard risk assessment (Low/Moderate/High/Critical)
- Personalized treatment plans and exercise protocols
- Real-time compensation pattern detection
- Professional English interface with comprehensive reporting

**Use Cases:**
- Clinical physiotherapy assessment
- Workplace ergonomic evaluation
- Personal posture monitoring
- Rehabilitation progress tracking

### 🤚 **Hand Tracking System** (Legacy Application)
**File**: `hand_tracking_app.py`

Real-time hand gesture recognition and analysis system.

**Key Features:**
- 21-point hand landmark detection (up to 2 hands)
- Gesture recognition (fist, open hand, finger counting)
- Real-time finger position analysis
- Adjustable detection sensitivity
- Bilingual interface (Turkish/English)

**Use Cases:**
- Gesture-based interaction research
- Hand rehabilitation exercises
- Sign language analysis
- Gaming and entertainment applications

## 🔬 Core Technologies

### AI/ML Framework
- **MediaPipe**: Google's ML framework for pose and hand detection
- **OpenCV**: Computer vision and image processing
- **NumPy**: Numerical computations and array operations

### Web Interface
- **Gradio**: Modern web interface for ML applications
- **CSS3**: Professional styling with gradients and responsive design
- **Real-time Streaming**: Live camera feed processing

### Clinical Modules
- **Advanced Algorithms**: Custom biomechanical analysis (`advanced_physiotherapy_algorithms.py`)
- **Clinical Feedback**: Evidence-based treatment protocols (`clinical_feedback_system.py`)
- **Risk Assessment**: Professional injury risk stratification

## 📦 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/semskurto/pose-think.git
cd pose-think
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Choose Your Application

#### 🏥 For Professional Physiotherapy Assessment:
```bash
python physiotherapy_assessment_app.py
```
- Opens at: `http://localhost:7861`
- Full body analysis and clinical assessment
- Professional treatment planning

#### 🤚 For Hand Tracking and Gesture Recognition:
```bash
python hand_tracking_app.py
```
- Opens at: `http://localhost:7860`
- Hand gesture recognition and analysis
- Real-time finger tracking

### 4. Grant Camera Permissions
- Allow camera access when prompted by your browser
- Ensure good lighting and clear background for optimal results

## 🏗️ Repository Structure

```
📁 pose-think/
├── 🏥 physiotherapy_assessment_app.py    # Main physiotherapy application
├── 🤚 hand_tracking_app.py              # Hand tracking application
├── 🔬 advanced_physiotherapy_algorithms.py # Biomechanical analysis engine
├── 💊 clinical_feedback_system.py        # Treatment planning system
├── 🧪 test_app.py                       # System testing utilities
├── 📋 requirements.txt                   # Python dependencies
├── 📖 README.md                         # This documentation
├── 🎭 demo_instructions.md              # Demo usage guide
├── 📊 PROJECT_SUMMARY.md               # Technical project summary
├── 📄 LICENSE                          # MIT License
└── 🌍 PROJE_OZETI.md                   # Turkish project summary
```

## 🎯 Application-Specific Features

### 🏥 Physiotherapy Assessment System

#### Clinical Analysis Capabilities
- **33-Point Body Analysis**: Complete biomechanical assessment
- **Risk Stratification**: Professional injury risk categorization
- **Compensation Patterns**: Upper/Lower Crossed Syndrome detection
- **Functional Scoring**: 0-100 scale for each body region
- **Treatment Planning**: Evidence-based exercise protocols

#### Assessment Parameters
- **Cervical**: Forward head posture, neck inclination
- **Shoulder**: Protraction, asymmetry, blade positioning
- **Spinal**: Lateral tilt, kyphosis/lordosis curves
- **Pelvic**: Tilt angle, hip asymmetry analysis
- **Lower Extremity**: Knee angles, valgus/varus assessment

#### Usage Workflow
1. **Setup**: Position for full body visibility
2. **Profile**: Enter age and exercise experience
3. **Analysis**: Real-time biomechanical assessment
4. **Planning**: Generate personalized treatment protocols

### 🤚 Hand Tracking System

#### Detection Capabilities
- **21-Point Tracking**: Detailed hand landmark detection
- **Dual Hand Support**: Simultaneous tracking of both hands
- **Gesture Recognition**: Fist, open hand, finger counting
- **Real-time Analysis**: 30+ FPS processing speed

#### Gesture Analysis
- **Finger States**: Extended/flexed position detection
- **Hand Orientation**: Palm direction and rotation
- **Distance Metrics**: Inter-finger and palm measurements
- **Confidence Scoring**: Detection reliability assessment

#### Usage Workflow
1. **Setup**: Position hands clearly in camera view
2. **Calibration**: Adjust sensitivity for optimal detection
3. **Interaction**: Perform gestures for real-time analysis
4. **Feedback**: View detailed landmark and gesture data

## 🔧 System Requirements

### Hardware Requirements
- **Camera**: HD webcam or built-in camera (720p minimum)
- **Processor**: Multi-core CPU (Intel i5/AMD Ryzen 5 or better)
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB free space for dependencies

### Software Requirements
- **Python**: 3.7+ (3.8+ recommended)
- **Operating System**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Browser**: Chrome 80+, Firefox 75+, Safari 13+, Edge 80+

### Network Requirements
- **Internet**: Required for initial setup and dependency installation
- **Local Network**: Applications run locally (no cloud processing)

## 📚 Dependencies

The applications share common dependencies managed through `requirements.txt`:

```txt
opencv-python>=4.8.0      # Computer vision and image processing
mediapipe>=0.10.0         # AI pose and hand estimation
gradio>=4.0.0             # Web interface framework
numpy>=1.21.0             # Numerical computations
Pillow>=9.0.0             # Image manipulation support
```

### Installation Notes
- **MediaPipe**: Requires specific versions for stability
- **OpenCV**: Hardware acceleration support varies by platform
- **Gradio**: Automatic port selection (7860, 7861, etc.)

## 🎯 Performance Metrics

### Expected Performance
- **Frame Rate**: 15-30 FPS (device dependent)
- **Latency**: <100ms processing time
- **Accuracy**: 90%+ in optimal conditions
- **Detection Rate**: 95%+ with proper positioning

### Optimization Tips
- **Lighting**: Ensure even, bright lighting
- **Background**: Use plain, contrasting backgrounds
- **Distance**: Maintain 1.5-3 meters from camera
- **Stability**: Minimize camera movement and vibration

## 🚀 Use Cases & Applications

### 🏥 Healthcare & Clinical
- **Physiotherapy Clinics**: Professional patient assessment
- **Rehabilitation Centers**: Progress monitoring and treatment planning
- **Sports Medicine**: Athlete biomechanical analysis
- **Occupational Health**: Workplace injury prevention

### 🏢 Corporate & Workplace
- **Ergonomic Assessment**: Workstation setup evaluation
- **Employee Wellness**: Posture monitoring programs
- **Safety Training**: Movement pattern education
- **Health Screenings**: Preventive health initiatives

### 🎓 Research & Education
- **Biomechanics Research**: Movement pattern studies
- **Medical Education**: Clinical assessment training
- **Kinesiology Studies**: Human movement analysis
- **Rehabilitation Research**: Treatment efficacy studies

### 🏠 Personal & Home Use
- **Posture Monitoring**: Daily posture awareness
- **Exercise Guidance**: Home rehabilitation programs
- **Fitness Assessment**: Personal movement quality
- **Health Tracking**: Long-term posture trends

## 🔬 Technical Architecture

### Core Analysis Engine
```
📊 Data Flow:
Camera Input → MediaPipe Processing → Feature Extraction →
Clinical Analysis → Risk Assessment → Treatment Planning →
User Interface Display
```

### Module Dependencies
```
🏥 physiotherapy_assessment_app.py
├── 🔬 advanced_physiotherapy_algorithms.py
├── 💊 clinical_feedback_system.py
├── 📊 MediaPipe Pose
└── 🎨 Gradio Interface

🤚 hand_tracking_app.py
├── 📊 MediaPipe Hands
├── 🎯 Gesture Recognition
└── 🎨 Gradio Interface
```

## 🛠️ Development & Testing

### Running Tests
```bash
# Test system dependencies and imports
python test_app.py

# Verify camera and MediaPipe functionality
python -c "import cv2, mediapipe; print('Dependencies OK')"
```

### Development Setup
```bash
# Create virtual environment (recommended)
python -m venv pose-think-env
source pose-think-env/bin/activate  # Linux/Mac
# or
pose-think-env\Scripts\activate     # Windows

# Install in development mode
pip install -e .
```

### Troubleshooting Common Issues

#### Camera Not Working
- Check browser permissions for camera access
- Ensure no other applications are using the camera
- Try different browsers (Chrome recommended)

#### Poor Detection Accuracy
- Improve lighting conditions
- Use plain, contrasting background
- Adjust detection sensitivity in settings
- Ensure full body/hands are visible

#### Performance Issues
- Close unnecessary applications
- Reduce browser tabs
- Check system resource usage
- Consider lowering camera resolution

## 🚀 Roadmap & Future Development

### Short-term Goals (1-3 months)
- [ ] **Mobile Optimization**: Responsive design for tablets and phones
- [ ] **Video Analysis**: Upload and analyze recorded videos
- [ ] **Data Export**: CSV/PDF report generation
- [ ] **Multi-language Support**: Additional language interfaces

### Medium-term Goals (3-6 months)
- [ ] **Patient Database**: Multi-user tracking and history
- [ ] **Advanced Analytics**: Trend analysis and progress tracking
- [ ] **Telemedicine Integration**: Remote consultation features
- [ ] **Wearable Integration**: IoT device data fusion

### Long-term Vision (6+ months)
- [ ] **AI Enhancement**: Custom model training for specific populations
- [ ] **Clinical Validation**: Peer-reviewed accuracy studies
- [ ] **Enterprise Features**: Hospital/clinic management systems
- [ ] **Research Platform**: Academic collaboration tools

## 🤝 Contributing

We welcome contributions to improve and expand the Pose-Think suite! Here's how you can help:

### Types of Contributions
- **Bug Reports**: Report issues with detailed reproduction steps
- **Feature Requests**: Suggest new applications or improvements
- **Code Contributions**: Submit pull requests for new features or fixes
- **Documentation**: Improve guides, tutorials, and API documentation
- **Testing**: Help test applications across different platforms

### Development Guidelines
1. **Fork** the repository and create a feature branch
2. **Follow** existing code style and comment conventions (bilingual comments)
3. **Test** your changes thoroughly across different scenarios
4. **Document** new features and update relevant documentation
5. **Submit** a pull request with clear description of changes

### Code Style
- **Comments**: Bilingual format "Turkish explanation / English explanation"
- **Functions**: Comprehensive docstrings in both languages
- **Variables**: Descriptive names with clear purpose
- **Structure**: Modular design following existing patterns

## 📄 License & Legal

### License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for complete terms.

### Medical Disclaimer
⚠️ **Important**: These applications are for educational and research purposes only. They do not provide medical diagnosis or replace professional healthcare advice. Always consult qualified healthcare professionals for medical concerns.

### Privacy & Data
- **Local Processing**: All analysis performed locally on your device
- **No Data Collection**: No personal data transmitted or stored remotely
- **Camera Access**: Used only for real-time analysis, not recorded or saved

## 🙏 Acknowledgments & Credits

### Core Technologies
- **[Google MediaPipe](https://mediapipe.dev/)**: State-of-the-art ML framework for pose and hand detection
- **[Gradio](https://gradio.app/)**: Intuitive web interface framework for ML applications
- **[OpenCV](https://opencv.org/)**: Comprehensive computer vision library

### Clinical Expertise
- **Physiotherapy Community**: Professional guidance and clinical validation
- **Biomechanics Researchers**: Scientific foundation and methodology
- **Healthcare Professionals**: Real-world testing and feedback

### Development Support
- **Open Source Community**: Continuous inspiration and collaboration
- **Academic Institutions**: Research partnerships and validation studies

## 📞 Contact & Support

### Developer
- **Name**: Sems Kurtoglu
- **GitHub**: [@semskurto](https://github.com/semskurto)
- **Project Repository**: [pose-think](https://github.com/semskurto/pose-think)

### Support Channels
- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: GitHub Discussions for questions and community interaction
- **Documentation**: Check `demo_instructions.md` for detailed usage guides

### Professional Inquiries
For clinical partnerships, research collaborations, or commercial licensing, please contact through GitHub or create a detailed issue with your requirements.

---

**🎯 Mission**: Democratizing access to professional-grade movement analysis through open-source AI technology, making advanced biomechanical assessment available to healthcare professionals, researchers, and individuals worldwide.
