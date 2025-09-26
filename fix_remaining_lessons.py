#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def fix_remaining_lessons():
    """إصلاح باقي الدروس"""
    base_path = Path(".")
    
    # باقي الدروس
    remaining_lessons = [
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
    
    # نسخ درس يعمل كمرجع
    reference_lesson = base_path / "unit-1-cells/lesson-1-2/index.html"
    
    if not reference_lesson.exists():
        print("❌ الدرس المرجعي غير موجود")
        return
    
    with open(reference_lesson, 'r', encoding='utf-8') as f:
        reference_content = f.read()
    
    fixed_count = 0
    
    for lesson_path in remaining_lessons:
        full_path = base_path / lesson_path / "index.html"
        if not full_path.exists():
            continue
            
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # استخراج العنوان
            title_match = re.search(r'<title>(.*?)</title>', content)
            title = title_match.group(1) if title_match else "درس"
            
            # استخراج قسم الأسئلة
            quiz_section_match = re.search(r'<section id="quiz"[^>]*>(.*?)</section>', content, re.DOTALL)
            if not quiz_section_match:
                print(f"❌ {lesson_path}: لم يتم العثور على قسم الأسئلة")
                continue
            
            quiz_section = quiz_section_match.group(1)
            
            # استبدال العنوان والأسئلة في الدرس المرجعي
            new_content = reference_content
            new_content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', new_content)
            new_content = re.sub(r'(<section id="quiz"[^>]*>).*?(</section>)', 
                               rf'\1{quiz_section}\2', new_content, flags=re.DOTALL)
            
            # كتابة الملف الجديد
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ تم إصلاح: {lesson_path}")
            fixed_count += 1
            
        except Exception as e:
            print(f"❌ خطأ في {lesson_path}: {str(e)}")
    
    print(f"\n🎉 تم إصلاح {fixed_count} درس إضافي!")

if __name__ == "__main__":
    fix_remaining_lessons()