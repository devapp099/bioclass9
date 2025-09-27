#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
إصلاح شريط التقدم فقط - بدون التأثير على المحتوى
"""

import os
import re

def fix_progress_bar_only(file_path):
    """إصلاح شريط التقدم فقط"""
    
    if not os.path.exists(file_path):
        print(f"❌ الملف غير موجود: {file_path}")
        return False
    
    try:
        # قراءة المحتوى
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # التحقق من وجود updateProgress function
        if 'function updateProgress()' not in content:
            print(f"⚠️ {file_path}: لا توجد دالة updateProgress")
            return add_progress_function(file_path, content)
        
        # البحث عن دالة updateProgress الحالية واستبدالها
        progress_pattern = r'function updateProgress\(\)\{[^}]*\}'
        
        new_progress_function = '''function updateProgress(){
      const total = document.querySelectorAll('.q[data-qid]').length;
      const answered = Array.from(document.querySelectorAll('.q')).filter(q => 
        q.querySelector('.choice.correct, .choice.wrong')
      ).length;
      
      const barFill = document.getElementById('barFill');
      const countDone = document.getElementById('countDone');
      const countTotal = document.getElementById('countTotal');
      
      if (countTotal) countTotal.textContent = total;
      if (countDone) countDone.textContent = answered;
      if (barFill) barFill.style.width = Math.round((answered/total)*100) + '%';
    }'''
        
        # استبدال الدالة
        if re.search(progress_pattern, content, re.DOTALL):
            content = re.sub(progress_pattern, new_progress_function, content, flags=re.DOTALL)
            print(f"✅ {file_path}: تم استبدال دالة updateProgress")
        else:
            print(f"⚠️ {file_path}: لم يتم العثور على دالة updateProgress بالتنسيق المتوقع")
            return add_progress_function(file_path, content)
        
        # كتابة الملف المحدث
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في معالجة {file_path}: {e}")
        return False

def add_progress_function(file_path, content):
    """إضافة دالة updateProgress إذا لم تكن موجودة"""
    
    progress_function = '''
    function updateProgress(){
      const total = document.querySelectorAll('.q[data-qid]').length;
      const answered = Array.from(document.querySelectorAll('.q')).filter(q => 
        q.querySelector('.choice.correct, .choice.wrong')
      ).length;
      
      const barFill = document.getElementById('barFill');
      const countDone = document.getElementById('countDone');
      const countTotal = document.getElementById('countTotal');
      
      if (countTotal) countTotal.textContent = total;
      if (countDone) countDone.textContent = answered;
      if (barFill) barFill.style.width = Math.round((answered/total)*100) + '%';
    }'''
    
    # البحث عن مكان مناسب لإضافة الدالة
    insertion_points = [
        'function renderQuestions()',
        'function computeScore()',
        'document.addEventListener(\'click\'',
        'el.start.addEventListener(\'click\''
    ]
    
    for point in insertion_points:
        if point in content:
            content = content.replace(point, progress_function + '\n\n    ' + point)
            print(f"✅ {file_path}: تم إضافة دالة updateProgress")
            break
    else:
        print(f"⚠️ {file_path}: لم يتم العثور على مكان مناسب لإضافة الدالة")
        return False
    
    # كتابة الملف المحدث
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ خطأ في كتابة {file_path}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    
    print("🔧 إصلاح شريط التقدم في جميع الدروس...")
    print("=" * 50)
    
    # قائمة جميع الدروس
    lessons = [
        "unit-1-cells/lesson-1-1/index.html",
        "unit-1-cells/lesson-1-2/index.html", 
        "unit-1-cells/lesson-1-3/index.html",
        "unit-2-transport/lesson-2-1/index.html",
        "unit-2-transport/lesson-2-2/index.html",
        "unit-2-transport/lesson-2-3/index.html",
        "unit-3-biomolecules/lesson-3-1/index.html",
        "unit-3-biomolecules/lesson-3-2/index.html",
        "unit-3-biomolecules/lesson-3-3/index.html",
        "unit-4-nutrition/lesson-4-1/index.html",
        "unit-4-nutrition/lesson-4-2/index.html",
        "unit-5-respiration/lesson-5-1/index.html",
        "unit-6-homeostasis/lesson-6-1/index.html",
        "unit-6-homeostasis/lesson-6-2/index.html",
        "unit-6-homeostasis/lesson-6-3/index.html",
        "unit-6-homeostasis/lesson-6-4/index.html"
    ]
    
    fixed_count = 0
    
    for lesson in lessons:
        if fix_progress_bar_only(lesson):
            fixed_count += 1
    
    print("\n" + "=" * 50)
    print(f"✅ تم إصلاح شريط التقدم في {fixed_count} درس من أصل {len(lessons)}")
    print("🎯 الإصلاح يشمل:")
    print("   • عداد الأسئلة المُجابة")
    print("   • عداد إجمالي الأسئلة") 
    print("   • شريط التقدم المرئي")
    print("   • حماية من الأخطاء")

if __name__ == "__main__":
    main()