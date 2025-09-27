#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح إظهار المحتوى في جميع الدروس
Fix content visibility in all lessons
"""

import os
import re

def fix_lesson_content(file_path):
    """إصلاح إظهار المحتوى في درس واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # البحث عن قسم quiz المخفي وتغييره ليظهر مباشرة
        quiz_pattern = r'<section id="quiz" class="card" style="margin-top:16px; display:none"'
        if quiz_pattern in content:
            content = content.replace(
                '<section id="quiz" class="card" style="margin-top:16px; display:none"',
                '<section id="quiz" class="card" style="margin-top:16px; display:block"'
            )
            
            # إضافة كود JavaScript لضمان إظهار المحتوى
            js_fix = '''
    // ضمان إظهار المحتوى
    document.addEventListener('DOMContentLoaded', function() {
        const quizSection = document.getElementById('quiz');
        if (quizSection) {
            quizSection.style.display = 'block';
        }
    });
    
    // إصلاح إضافي في حالة عدم عمل الكود السابق
    window.addEventListener('load', function() {
        setTimeout(() => {
            const quiz = document.getElementById('quiz');
            if (quiz) {
                quiz.style.display = 'block';
                quiz.style.visibility = 'visible';
                quiz.style.opacity = '1';
            }
        }, 100);
    });
'''
            
            # إضافة الكود قبل إغلاق body
            if '</body>' in content:
                content = content.replace('</body>', f'<script>{js_fix}</script>\n</body>')
        
        # حفظ الملف
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في معالجة {file_path}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔧 بدء إصلاح إظهار المحتوى في جميع الدروس...")
    
    # مجلدات الوحدات
    units = [
        'unit-1-cells',
        'unit-2-transport', 
        'unit-3-biomolecules',
        'unit-4-nutrition',
        'unit-5-respiration',
        'unit-6-homeostasis'
    ]
    
    fixed_count = 0
    total_count = 0
    
    for unit in units:
        unit_path = unit
        if os.path.exists(unit_path):
            # البحث عن جميع الدروس في الوحدة
            for item in os.listdir(unit_path):
                lesson_path = os.path.join(unit_path, item)
                if os.path.isdir(lesson_path) and item.startswith('lesson-'):
                    index_file = os.path.join(lesson_path, 'index.html')
                    if os.path.exists(index_file):
                        total_count += 1
                        print(f"🔄 معالجة: {item}")
                        
                        if fix_lesson_content(index_file):
                            fixed_count += 1
                            print(f"✅ تم إصلاح: {item}")
                        else:
                            print(f"❌ فشل إصلاح: {item}")
    
    print(f"\n🎉 انتهاء العملية!")
    print(f"✅ تم إصلاح {fixed_count} درس من أصل {total_count}")
    
    if fixed_count == total_count:
        print("🌟 جميع الدروس تم إصلاحها بنجاح!")
    else:
        print(f"⚠️  {total_count - fixed_count} دروس تحتاج مراجعة")

if __name__ == "__main__":
    main()