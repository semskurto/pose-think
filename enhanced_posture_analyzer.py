# Gelişmiş Basit Postür Analiz Sistemi / Enhanced Simple Posture Analysis System
import cv2
import mediapipe as mp
import gradio as gr
import numpy as np
import math

# MediaPipe başlatma / Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

class EnhancedPostureAnalyzer:
    """Gelişmiş basit postür analiz sınıfı / Enhanced simple posture analyzer class"""
    
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
    
    def get_age_specific_recommendations(self, age, issues):
        """Yaşa özel öneriler / Age-specific recommendations"""
        recommendations = []
        
        if age < 25:
            recommendations.append("💡 Genç yaş: Postür alışkanlıkları şimdi oluşturun / Young age: Form posture habits now")
            if "forward_head" in issues:
                recommendations.append("📱 Telefon/bilgisayar kullanımını sınırlayın / Limit phone/computer use")
        elif age < 45:
            recommendations.append("💡 Orta yaş: Düzenli egzersiz önemli / Middle age: Regular exercise important")
            if "shoulder_imbalance" in issues:
                recommendations.append("💼 Çalışma ortamınızı ergonomik yapın / Make workspace ergonomic")
        else:
            recommendations.append("💡 Olgun yaş: Kemik sağlığına dikkat / Mature age: Focus on bone health")
            if "hip_imbalance" in issues:
                recommendations.append("🚶 Günlük yürüyüş yapın / Take daily walks")
        
        return recommendations
    
    def analyze_frame_with_profile(self, frame, age=None, height=None, weight=None):
        """Profil bilgileriyle frame analiz et / Analyze frame with profile information"""
        if frame is None:
            return None, "❌ Kamera bağlantısı yok / No camera connection"
        
        # Temel analiz / Basic analysis
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        output_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
        
        feedback = []
        detected_issues = []
        
        # Profil bilgisi varsa ekle / Add profile info if available
        if age or height or weight:
            profile_info = []
            if age:
                profile_info.append(f"Yaş/Age: {age}")
            if height:
                profile_info.append(f"Boy/Height: {height}cm")
            if weight:
                profile_info.append(f"Kilo/Weight: {weight}kg")
                
                # BMI hesapla / Calculate BMI
                if height and weight:
                    bmi = weight / ((height/100) ** 2)
                    profile_info.append(f"BMI: {bmi:.1f}")
                    
                    if bmi > 25:
                        feedback.append("⚠️ BMI yüksek - postür üzerinde ekstra yük / High BMI - extra load on posture")
                        detected_issues.append("high_bmi")
            
            feedback.append(f"👤 Profil / Profile: {' | '.join(profile_info)}")
            feedback.append("")
        
        if results.pose_landmarks:
            # Landmark'ları çiz / Draw landmarks
            mp_drawing.draw_landmarks(
                output_frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            landmarks = results.pose_landmarks.landmark
            
            # Detaylı analiz / Detailed analysis
            feedback.extend(self.detailed_body_analysis(landmarks, detected_issues))
            
            # Yaşa özel öneriler / Age-specific recommendations
            if age:
                recommendations = self.get_age_specific_recommendations(age, detected_issues)
                if recommendations:
                    feedback.append("")
                    feedback.append("🎯 Yaşınıza Özel Öneriler / Age-Specific Recommendations:")
                    feedback.extend(recommendations)
        else:
            feedback.append("❌ Vücut tespit edilemedi / Body not detected")
        
        return output_frame, "\n".join(feedback)
    
    def detailed_body_analysis(self, landmarks, detected_issues):
        """Detaylı vücut analizi / Detailed body analysis"""
        feedback = []
        
        try:
            # Görünür parçalar / Visible parts
            visible_parts = self.check_visibility(landmarks)
            feedback.append(f"✅ Görünen: {', '.join(visible_parts)} / Visible: {', '.join(visible_parts)}")
            feedback.append("")
            
            # Baş ve boyun analizi / Head and neck analysis
            head_analysis = self.analyze_head_neck(landmarks)
            feedback.extend(head_analysis)
            if "forward_head" in head_analysis[0]:
                detected_issues.append("forward_head")
            
            # Omuz analizi / Shoulder analysis
            shoulder_analysis = self.analyze_shoulders(landmarks)
            feedback.extend(shoulder_analysis)
            if "imbalance" in str(shoulder_analysis):
                detected_issues.append("shoulder_imbalance")
            
            # Gövde analizi / Torso analysis
            torso_analysis = self.analyze_torso(landmarks)
            feedback.extend(torso_analysis)
            
            # Kalça analizi / Hip analysis
            hip_analysis = self.analyze_hips(landmarks)
            feedback.extend(hip_analysis)
            if "imbalance" in str(hip_analysis):
                detected_issues.append("hip_imbalance")
            
            # Bacak analizi / Leg analysis
            leg_analysis = self.analyze_legs(landmarks)
            feedback.extend(leg_analysis)
            
        except Exception as e:
            feedback.append(f"⚠️ Analiz hatası / Analysis error: {str(e)}")
        
        return feedback
    
    def check_visibility(self, landmarks):
        """Görünürlük kontrolü / Visibility check"""
        parts = []
        
        # Baş / Head
        if landmarks[mp_pose.PoseLandmark.NOSE.value].visibility > 0.5:
            parts.append("Baş/Head")
        
        # Omuzlar / Shoulders
        if (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility > 0.5 and 
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility > 0.5):
            parts.append("Omuzlar/Shoulders")
        
        # Dirsekler / Elbows
        if (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility > 0.5 and 
            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].visibility > 0.5):
            parts.append("Dirsekler/Elbows")
        
        # Kalçalar / Hips
        if (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility > 0.5 and 
            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].visibility > 0.5):
            parts.append("Kalçalar/Hips")
        
        # Dizler / Knees
        if (landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility > 0.5 and 
            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].visibility > 0.5):
            parts.append("Dizler/Knees")
        
        return parts
    
    def analyze_head_neck(self, landmarks):
        """Baş ve boyun analizi / Head and neck analysis"""
        feedback = []
        
        nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
        left_ear = landmarks[mp_pose.PoseLandmark.LEFT_EAR.value]
        right_ear = landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        
        # Baş eğimi / Head tilt
        ear_center_x = (left_ear.x + right_ear.x) / 2
        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
        
        head_offset = abs(nose.x - shoulder_center_x)
        
        if head_offset > 0.08:
            if nose.x < shoulder_center_x:
                feedback.append("🔍 Boyun: Sola eğik / Neck: Tilted left")
            else:
                feedback.append("🔍 Boyun: Sağa eğik / Neck: Tilted right")
        else:
            feedback.append("🔍 Boyun: Merkezi pozisyon / Neck: Centered")
        
        # İleri baş pozisyonu / Forward head posture
        shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
        if nose.y > shoulder_center_y - 0.08:
            feedback.append("⚠️ İleri baş pozisyonu tespit edildi / Forward head posture detected")
        
        return feedback
    
    def analyze_shoulders(self, landmarks):
        """Omuz analizi / Shoulder analysis"""
        feedback = []
        
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        
        # Omuz seviyesi / Shoulder level
        height_diff = abs(left_shoulder.y - right_shoulder.y)
        
        if height_diff > 0.04:
            if left_shoulder.y < right_shoulder.y:
                feedback.append("🔍 Omuzlar: Sol omuz yüksek / Shoulders: Left shoulder high")
            else:
                feedback.append("🔍 Omuzlar: Sağ omuz yüksek / Shoulders: Right shoulder high")
        else:
            feedback.append("🔍 Omuzlar: Seviyeli / Shoulders: Level")
        
        return feedback
    
    def analyze_torso(self, landmarks):
        """Gövde analizi / Torso analysis"""
        feedback = []
        
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        
        # Gövde eğimi / Torso tilt
        shoulder_center = ((left_shoulder.x + right_shoulder.x) / 2, (left_shoulder.y + right_shoulder.y) / 2)
        hip_center = ((left_hip.x + right_hip.x) / 2, (left_hip.y + right_hip.y) / 2)
        
        torso_tilt = abs(shoulder_center[0] - hip_center[0])
        
        if torso_tilt > 0.05:
            if shoulder_center[0] < hip_center[0]:
                feedback.append("🔍 Gövde: Sola eğik / Torso: Leaning left")
            else:
                feedback.append("🔍 Gövde: Sağa eğik / Torso: Leaning right")
        else:
            feedback.append("🔍 Gövde: Dik duruş / Torso: Upright")
        
        return feedback
    
    def analyze_hips(self, landmarks):
        """Kalça analizi / Hip analysis"""
        feedback = []
        
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        
        # Kalça seviyesi / Hip level
        height_diff = abs(left_hip.y - right_hip.y)
        
        if height_diff > 0.03:
            if left_hip.y < right_hip.y:
                feedback.append("🔍 Kalçalar: Sol kalça yüksek / Hips: Left hip high")
            else:
                feedback.append("🔍 Kalçalar: Sağ kalça yüksek / Hips: Right hip high")
        else:
            feedback.append("🔍 Kalçalar: Seviyeli / Hips: Level")
        
        return feedback
    
    def analyze_legs(self, landmarks):
        """Bacak analizi / Leg analysis"""
        feedback = []
        
        try:
            # Diz açıları / Knee angles
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
            
            if left_knee_angle > 0:
                feedback.append(f"🔍 Sol diz açısı / Left knee angle: {left_knee_angle:.1f}°")
                if left_knee_angle < 160:
                    feedback.append("   ⚠️ Sol diz bükümlü / Left knee bent")
            
            # Sağ diz / Right knee
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            
            right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)
            
            if right_knee_angle > 0:
                feedback.append(f"🔍 Sağ diz açısı / Right knee angle: {right_knee_angle:.1f}°")
                if right_knee_angle < 160:
                    feedback.append("   ⚠️ Sağ diz bükümlü / Right knee bent")
        
        except:
            feedback.append("⚠️ Bacak analizi yapılamadı / Leg analysis failed")
        
        return feedback

# Global analyzer
analyzer = EnhancedPostureAnalyzer()

def process_with_profile(frame, age, height, weight):
    """Profil bilgileriyle işle / Process with profile"""
    # Boş değerleri None'a çevir / Convert empty values to None
    age = int(age) if age and str(age).strip() else None
    height = int(height) if height and str(height).strip() else None
    weight = int(weight) if weight and str(weight).strip() else None
    
    return analyzer.analyze_frame_with_profile(frame, age, height, weight)

# Basit Gradio arayüzü / Simple Gradio interface
def create_interface():
    with gr.Blocks(title="Enhanced Posture Analyzer") as demo:
        gr.Markdown("""
        # 🎯 Enhanced Posture Analyzer
        ## Real-time posture analysis with optional profile information

        **Profile benefits:**
        - **Age**: Age-specific recommendations and risk factors
        - **Height & Weight**: BMI calculation and posture load assessment
        - **All optional**: Works perfectly without any profile info
        """)

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 👤 Optional Profile")

                age_input = gr.Number(
                    label="Age / Yaş",
                    value=None,
                    minimum=10,
                    maximum=100
                )

                height_input = gr.Number(
                    label="Height (cm) / Boy (cm)",
                    value=None,
                    minimum=100,
                    maximum=250
                )

                weight_input = gr.Number(
                    label="Weight (kg) / Kilo (kg)",
                    value=None,
                    minimum=30,
                    maximum=200
                )

                input_video = gr.Image(
                    sources=["webcam"],
                    streaming=True,
                    label="📹 Camera Input"
                )

            with gr.Column():
                output_video = gr.Image(
                    streaming=True,
                    label="🎯 Analysis Output"
                )

                feedback_text = gr.Textbox(
                    label="📊 Detailed Analysis",
                    lines=15,
                    interactive=False
                )

        # Canlı işleme / Live processing
        input_video.stream(
            fn=process_with_profile,
            inputs=[input_video, age_input, height_input, weight_input],
            outputs=[output_video, feedback_text],
            stream_every=0.1
        )

    return demo

demo = create_interface()

if __name__ == "__main__":
    demo.launch(
        share=False,
        server_port=7863,
        show_error=True
    )
