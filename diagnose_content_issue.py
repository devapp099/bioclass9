#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشخيص المشكلة الحقيقية للمحتوى
"""

import os
import re

def check_lesson_content(file_path):
    """فحص محتوى درس واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n🔍 فحص الدرس: {file_path}")
        print("=" * 50)
        
        # 1. التحقق من display property
        quiz_section_match = re.search(r'<section id="quiz"[^>]*>', content)
        if quiz_section_match:
            quiz_tag = quiz_section_match.group(0)
            print(f"✅ قسم quiz موجود: {quiz_tag}")
            if 'display:block' in quiz_tag:
                print("✅ Display property: block")
            elif 'display:none' in quiz_tag:
                print("❌ Display property: none")
            else:
                print("⚠️  لا يحتوي على display property")
        else:
            print("❌ قسم quiz غير موجود!")
            return
        
        # 2. التحقق من وجود الأسئلة
        bank_match = re.search(r'const bank\s*=\s*\[(.*?)\];', content, re.DOTALL)
        if bank_match:
            bank_content = bank_match.group(1)
            questions = re.findall(r'\{q:"[^"]+",\s*c:\[[^\]]+\],\s*a:\d+\}', bank_content)
            print(f"✅ عدد الأسئلة: {len(questions)}")
            
            # عرض أول سؤال كعينة
            first_q = re.search(r'q:"([^"]+)"', bank_content)
            if first_q:
                print(f"📝 عينة سؤال: {first_q.group(1)[:50]}...")
        else:
            print("❌ لا توجد أسئلة في bank!")
        
        # 3. التحقق من استدعاء renderQuestions
        if 'renderQuestions();' in content:
            print("✅ يتم استدعاء renderQuestions")
        else:
            print("❌ لا يتم استدعاء renderQuestions!")
        
        # 4. التحقق من وجود دالة renderQuestions
        if 'function renderQuestions()' in content:
            print("✅ دالة renderQuestions موجودة")
        else:
            print("❌ دالة renderQuestions غير موجودة!")
        
        # 5. التحقق من CSS للأسئلة
        if '.q{' in content:
            print("✅ CSS للأسئلة موجود")
        else:
            print("❌ CSS للأسئلة غير موجود!")
        
        # 6. التحقق من HTML لعرض الأسئلة
        if 'id="quizList"' in content:
            print("✅ div quizList موجود")
        else:
            print("❌ div quizList غير موجود!")
        
        # 7. فحص أي JavaScript errors محتملة
        js_errors = []
        if 'SoundSystem.play(' in content and 'SoundSystem = {' not in content:
            js_errors.append("SoundSystem غير معرف")
        if 'el.list' in content and 'el = {' not in content:
            js_errors.append("متغير el غير معرف")
        
        if js_errors:
            print(f"⚠️  أخطاء JavaScript محتملة: {', '.join(js_errors)}")
        else:
            print("✅ لا توجد أخطاء JavaScript واضحة")
            
    except Exception as e:
        print(f"❌ خطأ في فحص {file_path}: {e}")

def main():
    """الدالة الرئيسية"""
    print("🔧 تشخيص مشكلة المحتوى المخفي...")
    print("=" * 60)
    
    # فحص بعض الدروس كعينة
    sample_lessons = [
        "unit-1-cells/lesson-1-1/index.html",
        "unit-1-cells/lesson-1-2/index.html",
        "unit-2-transport/lesson-2-1/index.html",
        "unit-6-homeostasis/lesson-6-4/index.html"
    ]
    
    for lesson in sample_lessons:
        if os.path.exists(lesson):
            check_lesson_content(lesson)
        else:
            print(f"❌ الملف غير موجود: {lesson}")
    
    print("\n" + "=" * 60)
    print("🎯 خلاصة التشخيص:")
    print("إذا كانت جميع العناصر موجودة ولكن المحتوى لا يظهر،")
    print("فالمشكلة قد تكون في:")
    print("• تضارب في CSS")
    print("• خطأ في JavaScript يمنع تنفيذ renderQuestions")
    print("• مشكلة في ترتيب تحميل الكود")
    print("• إعدادات المتصفح أو AdBlocker")

if __name__ == "__main__":
    main()