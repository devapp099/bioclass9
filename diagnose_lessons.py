#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def diagnose_lesson_loading_issues(lesson_path):
    """تشخيص مشاكل تحميل الدرس"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        warnings = []
        
        # فحص وجود العناصر الأساسية
        if not re.search(r'<body>', content):
            issues.append("❌ عنصر body مفقود")
        
        if not re.search(r'<style>', content):
            issues.append("❌ قسم CSS مفقود")
        
        if not re.search(r'<div class="wrap">', content):
            issues.append("❌ div الرئيسي مفقود")
        
        # فحص JavaScript
        if not re.search(r'const el =', content):
            issues.append("❌ متغيرات JavaScript الأساسية مفقودة")
        
        # فحص مشاكل الأقواس في JavaScript
        js_section_match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
        if js_section_match:
            js_content = js_section_match.group(1)
            
            # عد الأقواس
            open_braces = js_content.count('{')
            close_braces = js_content.count('}')
            
            if open_braces != close_braces:
                issues.append(f"❌ عدم توازن الأقواس - فتح: {open_braces}, إغلاق: {close_braces}")
            
            # فحص أخطاء نحوية شائعة
            if 'el.submit.addEventListener' in js_content and 'el.submit.addEventListener' not in content:
                warnings.append("⚠️ قد يكون هناك مشكلة في تعريف زر النتائج")
            
            # فحص تهيئة AOS
            if 'AOS.init()' not in js_content:
                warnings.append("⚠️ AOS غير مهيأ - قد يؤثر على الأنيميشن")
        
        # فحص وجود أزرار مهمة
        if not re.search(r'id="btnStart"', content):
            issues.append("❌ زر البداية مفقود")
        
        if not re.search(r'id="btnSubmit"', content):
            warnings.append("⚠️ زر النتائج قد يكون مفقود")
        
        # فحص وجود الأسئلة
        question_count = len(re.findall(r'data-qid=', content))
        if question_count == 0:
            issues.append("❌ لا توجد أسئلة")
        elif question_count < 5:
            warnings.append(f"⚠️ عدد قليل من الأسئلة: {question_count}")
        
        return {
            'issues': issues,
            'warnings': warnings,
            'questions_count': question_count,
            'has_css': '<style>' in content,
            'has_js': '<script>' in content
        }
        
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
    
    print("🔍 تشخيص مشاكل تحميل الدروس...")
    print("=" * 80)
    
    problematic_lessons = []
    working_lessons = []
    
    for lesson in sorted(lessons, key=lambda x: x['full_name']):
        diagnosis = diagnose_lesson_loading_issues(lesson['path'])
        
        if 'error' in diagnosis:
            print(f"\n❌ {lesson['full_name']}: خطأ في القراءة - {diagnosis['error']}")
            continue
        
        has_critical_issues = len(diagnosis['issues']) > 0
        
        print(f"\n📚 {lesson['full_name']}")
        print("-" * 40)
        
        if has_critical_issues:
            print("🚨 مشاكل حرجة:")
            for issue in diagnosis['issues']:
                print(f"  {issue}")
            problematic_lessons.append(lesson['full_name'])
        else:
            print("✅ لا توجد مشاكل حرجة")
            working_lessons.append(lesson['full_name'])
        
        if diagnosis['warnings']:
            print("⚠️ تحذيرات:")
            for warning in diagnosis['warnings']:
                print(f"  {warning}")
        
        print(f"📊 عدد الأسئلة: {diagnosis['questions_count']}")
        print(f"🎨 CSS: {'✅' if diagnosis['has_css'] else '❌'}")
        print(f"⚙️ JavaScript: {'✅' if diagnosis['has_js'] else '❌'}")
    
    print("\n" + "=" * 80)
    print(f"📈 ملخص التشخيص:")
    print(f"✅ دروس تعمل بشكل صحيح: {len(working_lessons)}")
    print(f"🚨 دروس تحتاج إصلاح: {len(problematic_lessons)}")
    
    if problematic_lessons:
        print(f"\n🔧 الدروس التي تحتاج إصلاح:")
        for lesson in problematic_lessons:
            print(f"  - {lesson}")
    
    if len(working_lessons) == len(lessons):
        print(f"\n🎉 جميع الدروس تبدو سليمة من ناحية الهيكل!")
        print(f"💡 المشكلة قد تكون في تحميل المكتبات الخارجية أو شبكة الإنترنت")

if __name__ == "__main__":
    main()