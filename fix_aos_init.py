#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def fix_aos_initialization(lesson_path):
    """إضافة تهيئة AOS للدروس"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # التحقق من وجود AOS.init()
        if 'AOS.init()' in content:
            return False, "AOS مهيأ بالفعل"
        
        # البحث عن نهاية JavaScript الرئيسي
        # البحث عن آخر updateMeta() أو مكان مشابه لإضافة AOS.init()
        insert_points = [
            r'(updateMeta\(\);)',
            r'(document\.getElementById\([\'"]countTotal[\'"].*?;)',
            r'(SoundSystem\.init\(\);)',
            r'(console\.log\([\'"].*تم تهيئة.*[\'"].*\);)'
        ]
        
        inserted = False
        new_content = content
        
        for pattern in insert_points:
            if re.search(pattern, content):
                # إضافة تهيئة AOS بعد النقطة المعثور عليها
                aos_init_code = '''
    
    // تهيئة AOS للأنيميشن
    AOS.init({
      duration: 700,
      easing: 'ease',
      once: true,
      offset: 50
    });
    
    console.log('✨ تم تهيئة AOS للأنيميشن');'''
                
                new_content = re.sub(pattern, r'\1' + aos_init_code, content)
                inserted = True
                break
        
        if not inserted:
            # إذا لم نجد نقطة إدراج مناسبة، أضف قبل نهاية script
            script_end_pattern = r'(\s*</script>)'
            if re.search(script_end_pattern, content):
                aos_init_code = '''
    
    // تهيئة AOS للأنيميشن
    AOS.init({
      duration: 700,
      easing: 'ease',
      once: true,
      offset: 50
    });
    
    console.log('✨ تم تهيئة AOS للأنيميشن');
  '''
                new_content = re.sub(script_end_pattern, aos_init_code + r'\1', content)
                inserted = True
        
        if not inserted:
            return False, "لم يتم العثور على مكان مناسب لإضافة AOS.init()"
        
        # كتابة الملف المحدث
        with open(lesson_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "تم إضافة تهيئة AOS بنجاح"
        
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
    
    print("🔧 إصلاح تهيئة AOS في جميع الدروس...")
    print("=" * 80)
    
    total_lessons = len(lessons)
    fixed_count = 0
    skipped_count = 0
    error_count = 0
    
    for lesson in sorted(lessons, key=lambda x: x['full_name']):
        print(f"\n📚 معالجة الدرس: {lesson['full_name']}")
        
        success, message = fix_aos_initialization(lesson['path'])
        
        if success:
            print(f"✅ تم الإصلاح بنجاح")
            fixed_count += 1
        elif "مهيأ بالفعل" in message:
            print(f"⏭️ {message}")
            skipped_count += 1
        else:
            print(f"❌ فشل الإصلاح: {message}")
            error_count += 1
    
    print("\n" + "=" * 80)
    print(f"📈 ملخص النتائج:")
    print(f"📚 إجمالي الدروس: {total_lessons}")
    print(f"✅ الدروس المُصلحة: {fixed_count}")
    print(f"⏭️ الدروس المتخطاة (مهيأة مسبقاً): {skipped_count}")
    print(f"❌ الدروس التي فشل إصلاحها: {error_count}")
    
    if fixed_count > 0:
        print(f"\n🎉 تم إصلاح {fixed_count} درس!")
        print(f"📝 AOS سيعمل الآن بشكل صحيح وستظهر الأنيميشن")
        print(f"💡 هذا يجب أن يحل مشكلة عدم ظهور المحتوى")
    else:
        print(f"\n💡 جميع الدروس كانت مهيأة بالفعل!")

if __name__ == "__main__":
    main()