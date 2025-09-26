#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def fix_duplicate_aos_init(lesson_path):
    """إزالة تكرارات AOS.init والاحتفاظ بواحد فقط"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # عد تكرارات AOS.init
        aos_matches = list(re.finditer(r'AOS\.init\s*\([^)]*\);?', content))
        
        if len(aos_matches) <= 1:
            return False, f"يحتوي على {len(aos_matches)} تكرار فقط (طبيعي)"
        
        print(f"  وُجد {len(aos_matches)} تكرار من AOS.init")
        
        # الاحتفاظ بآخر تكرار فقط (عادة الأحدث)
        new_content = content
        for i in range(len(aos_matches) - 1):  # إزالة جميع التكرارات عدا الأخير
            match = aos_matches[i]
            # البحث عن السطر الكامل الذي يحتوي على AOS.init
            lines = content.split('\n')
            for line_idx, line in enumerate(lines):
                if 'AOS.init' in line and match.start() in range(len('\n'.join(lines[:line_idx+1]))-len(line), len('\n'.join(lines[:line_idx+1]))+1):
                    # إزالة السطر الكامل
                    lines[line_idx] = ''
                    break
        
        # إعادة بناء المحتوى
        new_content = '\n'.join(lines)
        
        # تنظيف الأسطر الفارغة المتتالية
        new_content = re.sub(r'\n\s*\n\s*\n', '\n\n', new_content)
        
        # إضافة AOS.init واحد فقط في المكان المناسب إذا لم يعد موجود
        if 'AOS.init' not in new_content:
            # البحث عن مكان مناسب للإضافة
            insert_points = [
                r'(updateMeta\(\);)',
                r'(console\.log\([\'"].*تم تهيئة.*[\'"].*\);)',
                r'(\s*</script>)'
            ]
            
            inserted = False
            for pattern in insert_points:
                if re.search(pattern, new_content):
                    aos_code = '''
    
    // تهيئة AOS للأنيميشن
    AOS.init({
      duration: 700,
      easing: 'ease',
      once: true,
      offset: 50
    });'''
                    new_content = re.sub(pattern, aos_code + '\n    ' + r'\1', new_content)
                    inserted = True
                    break
        
        # كتابة الملف المحدث
        with open(lesson_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, f"تم إزالة {len(aos_matches) - 1} تكرار والاحتفاظ بواحد"
        
    except Exception as e:
        return False, f"خطأ: {str(e)}"

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
    
    print("🔧 إصلاح تكرارات AOS.init...")
    print("=" * 80)
    
    total_lessons = len(lessons)
    fixed_count = 0
    skipped_count = 0
    error_count = 0
    
    for lesson in sorted(lessons, key=lambda x: x['full_name']):
        print(f"\n📚 معالجة الدرس: {lesson['full_name']}")
        
        success, message = fix_duplicate_aos_init(lesson['path'])
        
        if success:
            print(f"✅ تم الإصلاح: {message}")
            fixed_count += 1
        elif "طبيعي" in message:
            print(f"⏭️ {message}")
            skipped_count += 1
        else:
            print(f"❌ فشل الإصلاح: {message}")
            error_count += 1
    
    print("\n" + "=" * 80)
    print(f"📈 ملخص النتائج:")
    print(f"📚 إجمالي الدروس: {total_lessons}")
    print(f"✅ الدروس المُصلحة: {fixed_count}")
    print(f"⏭️ الدروس المتخطاة: {skipped_count}")
    print(f"❌ الدروس التي فشل إصلاحها: {error_count}")
    
    if fixed_count > 0:
        print(f"\n🎉 تم إصلاح تكرارات AOS في {fixed_count} درس!")
        print(f"💡 الآن كل درس يحتوي على AOS.init واحد فقط")

if __name__ == "__main__":
    main()