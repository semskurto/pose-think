# Test dosyası / Test file
import sys
import os

print("Python version:", sys.version)
print("Current directory:", os.getcwd())

try:
    import cv2
    print("✅ OpenCV imported successfully")
except ImportError as e:
    print("❌ OpenCV import failed:", e)

try:
    import mediapipe as mp
    print("✅ MediaPipe imported successfully")
    print("MediaPipe version:", mp.__version__)
    
    # MediaPipe solutions test
    try:
        mp_pose = mp.solutions.pose
        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        print("✅ MediaPipe solutions imported successfully")
    except Exception as e:
        print("❌ MediaPipe solutions import failed:", e)
        
except ImportError as e:
    print("❌ MediaPipe import failed:", e)

try:
    import gradio as gr
    print("✅ Gradio imported successfully")
    print("Gradio version:", gr.__version__)
except ImportError as e:
    print("❌ Gradio import failed:", e)

try:
    import numpy as np
    print("✅ NumPy imported successfully")
    print("NumPy version:", np.__version__)
except ImportError as e:
    print("❌ NumPy import failed:", e)

# Test our custom modules
try:
    from advanced_physiotherapy_algorithms import AdvancedPhysiotherapyAnalyzer
    print("✅ Advanced physiotherapy algorithms imported successfully")
except ImportError as e:
    print("❌ Advanced physiotherapy algorithms import failed:", e)

try:
    from clinical_feedback_system import ClinicalFeedbackSystem
    print("✅ Clinical feedback system imported successfully")
except ImportError as e:
    print("❌ Clinical feedback system import failed:", e)

print("\n🎯 All imports tested!")
