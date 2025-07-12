# Minimal Postür Analiz Sistemi / Minimal Posture Analysis System
import cv2
import mediapipe as mp
import gradio as gr
import numpy as np

# MediaPipe başlatma / Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def analyze_posture(image):
    """Postür analiz fonksiyonu / Posture analysis function"""
    if image is None:
        return None, "❌ Görüntü yok / No image"
    
    # MediaPipe Pose başlat / Initialize MediaPipe Pose
    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:
        
        # BGR'den RGB'ye çevir / Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Pose tespiti / Pose detection
        results = pose.process(rgb_image)
        
        # Çizim için BGR'ye geri çevir / Convert back to BGR
        output_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        
        feedback = []
        
        if results.pose_landmarks:
            # Landmark'ları çiz / Draw landmarks
            mp_drawing.draw_landmarks(
                output_image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )
            
            landmarks = results.pose_landmarks.landmark
            
            # Görünür parçaları kontrol et / Check visible parts
            visible_parts = []
            
            # Baş kontrolü / Head check
            if landmarks[mp_pose.PoseLandmark.NOSE.value].visibility > 0.5:
                visible_parts.append("Baş/Head")
            
            # Omuz kontrolü / Shoulder check
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            
            if left_shoulder.visibility > 0.5 and right_shoulder.visibility > 0.5:
                visible_parts.append("Omuzlar/Shoulders")
                
                # Omuz seviyesi / Shoulder level
                shoulder_diff = abs(left_shoulder.y - right_shoulder.y)
                if shoulder_diff > 0.05:
                    if left_shoulder.y < right_shoulder.y:
                        feedback.append("⚠️ Sol omuz yüksek / Left shoulder high")
                    else:
                        feedback.append("⚠️ Sağ omuz yüksek / Right shoulder high")
                else:
                    feedback.append("✅ Omuzlar seviyeli / Shoulders level")
            
            # Dirsek kontrolü / Elbow check
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
            
            if left_elbow.visibility > 0.5 and right_elbow.visibility > 0.5:
                visible_parts.append("Dirsekler/Elbows")
                
                # Basit dirsek açısı tahmini / Simple elbow angle estimation
                if left_elbow.visibility > 0.7:
                    feedback.append("📐 Sol dirsek görünür / Left elbow visible")
                if right_elbow.visibility > 0.7:
                    feedback.append("📐 Sağ dirsek görünür / Right elbow visible")
            
            # Kalça kontrolü / Hip check
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
            
            if left_hip.visibility > 0.5 and right_hip.visibility > 0.5:
                visible_parts.append("Kalçalar/Hips")
                
                # Kalça seviyesi / Hip level
                hip_diff = abs(left_hip.y - right_hip.y)
                if hip_diff > 0.03:
                    if left_hip.y < right_hip.y:
                        feedback.append("⚠️ Sol kalça yüksek / Left hip high")
                    else:
                        feedback.append("⚠️ Sağ kalça yüksek / Right hip high")
                else:
                    feedback.append("✅ Kalçalar seviyeli / Hips level")
            
            # Boyun pozisyonu / Neck position
            nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
            if nose.visibility > 0.5 and left_shoulder.visibility > 0.5 and right_shoulder.visibility > 0.5:
                shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
                head_offset = abs(nose.x - shoulder_center_x)
                
                if head_offset > 0.08:
                    if nose.x < shoulder_center_x:
                        feedback.append("🔍 Boyun sola eğik / Neck tilted left")
                    else:
                        feedback.append("🔍 Boyun sağa eğik / Neck tilted right")
                else:
                    feedback.append("🔍 Boyun merkezi / Neck centered")
            
            # Görünür parçaları listele / List visible parts
            if visible_parts:
                feedback.insert(0, f"✅ Görünen: {', '.join(visible_parts)}")
                feedback.insert(1, "")
        else:
            feedback.append("❌ Vücut tespit edilemedi / Body not detected")
            feedback.append("📍 Kameraya daha yakın durun / Stand closer to camera")
        
        return output_image, "\n".join(feedback)

# Gradio arayüzü / Gradio interface
iface = gr.Interface(
    fn=analyze_posture,
    inputs=gr.Image(sources=["webcam"]),
    outputs=[
        gr.Image(label="🎯 Analiz / Analysis"),
        gr.Textbox(label="📊 Geri Bildirim / Feedback", lines=8)
    ],
    title="🎯 Minimal Posture Analyzer",
    description="Basit postür analizi - kameranın gördüklerini anında değerlendirir",
    live=True
)

if __name__ == "__main__":
    iface.launch(server_port=7865)
