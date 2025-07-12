# Gerekli kütüphaneleri içe aktar / Import necessary libraries
import cv2
import mediapipe as mp
import gradio as gr
import numpy as np

# MediaPipe el takip modüllerini başlat / Initialize MediaPipe hand tracking modules
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def process_frame(frame):
    """
    Tek bir frame'i el tespiti için işler / Process a single frame for hand detection
    
    Args:
        frame: Giriş görüntüsü (numpy array) / Input image (numpy array)
    
    Returns:
        annotated_frame: El landmark'ları çizilmiş görüntü / Image with hand landmarks drawn
    """
    # El tespit edici başlat / Initialize hands detector
    with mp_hands.Hands(
        static_image_mode=False,      # Video akışı için False / False for video stream
        max_num_hands=2,              # Maksimum 2 el tespit et / Detect maximum 2 hands
        min_detection_confidence=0.5, # Minimum tespit güven skoru / Minimum detection confidence
        min_tracking_confidence=0.5   # Minimum takip güven skoru / Minimum tracking confidence
    ) as hands:
        
        # BGR'den RGB'ye dönüştür (MediaPipe RGB kullanır) / Convert BGR to RGB (MediaPipe uses RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Frame'i işle ve el landmark'larını tespit et / Process frame and detect hand landmarks
        results = hands.process(rgb_frame)
        
        # Görüntüleme için tekrar BGR'ye dönüştür / Convert back to BGR for display
        annotated_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        
        # El landmark'larını çiz / Draw hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # El landmark'larını ve bağlantılarını çiz / Draw hand landmarks and connections
                mp_drawing.draw_landmarks(
                    annotated_frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
        
        return annotated_frame

def analyze_hand_gestures(landmarks):
    """
    El hareketlerini analiz eder ve geri bildirim verir / Analyze hand gestures and provide feedback
    
    Args:
        landmarks: MediaPipe'dan gelen el landmark'ları / Hand landmarks from MediaPipe
    
    Returns:
        feedback: Analiz sonucu metni / Analysis result text
    """
    if not landmarks:
        return "El tespit edilemedi / No hands detected"
    
    feedback = []
    
    try:
        # Parmak uçları ve eklemleri / Finger tips and joints
        # Başparmak / Thumb: 4
        # İşaret parmağı / Index finger: 8
        # Orta parmak / Middle finger: 12
        # Yüzük parmağı / Ring finger: 16
        # Serçe parmak / Pinky: 20
        
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        # Parmak eklemleri / Finger joints
        thumb_joint = landmarks[3]
        index_joint = landmarks[6]
        middle_joint = landmarks[10]
        ring_joint = landmarks[14]
        pinky_joint = landmarks[18]
        
        # Açık parmakları say / Count extended fingers
        extended_fingers = 0
        finger_status = []
        
        # Başparmak kontrolü (x koordinatına göre) / Thumb check (based on x coordinate)
        if thumb_tip.x > thumb_joint.x:  # Sağ el için / For right hand
            extended_fingers += 1
            finger_status.append("Başparmak açık / Thumb extended")
        else:
            finger_status.append("Başparmak kapalı / Thumb closed")
        
        # Diğer parmaklar (y koordinatına göre) / Other fingers (based on y coordinate)
        fingers = [
            (index_tip, index_joint, "İşaret parmağı / Index finger"),
            (middle_tip, middle_joint, "Orta parmak / Middle finger"),
            (ring_tip, ring_joint, "Yüzük parmağı / Ring finger"),
            (pinky_tip, pinky_joint, "Serçe parmak / Pinky")
        ]
        
        for tip, joint, name in fingers:
            if tip.y < joint.y:  # Parmak ucu ekleme göre yukarıda / Finger tip above joint
                extended_fingers += 1
                finger_status.append(f"{name} açık / extended")
            else:
                finger_status.append(f"{name} kapalı / closed")
        
        # Genel durum / Overall status
        feedback.append(f"Açık parmak sayısı / Extended fingers: {extended_fingers}")
        feedback.extend(finger_status)
        
        # Basit jest tanıma / Simple gesture recognition
        if extended_fingers == 0:
            feedback.append("✊ Yumruk / Fist")
        elif extended_fingers == 1:
            feedback.append("☝️ Bir parmak / One finger")
        elif extended_fingers == 2:
            feedback.append("✌️ İki parmak / Two fingers")
        elif extended_fingers == 5:
            feedback.append("✋ Açık el / Open hand")
        else:
            feedback.append(f"🤚 {extended_fingers} parmak açık / {extended_fingers} fingers extended")
            
    except Exception as e:
        feedback.append(f"Analiz hatası / Analysis error: {str(e)}")
    
    return "\n".join(feedback)

def webcam_interface(frame, confidence_threshold):
    """
    Gradio webcam girişi için arayüz fonksiyonu / Interface function for Gradio webcam input
    
    Args:
        frame: Webcam'den gelen frame / Frame from webcam
        confidence_threshold: Güven eşiği / Confidence threshold
    
    Returns:
        processed_frame: İşlenmiş frame / Processed frame
        feedback: Analiz sonucu / Analysis result
    """
    if frame is None:
        return None, "Kamera verisi yok / No camera data"
    
    # El tespit edici başlat / Initialize hands detector
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=confidence_threshold,
        min_tracking_confidence=confidence_threshold
    ) as hands:
        
        # BGR'den RGB'ye dönüştür / Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Frame'i işle / Process frame
        results = hands.process(rgb_frame)
        
        feedback = ""
        
        # Sonuçları çiz ve analiz yap / Draw results and analyze
        if results.multi_hand_landmarks:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # El landmark'larını çiz / Draw hand landmarks
                mp_drawing.draw_landmarks(
                    rgb_frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # El analizini yap / Perform hand analysis
                hand_feedback = analyze_hand_gestures(hand_landmarks.landmark)
                feedback += f"El {i+1} / Hand {i+1}:\n{hand_feedback}\n\n"
        else:
            feedback = "El tespit edilemedi. Elinizi kameraya gösterin. / No hands detected. Show your hand to the camera."
        
        return rgb_frame, feedback

# Gradio arayüzünü oluştur / Create Gradio interface
with gr.Blocks(
    title="Real-time Hand Tracking System",
    theme=gr.themes.Soft(),
    css="footer {visibility: hidden}"
) as demo:
    
    # Başlık ve açıklama / Title and description
    gr.Markdown("# 🤚 Real-time Hand Tracking System")
    gr.Markdown("""
    **Advanced hand tracking and gesture recognition using MediaPipe technology**
    
    This application provides real-time hand tracking with detailed gesture analysis and finger position detection.
    """)
    
    with gr.Row():
        with gr.Column():
            # Güven eşiği ayarı / Confidence threshold setting
            confidence_slider = gr.Slider(
                minimum=0.1,
                maximum=1.0,
                value=0.5,
                step=0.1,
                label="Detection Confidence Threshold",
                info="Lower values detect hands more easily, higher values require clearer hand visibility"
            )
            
            input_image = gr.Image(
                sources=["webcam"],
                streaming=True,
                label="Camera Input",
                height=400
            )
        
        with gr.Column():
            output_image = gr.Image(
                streaming=True,
                label="Hand Tracking Output",
                height=400
            )
            
            feedback_text = gr.Textbox(
                label="Real-time Hand Analysis",
                lines=10,
                max_lines=15,
                interactive=False,
                placeholder="Hand analysis will appear here..."
            )
    
    # Canlı işleme arayüzü / Live processing interface
    gr.Interface(
        fn=webcam_interface,
        inputs=[input_image, confidence_slider],
        outputs=[output_image, feedback_text],
        live=True,
        allow_flagging="never"
    )
    
    # Kullanım bilgileri / Usage information
    with gr.Accordion("📖 How to Use", open=False):
        gr.Markdown("""
        ## Instructions
        
        1. **Allow camera access** when prompted by your browser
        2. **Position your hand** clearly in front of the camera
        3. **Adjust the confidence threshold** if detection is too sensitive or not sensitive enough
        4. **Watch real-time analysis** of your hand gestures and finger positions
        
        ## Features
        
        - ✅ **Real-time hand detection** up to 2 hands simultaneously
        - ✅ **21 hand landmarks** per hand with high precision
        - ✅ **Finger position analysis** (extended/closed status)
        - ✅ **Basic gesture recognition** (fist, open hand, finger counting)
        - ✅ **Adjustable detection sensitivity**
        - ✅ **Detailed real-time feedback**
        
        ## Technical Details
        
        - **Model**: MediaPipe Hands
        - **Landmarks**: 21 key points per hand
        - **Processing**: Real-time with optimized performance
        - **Accuracy**: High precision hand tracking
        - **Latency**: Low latency for smooth interaction
        """)

if __name__ == "__main__":
    # Uygulamayı başlat / Launch application
    demo.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7860,
        show_api=False
    )
