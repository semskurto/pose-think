# 🎯 Demo Usage Instructions

## 🚀 Quick Start

### 1. Launch the Application
```bash
python physiotherapy_assessment_app.py
```

### 2. Open in Browser
- Open the provided URL in your browser when the application starts
- Usually: `http://localhost:7861`

### 3. Grant Camera Permission
- Select "Allow" when the browser requests camera permission

## 🎭 Demo Scenarios

### Scenario 1: Normal Posture Test
1. **Position**: Stand so your full body is visible to the camera
2. **Posture**: Natural, relaxed standing position
3. **Expected Result**: 80+ posture score, minimal risk

### Scenario 2: Forward Head Posture Simulation
1. **Position**: Extend your head forward (like computer use)
2. **Posture**: Bring shoulders forward
3. **Expected Result**: Forward head posture detection, moderate-high risk

### Scenario 3: Shoulder Asymmetry Test
1. **Position**: Hold one shoulder higher than the other
2. **Posture**: Asymmetric stance
3. **Expected Result**: Shoulder asymmetry detection, compensation patterns

### Scenario 4: Pelvic Tilt Simulation
1. **Position**: Push your hips forward or backward
2. **Posture**: Exaggerated lordosis or kyphosis
3. **Expected Result**: Pelvic tilt detection, spinal curvature warnings

## 🎛️ Control Panel Usage

### Sensitivity Settings
- **0.3-0.4**: Very sensitive (for noisy environments)
- **0.5**: Default (ideal for most situations)
- **0.6-0.9**: Less sensitive (requires clear image)

### Patient Profile
- **Age**: 18-80 range (affects exercise plan)
- **Experience**: Beginner/Intermediate/Advanced (difficulty level)

## 📊 Understanding Results

### Posture Score
- **90-100**: 🟢 Excellent - Preventive exercises
- **80-89**: 🟡 Good - Minor corrections
- **70-79**: 🟠 Fair - Regular exercise needed
- **60-69**: 🔴 Poor - Professional assessment
- **<60**: 🚨 Critical - Urgent intervention

### Risk Levels
- **Low**: Preventive measures sufficient
- **Moderate**: Regular exercise and monitoring
- **High**: Professional guidance required
- **Critical**: Urgent medical assessment

## 🏋️ Exercise Plans

### Basic Exercise Plan
- General recommendations
- Daily routines
- Simple exercises

### Clinical Treatment Plan
- Detailed assessment
- Personalized exercises
- Follow-up program
- Professional recommendations

## 🔧 Troubleshooting

### Camera Not Working
1. Check browser permissions
2. Ensure no other applications are using the camera
3. Restart the browser

### Body Not Detected
1. Full body must be visible
2. Use a plain, light-colored background
3. Increase lighting
4. Lower sensitivity setting

### Slow Performance
1. Close other applications
2. Reduce browser tabs
3. Lower camera resolution

## 📱 Browser Compatibility

### Recommended Browsers
- ✅ **Chrome**: Best performance
- ✅ **Firefox**: Good compatibility
- ✅ **Safari**: Suitable for macOS
- ⚠️ **Edge**: Basic features

### Mobile Devices
- Tablet: Supported
- Phone: Limited support (screen size)

## 🎥 Demo Video Recommendations

### Recording Tips
1. **Lighting**: Provide adequate lighting
2. **Background**: Prefer plain, single color
3. **Distance**: 2-3 meters distance is ideal
4. **Angle**: Camera should be at eye level

### Demo Flow
1. Normal posture → Excellent score demonstration
2. Poor posture → Risk detection
3. Exercise plan generation
4. Clinical treatment plan creation

## 📈 Performance Metrics

### Expected Values
- **FPS**: 15-30 (device dependent)
- **Latency**: <100ms
- **Accuracy**: 90%+ (in good conditions)
- **Detection Rate**: 95%+ (in proper position)

## 🎯 Demo Objectives

### Technical Demonstration
- Real-time analysis
- Accurate landmark detection
- Fast processing

### Clinical Value
- Professional assessment
- Meaningful recommendations
- Practical exercise plans

### User Experience
- Easy to use
- Clear results
- Interactive interface

---

**💡 Tip**: For the best demo experience, test in a well-lit environment with a plain background!
