#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشخيص سريع لمشكلة اختفاء المحتوى
"""

import os
import re

def quick_diagnosis(file_path):
    """تشخيص سريع للملف"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n🔍 تشخيص سريع: {file_path}")
        print("-" * 50)
        
        # 1. فحص الأسئلة
        bank_match = re.search(r'const bank\s*=\s*\[(.*?)\];', content, re.DOTALL)
        if bank_match:
            questions = re.findall(r'\{q:"[^"]+",\s*c:\[[^\]]+\],\s*a:\d+\}', bank_match.group(1))
            print(f"✅ الأسئلة: {len(questions)} سؤال موجود")
        else:
            print("❌ لا توجد أسئلة!")
        
        # 2. فحص استدعاء renderQuestions
        if 'renderQuestions();' in content:
            print("✅ يتم استدعاء renderQuestions")
        else:
            print("❌ لا يتم استدعاء renderQuestions!")
        
        # 3. فحص دالة renderQuestions
        if 'function renderQuestions()' in content:
            print("✅ دالة renderQuestions موجودة")
        else:
            print("❌ دالة renderQuestions غير موجودة!")
        
        # 4. فحص تعريف el
        if 'const el = {' in content:
            print("✅ متغير el معرف")
        else:
            print("❌ متغير el غير معرف!")
        
        # 5. فحص عرض quiz
        quiz_section = re.search(r'<section id="quiz"[^>]*>', content)
        if quiz_section:
            if 'display:block' in quiz_section.group(0):
                print("✅ قسم quiz مرئي (display:block)")
            elif 'display:none' in quiz_section.group(0):
                print("❌ قسم quiz مخفي (display:none)")
            else:
                print("⚠️  قسم quiz بدون display property")
        else:
            print("❌ قسم quiz غير موجود!")
        
        # 6. فحص askStudent
        if 'askStudent();' in content:
            print("✅ يتم استدعاء askStudent")
        else:
            print("❌ لا يتم استدعاء askStudent!")
        
        # 7. فحص تسلسل التنفيذ
        lines = content.split('\n')
        render_line = -1
        ask_line = -1
        
        for i, line in enumerate(lines):
            if 'renderQuestions();' in line:
                render_line = i
            if 'askStudent();' in line:
                ask_line = i
        
        if render_line > 0 and ask_line > 0:
            if render_line < ask_line:
                print("✅ التسلسل صحيح: renderQuestions قبل askStudent")
            else:
                print("❌ التسلسل خاطئ: askStudent قبل renderQuestions!")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في فحص {file_path}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚨 تشخيص سريع لمشكلة اختفاء المحتوى...")
    print("=" * 60)
    
    # فحص عينة من الدروس
    sample_lessons = [
        "unit-1-cells/lesson-1-1/index.html",
        "unit-1-cells/lesson-1-2/index.html",
        "unit-2-transport/lesson-2-1/index.html"
    ]
    
    for lesson in sample_lessons:
        if os.path.exists(lesson):
            quick_diagnosis(lesson)
        else:
            print(f"❌ الملف غير موجود: {lesson}")
    
    print("\n" + "=" * 60)
    print("💡 تشخيص المشكلة المحتملة:")
    print("إذا كانت الأسئلة موجودة ولكن لا تظهر، المشكلة قد تكون:")
    print("1. ⏰ توقيت استدعاء askStudent يمنع عرض الأسئلة")
    print("2. 🔄 تضارب في تسلسل تنفيذ JavaScript")
    print("3. 🎯 قسم quiz مخفي بـ display:none")
    print("4. 🧩 خطأ في دالة renderQuestions")

if __name__ == "__main__":
    main()