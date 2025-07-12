# 🤚 Real-time Hand Tracking System

Advanced hand tracking and gesture recognition application using MediaPipe technology with a user-friendly Gradio web interface.

## 🌟 Features

### Core Functionality
- **Real-time Hand Detection**: Tracks up to 2 hands simultaneously with high precision
- **21 Hand Landmarks**: Detects 21 key points per hand including fingertips, joints, and palm
- **Gesture Recognition**: Identifies basic gestures like fist, open hand, and finger counting
- **Finger Analysis**: Real-time analysis of individual finger positions (extended/closed)
- **Adjustable Sensitivity**: Customizable detection confidence threshold
- **Live Feedback**: Detailed real-time analysis and feedback

### User Interface
- **Web-based Interface**: Clean, modern Gradio interface accessible via web browser
- **Real-time Streaming**: Live camera feed with instant processing
- **Interactive Controls**: Adjustable confidence threshold slider
- **Responsive Design**: Works on desktop and mobile devices
- **Public Sharing**: Optional public URL for remote access

## 🛠️ Technical Details

### Technology Stack
- **MediaPipe**: Google's machine learning framework for hand tracking
- **OpenCV**: Computer vision library for image processing
- **Gradio**: Web interface framework for machine learning applications
- **NumPy**: Numerical computing library for efficient array operations
- **Python**: Core programming language

### Hand Tracking Model
- **Model**: MediaPipe Hands solution
- **Landmarks**: 21 3D hand landmarks per hand
- **Accuracy**: High precision tracking with sub-pixel accuracy
- **Performance**: Optimized for real-time processing
- **Robustness**: Works in various lighting conditions and hand orientations

### Landmark Points
The system tracks 21 key points on each hand:
- **Wrist** (1 point)
- **Thumb** (4 points): CMC, MCP, IP, TIP
- **Index Finger** (4 points): MCP, PIP, DIP, TIP
- **Middle Finger** (4 points): MCP, PIP, DIP, TIP
- **Ring Finger** (4 points): MCP, PIP, DIP, TIP
- **Pinky** (4 points): MCP, PIP, DIP, TIP

### Gesture Recognition
- **Fist Detection**: All fingers closed
- **Open Hand**: All fingers extended
- **Finger Counting**: 1-5 fingers extended
- **Custom Gestures**: Extensible framework for additional gestures

## 📋 Requirements

### System Requirements
- **Python**: 3.7 or higher
- **Camera**: Webcam or built-in camera
- **Browser**: Modern web browser with camera access
- **OS**: Windows, macOS, or Linux

### Hardware Recommendations
- **CPU**: Multi-core processor for smooth real-time processing
- **RAM**: 4GB minimum, 8GB recommended
- **Camera**: HD webcam for better detection accuracy
- **Internet**: Required for initial model download and public sharing

## 🚀 Installation

### 1. Clone or Download
```bash
git clone <repository-url>
cd hand-tracking-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python hand_tracking_app.py
```

### 4. Access the Interface
- **Local**: http://localhost:7860
- **Public**: Use the generated Gradio public URL (if sharing enabled)

## 📖 Usage Guide

### Getting Started
1. **Launch the application** using the command above
2. **Open the web interface** in your browser
3. **Allow camera access** when prompted
4. **Position your hand** clearly in front of the camera
5. **Adjust settings** as needed for optimal detection

### Interface Controls
- **Confidence Threshold Slider**: Adjust detection sensitivity
  - Lower values (0.1-0.4): More sensitive, detects hands more easily
  - Higher values (0.6-1.0): Less sensitive, requires clearer hand visibility
- **Camera Input**: Live webcam feed
- **Tracking Output**: Processed video with hand landmarks
- **Analysis Panel**: Real-time text feedback and gesture information

### Tips for Best Results
- **Good Lighting**: Ensure adequate lighting for clear hand visibility
- **Stable Position**: Keep hands relatively stable for consistent tracking
- **Clear Background**: Plain backgrounds improve detection accuracy
- **Hand Orientation**: Works with various hand orientations and positions
- **Distance**: Maintain appropriate distance from camera (arm's length)

## 🔧 Configuration

### Adjustable Parameters
- **Detection Confidence**: Minimum confidence for hand detection (0.1-1.0)
- **Tracking Confidence**: Minimum confidence for hand tracking (0.1-1.0)
- **Maximum Hands**: Number of hands to detect (1-2)
- **Model Complexity**: Processing complexity vs. accuracy trade-off

### Performance Optimization
- **Lower confidence thresholds** for easier detection in challenging conditions
- **Higher confidence thresholds** for more accurate detection with less noise
- **Adjust camera resolution** if experiencing performance issues
- **Close other applications** for better CPU performance

## 🎯 Applications

### Educational
- **Sign Language Learning**: Practice and analyze hand gestures
- **Gesture Studies**: Research hand movement patterns
- **Interactive Learning**: Engaging educational demonstrations

### Accessibility
- **Gesture Control**: Hands-free computer interaction
- **Communication Aid**: Visual gesture recognition for communication
- **Assistive Technology**: Support for users with specific needs

### Entertainment
- **Interactive Games**: Hand gesture-based gaming
- **Virtual Reality**: Hand tracking for VR applications
- **Creative Arts**: Digital art and performance applications

### Development
- **Prototype Testing**: Test hand tracking algorithms
- **Research Platform**: Foundation for advanced gesture recognition
- **Integration Base**: Starting point for custom applications

## 🔍 Troubleshooting

### Common Issues
- **Camera not detected**: Check camera permissions and connections
- **Poor tracking**: Adjust lighting and confidence threshold
- **Slow performance**: Close other applications, check system resources
- **No hands detected**: Ensure hands are clearly visible and well-lit

### Performance Issues
- **High CPU usage**: Normal for real-time processing
- **Lag or delay**: Check camera resolution and system performance
- **Memory usage**: Restart application if memory usage grows over time

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **MediaPipe Team**: For the excellent hand tracking technology
- **Gradio Team**: For the user-friendly web interface framework
- **OpenCV Community**: For computer vision tools and libraries
- **Python Community**: For the robust ecosystem of libraries

## 📞 Support

For questions, issues, or suggestions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the usage guide for common solutions

---

**Built with ❤️ using MediaPipe, Gradio, and Python**
