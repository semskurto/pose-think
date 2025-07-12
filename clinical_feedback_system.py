# Klinik Geri Bildirim Sistemi / Clinical Feedback System
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta

class ExerciseType(Enum):
    """Egzersiz türleri / Exercise types"""
    STRENGTHENING = "strengthening"
    STRETCHING = "stretching"
    MOBILITY = "mobility"
    STABILITY = "stability"
    POSTURAL = "postural"
    CARDIOVASCULAR = "cardiovascular"

class ExerciseDifficulty(Enum):
    """Egzersiz zorluk seviyeleri / Exercise difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class Exercise:
    """Egzersiz veri yapısı / Exercise data structure"""
    name: str
    description: str
    duration: str
    repetitions: str
    sets: int
    exercise_type: ExerciseType
    difficulty: ExerciseDifficulty
    target_areas: List[str]
    precautions: List[str]
    benefits: List[str]

@dataclass
class TreatmentPlan:
    """Tedavi planı veri yapısı / Treatment plan data structure"""
    patient_id: str
    assessment_date: datetime
    primary_issues: List[str]
    secondary_issues: List[str]
    short_term_goals: List[str]
    long_term_goals: List[str]
    exercises: List[Exercise]
    follow_up_schedule: List[str]
    precautions: List[str]
    expected_outcomes: List[str]

class ClinicalFeedbackSystem:
    """Klinik geri bildirim sistemi / Clinical feedback system"""
    
    def __init__(self):
        self.exercise_database = self._initialize_exercise_database()
        self.treatment_protocols = self._initialize_treatment_protocols()
    
    def _initialize_exercise_database(self) -> Dict[str, List[Exercise]]:
        """Egzersiz veritabanını başlat / Initialize exercise database"""
        exercises = {
            'neck': [
                Exercise(
                    name="Boyun İzometrik Egzersizi",
                    description="Elinizi alnınıza koyun ve başınızı öne doğru itmeye çalışırken elinizle direnç uygulayın",
                    duration="10 saniye",
                    repetitions="10 tekrar",
                    sets=3,
                    exercise_type=ExerciseType.STRENGTHENING,
                    difficulty=ExerciseDifficulty.BEGINNER,
                    target_areas=["Derin boyun fleksörleri", "Servikal stabilizatörler"],
                    precautions=["Ağrı hissederseniz durdurun", "Yavaş ve kontrollü hareket yapın"],
                    benefits=["Boyun kas gücünü artırır", "Postür düzelir", "Baş ağrısı azalır"]
                ),
                Exercise(
                    name="Boyun Rotasyon Germe",
                    description="Başınızı yavaşça sağa çevirin, 30 saniye tutun, sonra sola çevirin",
                    duration="30 saniye",
                    repetitions="Her yöne 3 tekrar",
                    sets=2,
                    exercise_type=ExerciseType.STRETCHING,
                    difficulty=ExerciseDifficulty.BEGINNER,
                    target_areas=["Boyun rotasyon kasları", "Suboksipital kaslar"],
                    precautions=["Zorlamayın", "Ağrı hissederseniz durdurun"],
                    benefits=["Boyun hareketliliğini artırır", "Kas gerginliğini azaltır"]
                )
            ],
            'shoulder': [
                Exercise(
                    name="Omuz Blade Sıkıştırma",
                    description="Kollarınızı yanınızda tutarak omuz bıçaklarınızı arkaya doğru sıkıştırın",
                    duration="5 saniye",
                    repetitions="15 tekrar",
                    sets=3,
                    exercise_type=ExerciseType.STRENGTHENING,
                    difficulty=ExerciseDifficulty.BEGINNER,
                    target_areas=["Rhomboidler", "Orta trapez", "Alt trapez"],
                    precautions=["Omuzları yukarı kaldırmayın", "Yavaş hareket yapın"],
                    benefits=["Postürü düzeltir", "Omuz stabilitesini artırır"]
                ),
                Exercise(
                    name="Duvar İtme Egzersizi",
                    description="Duvara karşı durarak kollarınızla duvarı itin, sanki şınav yapıyormuş gibi",
                    duration="Sürekli",
                    repetitions="15 tekrar",
                    sets=3,
                    exercise_type=ExerciseType.STRENGTHENING,
                    difficulty=ExerciseDifficulty.INTERMEDIATE,
                    target_areas=["Serratus anterior", "Pektoraller", "Deltoidler"],
                    precautions=["Bel eğmeyin", "Core kaslarınızı aktif tutun"],
                    benefits=["Omuz stabilitesini artırır", "Postürü düzeltir"]
                )
            ],
            'back': [
                Exercise(
                    name="Cat-Cow Egzersizi",
                    description="Dört ayak üzerinde durarak sırtınızı yukarı kaldırın (kedi), sonra aşağı indirin (inek)",
                    duration="Yavaş hareket",
                    repetitions="10 tekrar",
                    sets=2,
                    exercise_type=ExerciseType.MOBILITY,
                    difficulty=ExerciseDifficulty.BEGINNER,
                    target_areas=["Spinal mobilite", "Core kaslar"],
                    precautions=["Yavaş hareket yapın", "Ağrı hissederseniz durdurun"],
                    benefits=["Spinal mobilitesini artırır", "Core kasları güçlendirir"]
                ),
                Exercise(
                    name="Bird Dog Egzersizi",
                    description="Dört ayak üzerinde durarak karşı kol ve bacağınızı kaldırın",
                    duration="10 saniye",
                    repetitions="Her taraf 10 tekrar",
                    sets=3,
                    exercise_type=ExerciseType.STABILITY,
                    difficulty=ExerciseDifficulty.INTERMEDIATE,
                    target_areas=["Core stabilizatörler", "Gluteal kaslar", "Spinal erektorler"],
                    precautions=["Dengeyi koruyun", "Kalça seviyesini koruyun"],
                    benefits=["Core stabilitesini artırır", "Koordinasyonu geliştirir"]
                )
            ],
            'hip': [
                Exercise(
                    name="Kalça Flexor Germe",
                    description="Hamle pozisyonunda ön bacağınızı 90 derece bükerek arka bacağınızı gerin",
                    duration="30 saniye",
                    repetitions="Her bacak 3 tekrar",
                    sets=2,
                    exercise_type=ExerciseType.STRETCHING,
                    difficulty=ExerciseDifficulty.BEGINNER,
                    target_areas=["Hip flexörler", "Psoas", "İliotibial band"],
                    precautions=["Yavaş gerin", "Dengeyi koruyun"],
                    benefits=["Kalça mobilitesini artırır", "Bel ağrısını azaltır"]
                ),
                Exercise(
                    name="Glute Bridge",
                    description="Sırt üstü yatarak dizlerinizi büküp kalçanızı yukarı kaldırın",
                    duration="5 saniye",
                    repetitions="15 tekrar",
                    sets=3,
                    exercise_type=ExerciseType.STRENGTHENING,
                    difficulty=ExerciseDifficulty.BEGINNER,
                    target_areas=["Gluteal kaslar", "Hamstring", "Core"],
                    precautions=["Bel eğmeyin", "Kalçayı sıkın"],
                    benefits=["Kalça gücünü artırır", "Bel stabilitesini sağlar"]
                )
            ],
            'knee': [
                Exercise(
                    name="Quadriceps Germe",
                    description="Ayakta durarak ayak bileğinizi tutup topuğunuzu kalçanıza doğru çekin",
                    duration="30 saniye",
                    repetitions="Her bacak 3 tekrar",
                    sets=2,
                    exercise_type=ExerciseType.STRETCHING,
                    difficulty=ExerciseDifficulty.BEGINNER,
                    target_areas=["Quadriceps", "Hip flexörler"],
                    precautions=["Dengeyi koruyun", "Zorlamayın"],
                    benefits=["Diz mobilitesini artırır", "Kas gerginliğini azaltır"]
                ),
                Exercise(
                    name="Tek Bacak Denge",
                    description="Tek ayak üzerinde durarak dengeyi koruyun",
                    duration="30 saniye",
                    repetitions="Her bacak 3 tekrar",
                    sets=2,
                    exercise_type=ExerciseType.STABILITY,
                    difficulty=ExerciseDifficulty.INTERMEDIATE,
                    target_areas=["Propriosepsiyon", "Diz stabilizatörleri", "Ayak bileği"],
                    precautions=["Güvenli bir yerde yapın", "Gerekirse tutunun"],
                    benefits=["Denge gelişir", "Yaralanma riskini azaltır"]
                )
            ]
        }
        return exercises
    
    def _initialize_treatment_protocols(self) -> Dict[str, Dict]:
        """Tedavi protokollerini başlat / Initialize treatment protocols"""
        protocols = {
            'forward_head_posture': {
                'primary_exercises': ['neck', 'shoulder'],
                'duration_weeks': 6,
                'frequency': '3x/hafta',
                'progression': 'Haftalık zorluk artışı'
            },
            'rounded_shoulders': {
                'primary_exercises': ['shoulder', 'back'],
                'duration_weeks': 8,
                'frequency': '4x/hafta',
                'progression': 'İki haftalık zorluk artışı'
            },
            'lower_crossed_syndrome': {
                'primary_exercises': ['hip', 'back'],
                'duration_weeks': 10,
                'frequency': '5x/hafta',
                'progression': 'Progresif yüklenme'
            },
            'knee_dysfunction': {
                'primary_exercises': ['knee', 'hip'],
                'duration_weeks': 6,
                'frequency': '3x/hafta',
                'progression': 'Fonksiyonel progresyon'
            }
        }
        return protocols
    
    def generate_personalized_treatment_plan(self, 
                                           assessment_results: Dict,
                                           patient_profile: Dict) -> TreatmentPlan:
        """Kişiselleştirilmiş tedavi planı oluştur / Generate personalized treatment plan"""
        
        # Birincil sorunları belirle / Identify primary issues
        primary_issues = self._identify_primary_issues(assessment_results)
        secondary_issues = self._identify_secondary_issues(assessment_results)
        
        # Egzersizleri seç / Select exercises
        selected_exercises = self._select_exercises(primary_issues, patient_profile)
        
        # Hedefleri belirle / Set goals
        short_term_goals = self._set_short_term_goals(primary_issues)
        long_term_goals = self._set_long_term_goals(primary_issues)
        
        # Takip programını oluştur / Create follow-up schedule
        follow_up_schedule = self._create_follow_up_schedule(primary_issues)
        
        # Önlemleri belirle / Set precautions
        precautions = self._set_precautions(assessment_results, patient_profile)
        
        # Beklenen sonuçları belirle / Set expected outcomes
        expected_outcomes = self._set_expected_outcomes(primary_issues)
        
        return TreatmentPlan(
            patient_id=patient_profile.get('id', 'anonymous'),
            assessment_date=datetime.now(),
            primary_issues=primary_issues,
            secondary_issues=secondary_issues,
            short_term_goals=short_term_goals,
            long_term_goals=long_term_goals,
            exercises=selected_exercises,
            follow_up_schedule=follow_up_schedule,
            precautions=precautions,
            expected_outcomes=expected_outcomes
        )
    
    def _identify_primary_issues(self, assessment_results: Dict) -> List[str]:
        """Birincil sorunları tespit et / Identify primary issues"""
        issues = []
        
        # Risk seviyelerine göre öncelik ver / Prioritize by risk levels
        for body_part, risk_level in assessment_results.get('risk_assessment', {}).items():
            if risk_level.value == 'high':
                issues.append(f"Yüksek risk: {body_part}")
            elif risk_level.value == 'moderate':
                issues.append(f"Orta risk: {body_part}")
        
        # Kompensasyon paternlerini ekle / Add compensation patterns
        compensation_patterns = assessment_results.get('compensation_patterns', [])
        issues.extend(compensation_patterns)
        
        return issues[:5]  # En fazla 5 birincil sorun
    
    def _identify_secondary_issues(self, assessment_results: Dict) -> List[str]:
        """İkincil sorunları tespit et / Identify secondary issues"""
        issues = []
        
        # Düşük risk faktörleri / Low risk factors
        for body_part, risk_level in assessment_results.get('risk_assessment', {}).items():
            if risk_level.value == 'low':
                issues.append(f"Koruyucu: {body_part}")
        
        # Fonksiyonel skorlar / Functional scores
        for area, score in assessment_results.get('functional_scores', {}).items():
            if 70 <= score < 85:
                issues.append(f"Geliştirilmesi gereken: {area}")
        
        return issues[:3]  # En fazla 3 ikincil sorun
    
    def _select_exercises(self, primary_issues: List[str], patient_profile: Dict) -> List[Exercise]:
        """Egzersizleri seç / Select exercises"""
        selected_exercises = []
        
        # Hasta profiline göre zorluk seviyesi belirle / Determine difficulty based on patient profile
        experience_level = patient_profile.get('exercise_experience', 'beginner')
        if experience_level == 'advanced':
            target_difficulty = ExerciseDifficulty.ADVANCED
        elif experience_level == 'intermediate':
            target_difficulty = ExerciseDifficulty.INTERMEDIATE
        else:
            target_difficulty = ExerciseDifficulty.BEGINNER
        
        # Her birincil sorun için egzersiz seç / Select exercises for each primary issue
        for issue in primary_issues:
            if 'neck' in issue.lower() or 'boyun' in issue.lower():
                exercises = self.exercise_database.get('neck', [])
                selected_exercises.extend([ex for ex in exercises if ex.difficulty == target_difficulty][:2])
            
            if 'shoulder' in issue.lower() or 'omuz' in issue.lower():
                exercises = self.exercise_database.get('shoulder', [])
                selected_exercises.extend([ex for ex in exercises if ex.difficulty == target_difficulty][:2])
            
            if 'back' in issue.lower() or 'bel' in issue.lower() or 'spinal' in issue.lower():
                exercises = self.exercise_database.get('back', [])
                selected_exercises.extend([ex for ex in exercises if ex.difficulty == target_difficulty][:2])
            
            if 'hip' in issue.lower() or 'kalça' in issue.lower():
                exercises = self.exercise_database.get('hip', [])
                selected_exercises.extend([ex for ex in exercises if ex.difficulty == target_difficulty][:2])
            
            if 'knee' in issue.lower() or 'diz' in issue.lower():
                exercises = self.exercise_database.get('knee', [])
                selected_exercises.extend([ex for ex in exercises if ex.difficulty == target_difficulty][:2])
        
        # Tekrarları kaldır ve maksimum 8 egzersiz seç / Remove duplicates and select max 8 exercises
        unique_exercises = list({ex.name: ex for ex in selected_exercises}.values())
        return unique_exercises[:8]
    
    def _set_short_term_goals(self, primary_issues: List[str]) -> List[str]:
        """Kısa vadeli hedefleri belirle / Set short-term goals"""
        goals = [
            "2 hafta içinde ağrı seviyesini %30 azaltmak",
            "4 hafta içinde postür farkındalığını artırmak",
            "6 hafta içinde günlük aktivitelerde rahatlık sağlamak",
            "Egzersiz rutinini günlük yaşama entegre etmek"
        ]
        return goals
    
    def _set_long_term_goals(self, primary_issues: List[str]) -> List[str]:
        """Uzun vadeli hedefleri belirle / Set long-term goals"""
        goals = [
            "3 ay içinde optimal postür pozisyonunu korumak",
            "6 ay içinde yaralanma riskini minimize etmek",
            "1 yıl içinde fonksiyonel kapasiteyi maksimize etmek",
            "Yaşam kalitesini sürdürülebilir şekilde artırmak"
        ]
        return goals
    
    def _create_follow_up_schedule(self, primary_issues: List[str]) -> List[str]:
        """Takip programını oluştur / Create follow-up schedule"""
        schedule = [
            "1. hafta: Günlük egzersiz takibi",
            "2. hafta: İlerleme değerlendirmesi",
            "4. hafta: Orta dönem değerlendirme",
            "8. hafta: Kapsamlı yeniden değerlendirme",
            "12. hafta: Uzun dönem sonuç değerlendirmesi"
        ]
        return schedule
    
    def _set_precautions(self, assessment_results: Dict, patient_profile: Dict) -> List[str]:
        """Önlemleri belirle / Set precautions"""
        precautions = [
            "Ağrı hissederseniz egzersizi durdurun",
            "Egzersizleri yavaş ve kontrollü yapın",
            "Düzenli su içmeyi unutmayın",
            "Egzersiz öncesi ısınma yapın"
        ]
        
        # Yaşa göre özel önlemler / Age-specific precautions
        age = patient_profile.get('age', 30)
        if age > 65:
            precautions.append("Denge egzersizlerinde dikkatli olun")
            precautions.append("Kan basıncınızı kontrol ettirin")
        
        return precautions
    
    def _set_expected_outcomes(self, primary_issues: List[str]) -> List[str]:
        """Beklenen sonuçları belirle / Set expected outcomes"""
        outcomes = [
            "Postür düzelmesi ve ağrı azalması",
            "Günlük aktivitelerde artış",
            "Kas gücü ve esneklik artışı",
            "Yaşam kalitesinde iyileşme",
            "Yaralanma riskinde azalma"
        ]
        return outcomes
    
    def format_treatment_plan_report(self, treatment_plan: TreatmentPlan) -> str:
        """Tedavi planı raporunu formatla / Format treatment plan report"""
        report = f"📋 KİŞİSELLEŞTİRİLMİŞ TEDAVİ PLANI\n"
        report += f"{'='*60}\n\n"
        
        report += f"📅 Değerlendirme Tarihi: {treatment_plan.assessment_date.strftime('%d.%m.%Y')}\n"
        report += f"🆔 Hasta ID: {treatment_plan.patient_id}\n\n"
        
        # Birincil sorunlar / Primary issues
        report += f"🎯 BİRİNCİL SORUNLAR:\n"
        for issue in treatment_plan.primary_issues:
            report += f"• {issue}\n"
        report += "\n"
        
        # Kısa vadeli hedefler / Short-term goals
        report += f"📈 KISA VADELİ HEDEFLER (2-6 hafta):\n"
        for goal in treatment_plan.short_term_goals:
            report += f"• {goal}\n"
        report += "\n"
        
        # Egzersiz programı / Exercise program
        report += f"💪 EGZERSİZ PROGRAMI:\n"
        for i, exercise in enumerate(treatment_plan.exercises, 1):
            report += f"\n{i}. {exercise.name}\n"
            report += f"   📝 Açıklama: {exercise.description}\n"
            report += f"   ⏱️ Süre: {exercise.duration}\n"
            report += f"   🔄 Tekrar: {exercise.repetitions}\n"
            report += f"   📊 Set: {exercise.sets}\n"
            report += f"   🎯 Hedef: {', '.join(exercise.target_areas)}\n"
            report += f"   ⚠️ Dikkat: {', '.join(exercise.precautions)}\n"
        
        # Takip programı / Follow-up schedule
        report += f"\n📅 TAKİP PROGRAMI:\n"
        for schedule in treatment_plan.follow_up_schedule:
            report += f"• {schedule}\n"
        
        # Önlemler / Precautions
        report += f"\n⚠️ ÖNEMLİ ÖNLEMLER:\n"
        for precaution in treatment_plan.precautions:
            report += f"• {precaution}\n"
        
        # Beklenen sonuçlar / Expected outcomes
        report += f"\n🎯 BEKLENEN SONUÇLAR:\n"
        for outcome in treatment_plan.expected_outcomes:
            report += f"• {outcome}\n"
        
        return report
