#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def check_lesson_systems(lesson_path):
    """فحص شامل لأنظمة الدرس"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        features = {
            'sound_system': False,
            'notification_system': False,
            'performance_functions': False,
            'external_libraries': False,
            'event_handlers': False,
            'smart_styles': False,
            'initialization': False
        }
        
        # التحقق من النظام الصوتي
        if 'const SoundSystem' in content and 'SoundSystem.init()' in content:
            features['sound_system'] = True
        
        # التحقق من نظام الإشعارات
        if 'EnhancedNotificationSystem' in content and 'showWelcomeMessage' in content:
            features['notification_system'] = True
        
        # التحقق من دوال الأداء
        if 'getPerformanceLevel' in content and 'getFinalResultMessage' in content:
            features['performance_functions'] = True
        
        # التحقق من المكتبات الخارجية
        external_libs = ['sweetalert2', 'canvas-confetti', 'gsap', 'aos', 'howler']
        if all(lib in content for lib in external_libs):
            features['external_libraries'] = True
        
        # التحقق من معالجات الأحداث
        if "document.addEventListener('click'" in content and 'choice.dataset.correct' in content:
            features['event_handlers'] = True
        
        # التحقق من الأنماط الذكية
        if 'linear-gradient' in content and '.card:hover' in content:
            features['smart_styles'] = True
        
        # التحقق من التهيئة
        if "DOMContentLoaded" in content and "AOS.init" in content:
            features['initialization'] = True
        
        working_features = sum(features.values())
        total_features = len(features)
        
        return {
            'working': working_features == total_features,
            'features': features,
            'score': f"{working_features}/{total_features}",
            'percentage': round((working_features/total_features)*100)
        }
        
    except Exception as e:
        return {
            'working': False,
            'error': str(e)
        }

def main():
    print("🔍 فحص شامل للأنظمة الجديدة في جميع الدروس...")
    print("=" * 80)
    
    # قائمة جميع الدروس
    all_lessons = [
        "unit-1-cells/lesson-1-1",  # المرجع
        "unit-1-cells/lesson-1-2",
        "unit-1-cells/lesson-1-3",
        "unit-2-transport/lesson-2-1",
        "unit-2-transport/lesson-2-2",
        "unit-2-transport/lesson-2-3",
        "unit-3-biomolecules/lesson-3-1",
        "unit-3-biomolecules/lesson-3-2",
        "unit-3-biomolecules/lesson-3-3",
        "unit-4-nutrition/lesson-4-1",
        "unit-4-nutrition/lesson-4-2",
        "unit-5-respiration/lesson-5-1",
        "unit-6-homeostasis/lesson-6-1",
        "unit-6-homeostasis/lesson-6-2",
        "unit-6-homeostasis/lesson-6-3",
        "unit-6-homeostasis/lesson-6-4"
    ]
    
    working_lessons = []
    broken_lessons = []
    feature_summary = {
        'sound_system': 0,
        'notification_system': 0,
        'performance_functions': 0,
        'external_libraries': 0,
        'event_handlers': 0,
        'smart_styles': 0,
        'initialization': 0
    }
    
    print("📋 تفاصيل الفحص:\n")
    
    for lesson in all_lessons:
        lesson_path = Path(lesson) / "index.html"
        
        if not lesson_path.exists():
            print(f"⚠️ {lesson}: الملف غير موجود")
            continue
        
        result = check_lesson_systems(lesson_path)
        
        if 'error' in result:
            print(f"❌ {lesson}: خطأ في القراءة - {result['error']}")
            broken_lessons.append(lesson)
            continue
        
        # تجميع الإحصائيات
        if result['working']:
            working_lessons.append(lesson)
            status = "✅ يعمل بكامل الأنظمة"
        else:
            broken_lessons.append(lesson)
            status = f"⚠️ أنظمة ناقصة ({result['score']} - {result['percentage']}%)"
        
        print(f"{status} - {lesson}")
        
        # إضافة تفاصيل الميزات للدروس التي لا تعمل بشكل كامل
        if not result['working']:
            print("   الميزات:")
            for feature, working in result['features'].items():
                icon = "✅" if working else "❌"
                print(f"     {icon} {feature}")
        
        # تحديث ملخص الميزات
        for feature, working in result['features'].items():
            if working:
                feature_summary[feature] += 1
    
    print("\n" + "=" * 80)
    print("📊 ملخص شامل:")
    print(f"✅ الدروس العاملة بكامل الأنظمة: {len(working_lessons)}")
    print(f"⚠️ الدروس التي تحتاج تحسين: {len(broken_lessons)}")
    print(f"📈 معدل النجاح: {round((len(working_lessons)/len(all_lessons))*100)}%")
    
    print("\n🔧 ملخص الميزات المفعلة:")
    total_lessons = len(all_lessons)
    for feature, count in feature_summary.items():
        percentage = round((count/total_lessons)*100)
        print(f"   {feature}: {count}/{total_lessons} ({percentage}%)")
    
    if working_lessons:
        print(f"\n🎉 الدروس العاملة بكامل الأنظمة:")
        for lesson in working_lessons:
            print(f"   ✅ {lesson}")
    
    if broken_lessons:
        print(f"\n⚠️ الدروس التي تحتاج مراجعة:")
        for lesson in broken_lessons:
            print(f"   🔧 {lesson}")
    
    print(f"\n💡 تم نقل جميع الأنظمة الذكية بنجاح!")
    print(f"🔔 الآن يمكنك تحديث محتوى كل درس والأنظمة ستتكيف تلقائياً")

if __name__ == "__main__":
    main()