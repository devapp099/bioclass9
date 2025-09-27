#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def check_lesson_content(lesson_path):
    """فحص محتوى الدرس للتأكد من وجود أسئلة"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # البحث عن الأسئلة
        questions = re.findall(r'<article class="q"[^>]*data-qid="([^"]*)"', content)
        
        # البحث عن أزرار الإدارة
        has_start_btn = 'id="btnStart"' in content
        has_submit_btn = 'id="btnSubmit"' in content
        has_quiz_section = 'id="quiz"' in content
        
        # البحث عن محتوى تعليمي
        has_objectives = '🎯 أهداف الدرس' in content or 'أهداف الدرس' in content
        
        return {
            'questions_count': len(questions),
            'has_buttons': has_start_btn and has_submit_btn,
            'has_quiz_section': has_quiz_section,
            'has_objectives': has_objectives,
            'questions': questions,
            'ready': len(questions) > 0 and has_start_btn and has_submit_btn and has_quiz_section
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'ready': False
        }

def main():
    print("🔍 فحص محتوى الدروس للتأكد من اكتمالها...")
    print("=" * 80)
    
    lessons = [
        "unit-1-cells/lesson-1-1",
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
    
    complete_lessons = []
    incomplete_lessons = []
    
    for lesson in lessons:
        lesson_path = Path(lesson) / "index.html"
        
        if not lesson_path.exists():
            print(f"⚠️ {lesson}: الملف غير موجود")
            continue
        
        result = check_lesson_content(lesson_path)
        
        if 'error' in result:
            print(f"❌ {lesson}: خطأ - {result['error']}")
            incomplete_lessons.append(lesson)
            continue
        
        if result['ready']:
            print(f"✅ {lesson}: مكتمل ({result['questions_count']} أسئلة)")
            complete_lessons.append(lesson)
        else:
            missing = []
            if result['questions_count'] == 0:
                missing.append("لا توجد أسئلة")
            if not result['has_buttons']:
                missing.append("أزرار ناقصة")
            if not result['has_quiz_section']:
                missing.append("قسم الأسئلة مفقود")
            if not result['has_objectives']:
                missing.append("الأهداف مفقودة")
            
            print(f"⚠️ {lesson}: ناقص - {', '.join(missing)}")
            incomplete_lessons.append(lesson)
    
    print("\n" + "=" * 80)
    print("📊 الملخص:")
    print(f"✅ دروس مكتملة: {len(complete_lessons)}")
    print(f"⚠️ دروس تحتاج تكملة: {len(incomplete_lessons)}")
    
    if complete_lessons:
        print(f"\n🎉 الدروس المكتملة:")
        for lesson in complete_lessons:
            print(f"   ✅ {lesson}")
    
    if incomplete_lessons:
        print(f"\n🔧 الدروس التي تحتاج تكملة:")
        for lesson in incomplete_lessons:
            print(f"   ⚠️ {lesson}")
    
    print(f"\n💡 الخلاصة:")
    if len(complete_lessons) == len(lessons):
        print("🎊 جميع الدروس مكتملة ومعها الأنظمة الذكية!")
    else:
        print(f"🔧 {len(incomplete_lessons)} درس يحتاج لإضافة محتوى تعليمي")
        print("📝 الأنظمة الذكية موجودة، فقط أضف المحتوى التعليمي")

if __name__ == "__main__":
    main()