#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def check_lesson_features(lesson_path):
    """فحص ميزات الدرس"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        features = {
            'sound_system': bool(re.search(r'SoundSystem\s*=\s*{', content)),
            'smart_notifications': bool(re.search(r'Swal\.fire', content)),
            'enhanced_features': bool(re.search(r'getPerformanceLevel|getFinalResultMessage', content)),
            'interactive_messages': bool(re.search(r'showEncouragementMessage', content)),
            'final_results_screen': bool(re.search(r'النتائج النهائية', content)),
            'celebration_effects': bool(re.search(r'confetti|celebrate', content)),
            'progress_tracking': bool(re.search(r'updateProgress', content)),
            'milestone_notifications': bool(re.search(r'checkMilestones', content))
        }
        
        return features
    except Exception as e:
        return {'error': str(e)}

def main():
    base_path = Path(".")
    lessons = []
    
    # البحث عن جميع دروس الوحدات
    for unit_dir in base_path.glob("unit-*"):
        if unit_dir.is_dir():
            for lesson_dir in unit_dir.glob("lesson-*"):
                if lesson_dir.is_dir():
                    index_file = lesson_dir / "index.html"
                    if index_file.exists():
                        lessons.append({
                            'path': str(index_file),
                            'unit': unit_dir.name,
                            'lesson': lesson_dir.name,
                            'full_name': f"{unit_dir.name}/{lesson_dir.name}"
                        })
    
    print("🔍 فحص حالة جميع الدروس...")
    print("=" * 80)
    
    total_lessons = len(lessons)
    updated_lessons = 0
    
    for lesson in sorted(lessons, key=lambda x: x['full_name']):
        print(f"\n📚 الدرس: {lesson['full_name']}")
        print("-" * 40)
        
        features = check_lesson_features(lesson['path'])
        
        if 'error' in features:
            print(f"❌ خطأ في القراءة: {features['error']}")
            continue
        
        # تحديد حالة الدرس
        essential_features = ['sound_system', 'smart_notifications', 'final_results_screen']
        has_essentials = all(features.get(f, False) for f in essential_features)
        
        enhanced_features = ['enhanced_features', 'interactive_messages', 'celebration_effects']
        has_enhanced = all(features.get(f, False) for f in enhanced_features)
        
        if has_essentials and has_enhanced:
            status = "✅ محدث بالكامل"
            updated_lessons += 1
        elif has_essentials:
            status = "⚠️ محدث جزئياً"
        else:
            status = "❌ يحتاج تحديث"
        
        print(f"📊 الحالة: {status}")
        
        # تفاصيل الميزات
        feature_status = []
        for feature, exists in features.items():
            emoji = "✅" if exists else "❌"
            feature_names = {
                'sound_system': 'نظام الصوت',
                'smart_notifications': 'الإشعارات الذكية', 
                'enhanced_features': 'الميزات المحسنة',
                'interactive_messages': 'الرسائل التفاعلية',
                'final_results_screen': 'شاشة النتائج النهائية',
                'celebration_effects': 'تأثيرات الاحتفال',
                'progress_tracking': 'تتبع التقدم',
                'milestone_notifications': 'إشعارات المعالم'
            }
            
            if feature in feature_names:
                feature_status.append(f"{emoji} {feature_names[feature]}")
        
        for status_item in feature_status:
            print(f"  {status_item}")

    print("\n" + "=" * 80)
    print(f"📈 ملخص النتائج:")
    print(f"📚 إجمالي الدروس: {total_lessons}")
    print(f"✅ الدروس المحدثة بالكامل: {updated_lessons}")
    print(f"⚠️ الدروس تحتاج تحديث: {total_lessons - updated_lessons}")
    print(f"📊 نسبة التحديث: {(updated_lessons/total_lessons)*100:.1f}%")
    
    if updated_lessons < total_lessons:
        print(f"\n🔧 يُنصح بتشغيل أداة التحديث الشامل للدروس المتبقية")
    else:
        print(f"\n🎉 تهانينا! جميع الدروس محدثة بالأنظمة الذكية!")

if __name__ == "__main__":
    main()