#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import time
from pathlib import Path

def test_lesson_loading(lesson_url):
    """اختبار تحميل الدرس"""
    try:
        response = requests.get(lesson_url, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            # فحص المحتوى الأساسي
            has_content = all([
                '<body>' in content,
                'class="wrap"' in content,
                'أهداف الدرس' in content or 'الأسئلة' in content,
                '</html>' in content
            ])
            
            # فحص JavaScript
            has_js = '<script>' in content
            
            # فحص CSS
            has_css = '<style>' in content or 'stylesheet' in content
            
            # فحص AOS
            has_aos = 'AOS.init' in content
            
            return {
                'status': 'success',
                'status_code': response.status_code,
                'has_content': has_content,
                'has_js': has_js,
                'has_css': has_css,
                'has_aos': has_aos,
                'content_length': len(content)
            }
        else:
            return {
                'status': 'error',
                'status_code': response.status_code,
                'error': f'HTTP {response.status_code}'
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'status': 'error',
            'error': str(e)
        }

def main():
    base_url = "https://devapp099.github.io/bioclass9"
    
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
    
    print("🌐 اختبار تحميل جميع الدروس على الإنترنت...")
    print("=" * 80)
    
    working_lessons = []
    broken_lessons = []
    
    for lesson in lessons:
        lesson_url = f"{base_url}/{lesson}/"
        print(f"\n📚 اختبار: {lesson}")
        print(f"🔗 الرابط: {lesson_url}")
        
        result = test_lesson_loading(lesson_url)
        
        if result['status'] == 'success':
            print(f"✅ الحالة: {result['status_code']}")
            print(f"📄 طول المحتوى: {result['content_length']} حرف")
            print(f"🎨 CSS: {'✅' if result['has_css'] else '❌'}")
            print(f"⚙️ JavaScript: {'✅' if result['has_js'] else '❌'}")
            print(f"✨ AOS: {'✅' if result['has_aos'] else '❌'}")
            print(f"📝 المحتوى كامل: {'✅' if result['has_content'] else '❌'}")
            
            if result['has_content'] and result['has_css'] and result['has_js']:
                working_lessons.append(lesson)
                print("🎉 الدرس يعمل بشكل صحيح")
            else:
                broken_lessons.append(lesson)
                print("⚠️ الدرس يحتاج إصلاح")
        else:
            print(f"❌ خطأ: {result['error']}")
            broken_lessons.append(lesson)
        
        # توقف قصير لتجنب الضغط على الخادم
        time.sleep(1)
    
    print("\n" + "=" * 80)
    print(f"📈 ملخص النتائج:")
    print(f"✅ دروس تعمل: {len(working_lessons)}")
    print(f"❌ دروس معطلة: {len(broken_lessons)}")
    
    if working_lessons:
        print(f"\n✅ الدروس العاملة:")
        for lesson in working_lessons:
            print(f"  - {lesson}")
    
    if broken_lessons:
        print(f"\n❌ الدروس المعطلة:")
        for lesson in broken_lessons:
            print(f"  - {lesson}")
        
        print(f"\n💡 قد تحتاج هذه الدروس:")
        print(f"  - فحص أخطاء JavaScript")
        print(f"  - فحص ملفات CSS")
        print(f"  - إعادة رفع أو تحديث")

if __name__ == "__main__":
    main()