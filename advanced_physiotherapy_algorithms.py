# Gelişmiş Fizyoterapi Algoritmaları / Advanced Physiotherapy Algorithms
import numpy as np
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import mediapipe as mp

class MovementPattern(Enum):
    """Hareket paternleri / Movement patterns"""
    NORMAL = "normal"
    COMPENSATORY = "compensatory"
    RESTRICTED = "restricted"
    HYPERMOBILE = "hypermobile"

class RiskLevel(Enum):
    """Risk seviyeleri / Risk levels"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class BiomechanicalAnalysis:
    """Biyomekanik analiz sonuçları / Biomechanical analysis results"""
    joint_angles: Dict[str, float]
    movement_patterns: Dict[str, MovementPattern]
    risk_assessment: Dict[str, RiskLevel]
    compensation_patterns: List[str]
    functional_scores: Dict[str, float]

class AdvancedPhysiotherapyAnalyzer:
    """Gelişmiş fizyoterapi analiz sınıfı / Advanced physiotherapy analyzer class"""
    
    def __init__(self):
        # Normal eklem açı aralıkları (derece) / Normal joint angle ranges (degrees)
        self.normal_ranges = {
            'cervical_flexion': (0, 50),
            'cervical_extension': (0, 60),
            'shoulder_flexion': (0, 180),
            'shoulder_abduction': (0, 180),
            'elbow_flexion': (0, 145),
            'hip_flexion': (0, 120),
            'knee_flexion': (0, 135),
            'ankle_dorsiflexion': (0, 20),
            'ankle_plantarflexion': (0, 50)
        }
        
        # Kritik postür parametreleri / Critical posture parameters
        self.critical_thresholds = {
            'forward_head_ratio': 0.25,
            'shoulder_protraction': 0.15,
            'pelvic_tilt_angle': 15.0,
            'knee_valgus_angle': 10.0,
            'spinal_curvature': 0.2
        }
    
    def calculate_3d_angle(self, point1: Tuple[float, float, float], 
                          point2: Tuple[float, float, float], 
                          point3: Tuple[float, float, float]) -> float:
        """3D uzayda açı hesapla / Calculate 3D angle"""
        try:
            # 3D vektörler / 3D vectors
            v1 = np.array([point1[0] - point2[0], point1[1] - point2[1], point1[2] - point2[2]])
            v2 = np.array([point3[0] - point2[0], point3[1] - point2[1], point3[2] - point2[2]])
            
            # Açı hesaplama / Angle calculation
            cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            cos_angle = np.clip(cos_angle, -1.0, 1.0)
            angle = np.arccos(cos_angle)
            
            return np.degrees(angle)
        except:
            return 0.0
    
    def analyze_cervical_spine(self, landmarks) -> Dict[str, float]:
        """Servikal omurga analizi / Cervical spine analysis"""
        try:
            # Landmark'ları al / Get landmarks
            nose = landmarks[mp.solutions.pose.PoseLandmark.NOSE.value]
            left_ear = landmarks[mp.solutions.pose.PoseLandmark.LEFT_EAR.value]
            right_ear = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_EAR.value]
            left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
            
            # Orta noktaları hesapla / Calculate midpoints
            ear_center = ((left_ear.x + right_ear.x) / 2, (left_ear.y + right_ear.y) / 2)
            shoulder_center = ((left_shoulder.x + right_shoulder.x) / 2, (left_shoulder.y + right_shoulder.y) / 2)
            
            # Forward head posture analizi / Forward head posture analysis
            head_forward_distance = abs(ear_center[0] - shoulder_center[0])
            vertical_distance = abs(ear_center[1] - shoulder_center[1])
            
            forward_head_ratio = head_forward_distance / vertical_distance if vertical_distance > 0 else 0
            
            # Boyun eğimi / Neck inclination
            neck_angle = math.degrees(math.atan2(
                ear_center[1] - shoulder_center[1],
                ear_center[0] - shoulder_center[0]
            ))
            
            return {
                'forward_head_ratio': forward_head_ratio,
                'neck_inclination': abs(neck_angle),
                'cervical_alignment': 100 - (forward_head_ratio * 100)
            }
        except:
            return {}
    
    def analyze_shoulder_complex(self, landmarks) -> Dict[str, float]:
        """Omuz kompleksi analizi / Shoulder complex analysis"""
        try:
            left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
            left_elbow = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value]
            right_elbow = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value]
            left_wrist = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value]
            right_wrist = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value]
            
            # Omuz yükseklik farkı / Shoulder height difference
            shoulder_height_diff = abs(left_shoulder.y - right_shoulder.y)
            
            # Omuz protraksiyon analizi / Shoulder protraction analysis
            shoulder_width = abs(left_shoulder.x - right_shoulder.x)
            elbow_width = abs(left_elbow.x - right_elbow.x)
            protraction_ratio = elbow_width / shoulder_width if shoulder_width > 0 else 0
            
            # Kol açıları / Arm angles
            left_arm_angle = self.calculate_3d_angle(
                (left_shoulder.x, left_shoulder.y, left_shoulder.z),
                (left_elbow.x, left_elbow.y, left_elbow.z),
                (left_wrist.x, left_wrist.y, left_wrist.z)
            )
            
            right_arm_angle = self.calculate_3d_angle(
                (right_shoulder.x, right_shoulder.y, right_shoulder.z),
                (right_elbow.x, right_elbow.y, right_elbow.z),
                (right_wrist.x, right_wrist.y, right_wrist.z)
            )
            
            return {
                'shoulder_asymmetry': shoulder_height_diff * 100,
                'shoulder_protraction': protraction_ratio,
                'left_elbow_angle': left_arm_angle,
                'right_elbow_angle': right_arm_angle,
                'arm_angle_difference': abs(left_arm_angle - right_arm_angle)
            }
        except:
            return {}
    
    def analyze_spinal_alignment(self, landmarks) -> Dict[str, float]:
        """Spinal hizalama analizi / Spinal alignment analysis"""
        try:
            # Spinal landmark'lar / Spinal landmarks
            nose = landmarks[mp.solutions.pose.PoseLandmark.NOSE.value]
            left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
            left_hip = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]
            
            # Orta noktalar / Midpoints
            shoulder_center = ((left_shoulder.x + right_shoulder.x) / 2, (left_shoulder.y + right_shoulder.y) / 2)
            hip_center = ((left_hip.x + right_hip.x) / 2, (left_hip.y + right_hip.y) / 2)
            
            # Spinal eğrilik / Spinal curvature
            spinal_deviation = abs(shoulder_center[0] - hip_center[0])
            spinal_length = abs(shoulder_center[1] - hip_center[1])
            curvature_ratio = spinal_deviation / spinal_length if spinal_length > 0 else 0
            
            # Lateral eğim / Lateral tilt
            lateral_tilt = math.degrees(math.atan2(
                shoulder_center[1] - hip_center[1],
                shoulder_center[0] - hip_center[0]
            ))
            
            return {
                'spinal_curvature': curvature_ratio,
                'lateral_tilt': abs(lateral_tilt),
                'spinal_alignment_score': max(0, 100 - (curvature_ratio * 500))
            }
        except:
            return {}
    
    def analyze_pelvic_alignment(self, landmarks) -> Dict[str, float]:
        """Pelvik hizalama analizi / Pelvic alignment analysis"""
        try:
            left_hip = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]
            left_knee = landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value]
            right_knee = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value]
            
            # Pelvik eğim / Pelvic tilt
            hip_height_diff = abs(left_hip.y - right_hip.y)
            pelvic_tilt_angle = math.degrees(math.atan2(
                right_hip.y - left_hip.y,
                right_hip.x - left_hip.x
            ))
            
            # Kalça-diz hizalama / Hip-knee alignment
            left_hip_knee_alignment = abs(left_hip.x - left_knee.x)
            right_hip_knee_alignment = abs(right_hip.x - right_knee.x)
            
            return {
                'pelvic_tilt_angle': abs(pelvic_tilt_angle),
                'hip_asymmetry': hip_height_diff * 100,
                'left_hip_knee_alignment': left_hip_knee_alignment,
                'right_hip_knee_alignment': right_hip_knee_alignment,
                'pelvic_stability_score': max(0, 100 - (abs(pelvic_tilt_angle) * 5))
            }
        except:
            return {}
    
    def analyze_lower_extremity(self, landmarks) -> Dict[str, float]:
        """Alt ekstremite analizi / Lower extremity analysis"""
        try:
            left_hip = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]
            left_knee = landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value]
            right_knee = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value]
            left_ankle = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]
            right_ankle = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value]
            
            # Diz açıları / Knee angles
            left_knee_angle = self.calculate_3d_angle(
                (left_hip.x, left_hip.y, left_hip.z),
                (left_knee.x, left_knee.y, left_knee.z),
                (left_ankle.x, left_ankle.y, left_ankle.z)
            )
            
            right_knee_angle = self.calculate_3d_angle(
                (right_hip.x, right_hip.y, right_hip.z),
                (right_knee.x, right_knee.y, right_knee.z),
                (right_ankle.x, right_ankle.y, right_ankle.z)
            )
            
            # Diz valgus/varus analizi / Knee valgus/varus analysis
            left_knee_valgus = abs(left_hip.x - left_knee.x) - abs(left_knee.x - left_ankle.x)
            right_knee_valgus = abs(right_hip.x - right_knee.x) - abs(right_knee.x - right_ankle.x)
            
            # Ayak pozisyonu / Foot position
            foot_width = abs(left_ankle.x - right_ankle.x)
            hip_width = abs(left_hip.x - right_hip.x)
            stance_width_ratio = foot_width / hip_width if hip_width > 0 else 0
            
            return {
                'left_knee_angle': left_knee_angle,
                'right_knee_angle': right_knee_angle,
                'knee_angle_asymmetry': abs(left_knee_angle - right_knee_angle),
                'left_knee_valgus': left_knee_valgus,
                'right_knee_valgus': right_knee_valgus,
                'stance_width_ratio': stance_width_ratio,
                'lower_extremity_symmetry': max(0, 100 - (abs(left_knee_angle - right_knee_angle) * 2))
            }
        except:
            return {}
    
    def assess_movement_quality(self, analysis_results: Dict[str, Dict]) -> Dict[str, MovementPattern]:
        """Hareket kalitesi değerlendirmesi / Movement quality assessment"""
        patterns = {}
        
        # Servikal hareket kalitesi / Cervical movement quality
        cervical = analysis_results.get('cervical', {})
        if cervical.get('forward_head_ratio', 0) > 0.2:
            patterns['cervical'] = MovementPattern.COMPENSATORY
        elif cervical.get('cervical_alignment', 100) < 70:
            patterns['cervical'] = MovementPattern.RESTRICTED
        else:
            patterns['cervical'] = MovementPattern.NORMAL
        
        # Omuz hareket kalitesi / Shoulder movement quality
        shoulder = analysis_results.get('shoulder', {})
        if shoulder.get('shoulder_protraction', 0) > 0.15:
            patterns['shoulder'] = MovementPattern.COMPENSATORY
        elif shoulder.get('arm_angle_difference', 0) > 15:
            patterns['shoulder'] = MovementPattern.RESTRICTED
        else:
            patterns['shoulder'] = MovementPattern.NORMAL
        
        # Spinal hareket kalitesi / Spinal movement quality
        spinal = analysis_results.get('spinal', {})
        if spinal.get('spinal_curvature', 0) > 0.2:
            patterns['spinal'] = MovementPattern.COMPENSATORY
        elif spinal.get('spinal_alignment_score', 100) < 60:
            patterns['spinal'] = MovementPattern.RESTRICTED
        else:
            patterns['spinal'] = MovementPattern.NORMAL
        
        return patterns
    
    def assess_injury_risk(self, analysis_results: Dict[str, Dict]) -> Dict[str, RiskLevel]:
        """Yaralanma riski değerlendirmesi / Injury risk assessment"""
        risks = {}
        
        # Boyun yaralanma riski / Neck injury risk
        cervical = analysis_results.get('cervical', {})
        if cervical.get('forward_head_ratio', 0) > 0.3:
            risks['neck'] = RiskLevel.HIGH
        elif cervical.get('forward_head_ratio', 0) > 0.2:
            risks['neck'] = RiskLevel.MODERATE
        else:
            risks['neck'] = RiskLevel.LOW
        
        # Omuz yaralanma riski / Shoulder injury risk
        shoulder = analysis_results.get('shoulder', {})
        if shoulder.get('shoulder_asymmetry', 0) > 15:
            risks['shoulder'] = RiskLevel.HIGH
        elif shoulder.get('shoulder_protraction', 0) > 0.15:
            risks['shoulder'] = RiskLevel.MODERATE
        else:
            risks['shoulder'] = RiskLevel.LOW
        
        # Bel yaralanma riski / Lower back injury risk
        spinal = analysis_results.get('spinal', {})
        pelvic = analysis_results.get('pelvic', {})
        if (spinal.get('spinal_curvature', 0) > 0.25 or 
            pelvic.get('pelvic_tilt_angle', 0) > 20):
            risks['lower_back'] = RiskLevel.HIGH
        elif (spinal.get('spinal_curvature', 0) > 0.15 or 
              pelvic.get('pelvic_tilt_angle', 0) > 10):
            risks['lower_back'] = RiskLevel.MODERATE
        else:
            risks['lower_back'] = RiskLevel.LOW
        
        # Diz yaralanma riski / Knee injury risk
        lower_ext = analysis_results.get('lower_extremity', {})
        if lower_ext.get('knee_angle_asymmetry', 0) > 20:
            risks['knee'] = RiskLevel.HIGH
        elif lower_ext.get('knee_angle_asymmetry', 0) > 10:
            risks['knee'] = RiskLevel.MODERATE
        else:
            risks['knee'] = RiskLevel.LOW
        
        return risks
    
    def comprehensive_analysis(self, landmarks) -> BiomechanicalAnalysis:
        """Kapsamlı biyomekanik analiz / Comprehensive biomechanical analysis"""
        # Tüm analizleri yap / Perform all analyses
        cervical_analysis = self.analyze_cervical_spine(landmarks)
        shoulder_analysis = self.analyze_shoulder_complex(landmarks)
        spinal_analysis = self.analyze_spinal_alignment(landmarks)
        pelvic_analysis = self.analyze_pelvic_alignment(landmarks)
        lower_ext_analysis = self.analyze_lower_extremity(landmarks)
        
        # Sonuçları birleştir / Combine results
        all_results = {
            'cervical': cervical_analysis,
            'shoulder': shoulder_analysis,
            'spinal': spinal_analysis,
            'pelvic': pelvic_analysis,
            'lower_extremity': lower_ext_analysis
        }
        
        # Hareket kalitesi ve risk değerlendirmesi / Movement quality and risk assessment
        movement_patterns = self.assess_movement_quality(all_results)
        risk_assessment = self.assess_injury_risk(all_results)
        
        # Kompensasyon paternlerini tespit et / Detect compensation patterns
        compensation_patterns = self.detect_compensation_patterns(all_results)
        
        # Fonksiyonel skorları hesapla / Calculate functional scores
        functional_scores = self.calculate_functional_scores(all_results)
        
        # Tüm eklem açılarını birleştir / Combine all joint angles
        joint_angles = {}
        for category, analysis in all_results.items():
            for key, value in analysis.items():
                joint_angles[f"{category}_{key}"] = value
        
        return BiomechanicalAnalysis(
            joint_angles=joint_angles,
            movement_patterns=movement_patterns,
            risk_assessment=risk_assessment,
            compensation_patterns=compensation_patterns,
            functional_scores=functional_scores
        )
    
    def detect_compensation_patterns(self, analysis_results: Dict[str, Dict]) -> List[str]:
        """Kompensasyon paternlerini tespit et / Detect compensation patterns"""
        patterns = []
        
        cervical = analysis_results.get('cervical', {})
        shoulder = analysis_results.get('shoulder', {})
        spinal = analysis_results.get('spinal', {})
        
        # Upper crossed syndrome
        if (cervical.get('forward_head_ratio', 0) > 0.2 and 
            shoulder.get('shoulder_protraction', 0) > 0.15):
            patterns.append("Upper Crossed Syndrome - Üst çapraz sendrom")
        
        # Lower crossed syndrome
        pelvic = analysis_results.get('pelvic', {})
        if (pelvic.get('pelvic_tilt_angle', 0) > 15 and 
            spinal.get('spinal_curvature', 0) > 0.2):
            patterns.append("Lower Crossed Syndrome - Alt çapraz sendrom")
        
        # Lateral chain dysfunction
        if (shoulder.get('shoulder_asymmetry', 0) > 10 and 
            pelvic.get('hip_asymmetry', 0) > 10):
            patterns.append("Lateral Chain Dysfunction - Lateral zincir disfonksiyonu")
        
        return patterns
    
    def calculate_functional_scores(self, analysis_results: Dict[str, Dict]) -> Dict[str, float]:
        """Fonksiyonel skorları hesapla / Calculate functional scores"""
        scores = {}
        
        # Boyun fonksiyonel skoru / Neck functional score
        cervical = analysis_results.get('cervical', {})
        neck_score = cervical.get('cervical_alignment', 100)
        scores['neck_function'] = max(0, min(100, neck_score))
        
        # Omuz fonksiyonel skoru / Shoulder functional score
        shoulder = analysis_results.get('shoulder', {})
        shoulder_score = 100 - (shoulder.get('shoulder_asymmetry', 0) * 2)
        scores['shoulder_function'] = max(0, min(100, shoulder_score))
        
        # Spinal fonksiyonel skor / Spinal functional score
        spinal = analysis_results.get('spinal', {})
        spinal_score = spinal.get('spinal_alignment_score', 100)
        scores['spinal_function'] = max(0, min(100, spinal_score))
        
        # Pelvik fonksiyonel skor / Pelvic functional score
        pelvic = analysis_results.get('pelvic', {})
        pelvic_score = pelvic.get('pelvic_stability_score', 100)
        scores['pelvic_function'] = max(0, min(100, pelvic_score))
        
        # Alt ekstremite fonksiyonel skoru / Lower extremity functional score
        lower_ext = analysis_results.get('lower_extremity', {})
        lower_ext_score = lower_ext.get('lower_extremity_symmetry', 100)
        scores['lower_extremity_function'] = max(0, min(100, lower_ext_score))
        
        # Genel fonksiyonel skor / Overall functional score
        scores['overall_function'] = np.mean(list(scores.values()))
        
        return scores
