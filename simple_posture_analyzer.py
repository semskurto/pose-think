# Basit Postür Analiz Sistemi / Simple Posture Analysis System
import cv2
import mediapipe as mp
import gradio as gr
import numpy as np
import math

# MediaPipe başlatma / Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

class SimplePostureAnalyzer:
    """Basit postür analiz sınıfı / Simple posture analyzer class"""
    
    def __init__(self):
        self.pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,  # Daha hızlı işlem için / Faster processing
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def calculate_angle(self, a, b, c):
        """Üç nokta arasındaki açıyı hesapla / Calculate angle between three points"""
        try:
            a = np.array(a)  # İlk nokta / First point
            b = np.array(b)  # Orta nokta / Middle point  
            c = np.array(c)  # Son nokta / Last point
            
            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            angle = np.abs(radians * 180.0 / np.pi)
            
            if angle > 180.0:
                angle = 360 - angle
                
            return angle
        except:
            return 0
    
    def analyze_frame(self, frame):
        """Frame analiz et ve geri bildirim ver / Analyze frame and provide feedback"""
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
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            # Landmark koordinatlarını al / Get landmark coordinates
            landmarks = results.pose_landmarks.landmark
            
            # Görünür vücut parçalarını kontrol et / Check visible body parts
            feedback.extend(self.check_visible_parts(landmarks))
            
            # Açı analizleri / Angle analyses
            feedback.extend(self.analyze_angles(landmarks))
            
            # Postür kontrolü / Posture check
            feedback.extend(self.check_posture(landmarks))
            
        else:
            feedback.append("❌ Vücut tespit edilemedi / Body not detected")
            feedback.append("📍 Kameraya tam vücut görünecek şekilde durun / Stand so full body is visible")
        
        return output_frame, "\n".join(feedback)
    
    def check_visible_parts(self, landmarks):
        """Görünür vücut parçalarını kontrol et / Check visible body parts"""
        feedback = []
        
        # Temel landmark'ların görünürlüğünü kontrol et / Check visibility of basic landmarks
        key_points = {
            'Baş/Head': [mp_pose.PoseLandmark.NOSE],
            'Omuzlar/Shoulders': [mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER],
            'Dirsekler/Elbows': [mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.RIGHT_ELBOW],
            'Eller/Hands': [mp_pose.PoseLandmark.LEFT_WRIST, mp_pose.PoseLandmark.RIGHT_WRIST],
            'Kalçalar/Hips': [mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP],
            'Dizler/Knees': [mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.RIGHT_KNEE],
            'Ayaklar/Feet': [mp_pose.PoseLandmark.LEFT_ANKLE, mp_pose.PoseLandmark.RIGHT_ANKLE]
        }
        
        visible_parts = []
        for part_name, landmark_indices in key_points.items():
            if all(landmarks[idx.value].visibility > 0.5 for idx in landmark_indices):
                visible_parts.append(part_name)
        
        if visible_parts:
            feedback.append(f"✅ Görünen vücut parçaları / Visible body parts: {', '.join(visible_parts)}")
        
        return feedback
    
    def analyze_angles(self, landmarks):
        """Eklem açılarını analiz et / Analyze joint angles"""
        feedback = []
        
        try:
            # Sol dirsek açısı / Left elbow angle
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            
            if left_elbow_angle > 0:
                feedback.append(f"📐 Sol dirsek açısı / Left elbow angle: {left_elbow_angle:.1f}°")
                if left_elbow_angle < 30:
                    feedback.append("   ⚠️ Sol kol çok bükümlü / Left arm very bent")
                elif left_elbow_angle > 160:
                    feedback.append("   ✅ Sol kol düz pozisyonda / Left arm in straight position")
            
            # Sağ dirsek açısı / Right elbow angle
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            
            right_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            
            if right_elbow_angle > 0:
                feedback.append(f"📐 Sağ dirsek açısı / Right elbow angle: {right_elbow_angle:.1f}°")
                if right_elbow_angle < 30:
                    feedback.append("   ⚠️ Sağ kol çok bükümlü / Right arm very bent")
                elif right_elbow_angle > 160:
                    feedback.append("   ✅ Sağ kol düz pozisyonda / Right arm in straight position")
            
            # Diz açıları / Knee angles
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
            
            if left_knee_angle > 0:
                feedback.append(f"🦵 Sol diz açısı / Left knee angle: {left_knee_angle:.1f}°")
                if left_knee_angle < 160:
                    feedback.append("   ⚠️ Sol diz bükümlü / Left knee bent")
                else:
                    feedback.append("   ✅ Sol diz düz / Left knee straight")
        
        except Exception as e:
            feedback.append(f"⚠️ Açı hesaplama hatası / Angle calculation error: {str(e)}")
        
        return feedback
    
    def check_posture(self, landmarks):
        """Postür kontrolü yap / Check posture"""
        feedback = []
        
        try:
            # Omuz seviyesi kontrolü / Shoulder level check
            left_shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
            right_shoulder_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
            shoulder_diff = abs(left_shoulder_y - right_shoulder_y)
            
            if shoulder_diff > 0.05:  # %5'ten fazla fark / More than 5% difference
                if left_shoulder_y < right_shoulder_y:
                    feedback.append("⚠️ Sol omuz daha yüksek / Left shoulder higher")
                else:
                    feedback.append("⚠️ Sağ omuz daha yüksek / Right shoulder higher")
            else:
                feedback.append("✅ Omuzlar seviyeli / Shoulders level")
            
            # Baş pozisyonu / Head position
            nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            
            shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
            head_offset = abs(nose.x - shoulder_center_x)
            
            if head_offset > 0.1:  # %10'dan fazla sapma / More than 10% deviation
                if nose.x < shoulder_center_x:
                    feedback.append("⚠️ Baş sola eğik / Head tilted left")
                else:
                    feedback.append("⚠️ Baş sağa eğik / Head tilted right")
            else:
                feedback.append("✅ Baş merkezi pozisyonda / Head centered")
            
            # İleri baş pozisyonu kontrolü / Forward head posture check
            shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
            if nose.y < shoulder_center_y - 0.15:  # Baş omuzlardan çok yukarıda / Head much above shoulders
                feedback.append("✅ Dik duruş / Upright posture")
            elif nose.y > shoulder_center_y - 0.05:  # Baş omuz seviyesine yakın / Head close to shoulder level
                feedback.append("⚠️ İleri baş pozisyonu / Forward head posture")
            
            # Kalça seviyesi / Hip level
            left_hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
            right_hip_y = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y
            hip_diff = abs(left_hip_y - right_hip_y)
            
            if hip_diff > 0.03:  # %3'ten fazla fark / More than 3% difference
                if left_hip_y < right_hip_y:
                    feedback.append("⚠️ Sol kalça daha yüksek / Left hip higher")
                else:
                    feedback.append("⚠️ Sağ kalça daha yüksek / Right hip higher")
            else:
                feedback.append("✅ Kalçalar seviyeli / Hips level")
        
        except Exception as e:
            feedback.append(f"⚠️ Postür analiz hatası / Posture analysis error: {str(e)}")
        
        return feedback

# Global analyzer instance
analyzer = SimplePostureAnalyzer()

def process_video_frame(frame):
    """Video frame işle / Process video frame"""
    return analyzer.analyze_frame(frame)

# Gradio arayüzü / Gradio interface
demo = gr.Interface(
    fn=process_video_frame,
    inputs=gr.Image(sources=["webcam"], streaming=True, label="📹 Camera Input"),
    outputs=[
        gr.Image(streaming=True, label="🎯 Analysis Output"),
        gr.Textbox(label="📊 Real-time Feedback", lines=15)
    ],
    title="🎯 Simple Posture Analyzer",
    description="""
    ## Real-time body posture and joint angle analysis

    **What it detects:**
    - Visible body parts (head, shoulders, elbows, hands, hips, knees, feet)
    - Joint angles (elbows, knees) with precise measurements
    - Posture issues (shoulder level, head position, hip alignment)

    **Instructions:**
    1. Allow camera access when prompted
    2. Stand 2-3 meters from the camera
    3. Ensure good lighting and plain background
    4. Keep full body visible for best results
    """,
    live=True
)


if __name__ == "__main__":
    demo.launch(
        share=False,
        server_port=7862,
        show_error=True
    )
