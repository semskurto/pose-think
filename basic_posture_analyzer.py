# Temel Postür Analiz Sistemi / Basic Posture Analysis System
import cv2
import mediapipe as mp
import gradio as gr
import numpy as np

# MediaPipe başlatma / Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

class BasicPostureAnalyzer:
    """Temel postür analiz sınıfı / Basic posture analyzer class"""
    
    def __init__(self):
        self.pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def calculate_angle(self, a, b, c):
        """Üç nokta arasındaki açıyı hesapla / Calculate angle between three points"""
        try:
            a = np.array(a)
            b = np.array(b)
            c = np.array(c)
            
            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            angle = np.abs(radians * 180.0 / np.pi)
            
            if angle > 180.0:
                angle = 360 - angle
                
            return angle
        except:
            return 0
    
    def analyze_frame(self, frame):
        """Frame analiz et / Analyze frame"""
        if frame is None:
            return None, "❌ Kamera bağlantısı yok / No camera connection"
        
        # BGR'den RGB'ye çevir / Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Pose tespiti / Pose detection
        results = self.pose.process(rgb_frame)
        
        # Çizim için BGR'ye geri çevir / Convert back to BGR for drawing
        output_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        
        feedback = []
        
        if results.pose_landmarks:
            # Landmark'ları çiz / Draw landmarks
            mp_drawing.draw_landmarks(
                output_frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )
            
            landmarks = results.pose_landmarks.landmark
            
            # Görünür parçaları kontrol et / Check visible parts
            visible_parts = []
            
            # Baş / Head
            if landmarks[mp_pose.PoseLandmark.NOSE.value].visibility > 0.5:
                visible_parts.append("Baş/Head")
            
            # Omuzlar / Shoulders
            if (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility > 0.5 and 
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility > 0.5):
                visible_parts.append("Omuzlar/Shoulders")
                
                # Omuz seviyesi kontrolü / Shoulder level check
                left_shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
                right_shoulder_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
                shoulder_diff = abs(left_shoulder_y - right_shoulder_y)
                
                if shoulder_diff > 0.05:
                    if left_shoulder_y < right_shoulder_y:
                        feedback.append("⚠️ Sol omuz daha yüksek / Left shoulder higher")
                    else:
                        feedback.append("⚠️ Sağ omuz daha yüksek / Right shoulder higher")
                else:
                    feedback.append("✅ Omuzlar seviyeli / Shoulders level")
            
            # Dirsekler / Elbows
            if (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility > 0.5 and 
                landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].visibility > 0.5):
                visible_parts.append("Dirsekler/Elbows")
                
                # Sol dirsek açısı / Left elbow angle
                try:
                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                   landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    
                    left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
                    if left_elbow_angle > 0:
                        feedback.append(f"📐 Sol dirsek açısı / Left elbow: {left_elbow_angle:.1f}°")
                        
                    # Sağ dirsek açısı / Right elbow angle
                    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    
                    right_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
                    if right_elbow_angle > 0:
                        feedback.append(f"📐 Sağ dirsek açısı / Right elbow: {right_elbow_angle:.1f}°")
                except:
                    feedback.append("⚠️ Dirsek açısı hesaplanamadı / Cannot calculate elbow angles")
            
            # Kalçalar / Hips
            if (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility > 0.5 and 
                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].visibility > 0.5):
                visible_parts.append("Kalçalar/Hips")
                
                # Kalça seviyesi / Hip level
                left_hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
                right_hip_y = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y
                hip_diff = abs(left_hip_y - right_hip_y)
                
                if hip_diff > 0.03:
                    if left_hip_y < right_hip_y:
                        feedback.append("⚠️ Sol kalça daha yüksek / Left hip higher")
                    else:
                        feedback.append("⚠️ Sağ kalça daha yüksek / Right hip higher")
                else:
                    feedback.append("✅ Kalçalar seviyeli / Hips level")
            
            # Dizler / Knees
            if (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility > 0.5 and 
                landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].visibility > 0.5):
                visible_parts.append("Dizler/Knees")
            
            # Boyun pozisyonu / Neck position
            if (landmarks[mp_pose.PoseLandmark.NOSE.value].visibility > 0.5 and
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility > 0.5 and
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility > 0.5):
                
                nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                
                shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
                head_offset = abs(nose.x - shoulder_center_x)
                
                if head_offset > 0.08:
                    if nose.x < shoulder_center_x:
                        feedback.append("🔍 Boyun: Sola eğik / Neck: Tilted left")
                    else:
                        feedback.append("🔍 Boyun: Sağa eğik / Neck: Tilted right")
                else:
                    feedback.append("🔍 Boyun: Merkezi / Neck: Centered")
            
            # Görünür parçaları listele / List visible parts
            if visible_parts:
                feedback.insert(0, f"✅ Görünen / Visible: {', '.join(visible_parts)}")
                feedback.insert(1, "")  # Boş satır / Empty line
        else:
            feedback.append("❌ Vücut tespit edilemedi / Body not detected")
            feedback.append("📍 Kameraya tam vücut görünecek şekilde durun / Stand so full body is visible")
        
        return output_frame, "\n".join(feedback)

# Global analyzer
analyzer = BasicPostureAnalyzer()

def process_frame(frame):
    """Frame işle / Process frame"""
    return analyzer.analyze_frame(frame)

# Gradio arayüzü / Gradio interface
demo = gr.Interface(
    fn=process_frame,
    inputs=gr.Image(sources=["webcam"], streaming=True),
    outputs=[
        gr.Image(streaming=True, label="🎯 Analysis"),
        gr.Textbox(label="📊 Feedback", lines=10)
    ],
    title="🎯 Basic Posture Analyzer",
    description="""
    **Real-time posture analysis - tells you exactly what the camera sees:**
    - Visible body parts (head, shoulders, elbows, hips, knees)
    - Joint angles (elbows with precise measurements)
    - Posture alignment (shoulder level, head position, hip level)
    
    **Instructions:**
    1. Allow camera access
    2. Stand 2-3 meters from camera
    3. Ensure good lighting
    4. Keep full body visible
    """,
    live=True
)

if __name__ == "__main__":
    demo.launch(
        share=False,
        server_port=7864,
        show_error=True
    )
