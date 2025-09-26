#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح مشكلة عرض أكواد JavaScript كنص عادي
حل المشكلة: إزالة الأكواد المكررة التي تظهر خارج علامات HTML
"""

import os
import re
import glob

def fix_javascript_display_issue(file_path):
    """إصلاح ملف HTML واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # البحث عن النهاية الصحيحة للملف (</html>)
        html_end_match = re.search(r'</html>\s*$', content, re.MULTILINE | re.DOTALL)
        
        if html_end_match:
            # قطع المحتوى عند نهاية علامة </html>
            clean_content = content[:html_end_match.end()]
            
            # التحقق من وجود محتوى إضافي بعد </html>
            extra_content = content[html_end_match.end():].strip()
            
            if extra_content:
                print(f"🔧 إصلاح {file_path}")
                print(f"   - إزالة {len(extra_content)} حرف إضافي")
                
                # إنشاء نسخة احتياطية
                backup_path = file_path + '.backup_js_fix'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # كتابة المحتوى المنظف
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(clean_content)
                
                return True
            else:
                print(f"✅ {file_path} - لا يحتاج إصلاح")
                return False
        else:
            print(f"⚠️  {file_path} - لم يتم العثور على علامة </html>")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في معالجة {file_path}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔧 بدء إصلاح مشكلة عرض JavaScript كنص...")
    print("=" * 60)
    
    # البحث عن جميع ملفات الدروس
    lesson_pattern = "unit-*/lesson-*/index.html"
    lesson_files = glob.glob(lesson_pattern)
    
    if not lesson_files:
        print("❌ لم يتم العثور على ملفات الدروس!")
        return
    
    print(f"📁 تم العثور على {len(lesson_files)} ملف درس")
    print()
    
    fixed_count = 0
    
    # معالجة كل ملف
    for file_path in sorted(lesson_files):
        if fix_javascript_display_issue(file_path):
            fixed_count += 1
    
    print()
    print("=" * 60)
    print(f"✅ تم الانتهاء! تم إصلاح {fixed_count} ملف من أصل {len(lesson_files)}")
    
    if fixed_count > 0:
        print()
        print("🎯 التوصيات:")
        print("   1. تحقق من الصفحات في المتصفح")
        print("   2. ارفع التغييرات على GitHub إذا كانت تعمل بشكل صحيح")
        print("   3. النسخ الاحتياطية محفوظة بامتداد .backup_js_fix")

if __name__ == "__main__":
    main()