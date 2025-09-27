#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص شامل لجميع الأنظمة التفاعلية
"""

import os
import re

def check_all_systems(file_path):
    """فحص جميع الأنظمة في درس واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n🔍 فحص شامل للدرس: {file_path}")
        print("=" * 60)
        
        # 1. فحص النظام الصوتي (SoundSystem)
        print("🔊 النظام الصوتي:")
        if 'const SoundSystem = {' in content:
            print("  ✅ SoundSystem معرّف")
            if 'SoundSystem.init()' in content:
                print("  ✅ يتم استدعاء SoundSystem.init()")
            else:
                print("  ❌ لا يتم استدعاء SoundSystem.init()")
            
            if 'SoundSystem.play(' in content:
                print("  ✅ يتم استخدام SoundSystem.play()")
            else:
                print("  ⚠️  لا يتم استخدام SoundSystem.play()")
        else:
            print("  ❌ SoundSystem غير معرّف")
        
        # 2. فحص نظام الإشعارات (SweetAlert2)
        print("\n📢 نظام الإشعارات:")
        if 'Swal.fire(' in content:
            print("  ✅ SweetAlert2 يُستخدم")
            swal_count = len(re.findall(r'Swal\.fire\(', content))
            print(f"  📊 عدد الإشعارات: {swal_count}")
        else:
            print("  ❌ SweetAlert2 غير مستخدم")
        
        # 3. فحص نظام الرسائل الذكية
        print("\n💬 نظام الرسائل التفاعلية:")
        smart_messages = []
        if 'askStudent()' in content:
            smart_messages.append("طلب بيانات الطالب")
        if 'showResults()' in content:
            smart_messages.append("عرض النتائج")
        if 'Swal.fire({' in content:
            smart_messages.append("رسائل تفاعلية مخصصة")
        
        if smart_messages:
            print(f"  ✅ الرسائل الذكية: {', '.join(smart_messages)}")
        else:
            print("  ⚠️  لا توجد رسائل ذكية")
        
        # 4. فحص عرض المحتوى
        print("\n👁️ عرض المحتوى:")
        quiz_match = re.search(r'<section id="quiz"[^>]*>', content)
        if quiz_match:
            quiz_tag = quiz_match.group(0)
            if 'display:block' in quiz_tag:
                print("  ✅ قسم الأسئلة مرئي (display:block)")
            elif 'display:none' in quiz_tag:
                print("  ❌ قسم الأسئلة مخفي (display:none)")
            else:
                print("  ⚠️  لا يحتوي على display property")
        else:
            print("  ❌ قسم الأسئلة غير موجود")
        
        # 5. فحص الأسئلة التفاعلية
        print("\n❓ الأسئلة التفاعلية:")
        bank_match = re.search(r'const bank\s*=\s*\[(.*?)\];', content, re.DOTALL)
        if bank_match:
            questions = re.findall(r'\{q:"[^"]+",\s*c:\[[^\]]+\],\s*a:\d+\}', bank_match.group(1))
            print(f"  ✅ عدد الأسئلة: {len(questions)}")
            
            # فحص التفاعل
            if "document.addEventListener('click', e =>" in content:
                print("  ✅ نظام التفاعل مع الأسئلة موجود")
            else:
                print("  ❌ نظام التفاعل مع الأسئلة غير موجود")
        else:
            print("  ❌ لا توجد أسئلة")
        
        # 6. فحص شريط التقدم
        print("\n📊 شريط التقدم:")
        if 'function updateProgress()' in content:
            print("  ✅ دالة updateProgress موجودة")
            if 'updateProgress()' in content:
                print("  ✅ يتم استدعاء updateProgress")
            else:
                print("  ❌ لا يتم استدعاء updateProgress")
        else:
            print("  ❌ دالة updateProgress غير موجودة")
        
        # 7. فحص JavaScript العام
        print("\n⚙️ JavaScript العام:")
        js_issues = []
        
        # فحص الأخطاء الشائعة
        if 'this.sounds    [' in content:
            js_issues.append("خطأ في تعريف SoundSystem")
        if 'const bank =' in content and not re.search(r'const bank\s*=\s*\[.*?\];', content, re.DOTALL):
            js_issues.append("خطأ في تعريف bank")
        
        if js_issues:
            print(f"  ❌ مشاكل JavaScript: {', '.join(js_issues)}")
        else:
            print("  ✅ لا توجد مشاكل JavaScript واضحة")
        
        # 8. فحص CSS المهم
        print("\n🎨 التصميم:")
        if '.q{' in content:
            print("  ✅ CSS للأسئلة موجود")
        else:
            print("  ❌ CSS للأسئلة غير موجود")
        
        if '.choice' in content:
            print("  ✅ CSS للخيارات موجود")
        else:
            print("  ❌ CSS للخيارات غير موجود")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في فحص {file_path}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔍 فحص شامل لجميع الأنظمة التفاعلية...")
    print("=" * 70)
    
    # فحص عينة من الدروس
    sample_lessons = [
        "unit-1-cells/lesson-1-1/index.html",
        "unit-1-cells/lesson-1-2/index.html",
        "unit-2-transport/lesson-2-1/index.html",
        "unit-3-biomolecules/lesson-3-1/index.html",
        "unit-6-homeostasis/lesson-6-4/index.html"
    ]
    
    checked_count = 0
    
    for lesson in sample_lessons:
        if os.path.exists(lesson):
            if check_all_systems(lesson):
                checked_count += 1
        else:
            print(f"❌ الملف غير موجود: {lesson}")
    
    print("\n" + "=" * 70)
    print(f"🎉 انتهاء الفحص الشامل!")
    print(f"✅ تم فحص {checked_count} درس من أصل {len(sample_lessons)}")
    print("\n🎯 الأنظمة المفحوصة:")
    print("   🔊 النظام الصوتي (SoundSystem)")
    print("   📢 نظام الإشعارات (SweetAlert2)")
    print("   💬 نظام الرسائل التفاعلية")
    print("   👁️  عرض المحتوى")
    print("   ❓ الأسئلة التفاعلية")
    print("   📊 شريط التقدم")
    print("   ⚙️  JavaScript العام")
    print("   🎨 التصميم (CSS)")

if __name__ == "__main__":
    main()