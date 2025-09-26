#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def comprehensive_lesson_fix(lesson_path):
    """إصلاح شامل للدرس"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixes_applied = []
        
        # 1. إزالة الفواصل المنقوطة الفارغة
        if ';\n    ;' in content:
            content = content.replace(';\n    ;', '')
            fixes_applied.append("إزالة فواصل منقوطة فارغة")
        
        # 2. إصلاح AOS.init المكسور
        broken_aos_pattern = r'// تهيئة AOS للأنيميشن\s*\n\s*duration:'
        if re.search(broken_aos_pattern, content):
            # استبدال AOS المكسور
            content = re.sub(
                r'// تهيئة AOS للأنيميشن\s*\n\s*duration:\s*700,\s*easing:\s*[\'"]ease[\'"],\s*once:\s*true,\s*offset:\s*50\s*\}\);?\s*console\.log\([\'"].*تم تهيئة AOS.*[\'"].*\);',
                '',
                content,
                flags=re.DOTALL
            )
            fixes_applied.append("إزالة AOS.init مكسور")
        
        # 3. التأكد من وجود AOS.init صحيح واحد فقط
        aos_matches = list(re.finditer(r'AOS\.init\s*\([^)]*\);?', content))
        if len(aos_matches) > 1:
            # إزالة جميع التكرارات عدا الأخير
            for i in range(len(aos_matches) - 1):
                match = aos_matches[i]
                start, end = match.span()
                # البحث عن بداية السطر ونهايته
                content_before = content[:start]
                content_after = content[end:]
                
                # العثور على بداية السطر
                line_start = content_before.rfind('\n') + 1
                # العثور على نهاية السطر
                line_end = content_after.find('\n')
                if line_end == -1:
                    line_end = len(content_after)
                
                # إزالة السطر الكامل
                content = content[:line_start] + content[end + line_end:]
                
                # تحديث المواضع
                for j in range(i + 1, len(aos_matches)):
                    aos_matches[j] = type(aos_matches[j])(
                        aos_matches[j].pattern,
                        aos_matches[j].string,
                        aos_matches[j].pos - (end + line_end - line_start),
                        aos_matches[j].endpos - (end + line_end - line_start)
                    )
            
            fixes_applied.append(f"إزالة {len(aos_matches) - 1} تكرار AOS")
        
        # 4. إضافة AOS.init إذا لم يكن موجود
        if 'AOS.init' not in content:
            # البحث عن مكان مناسب للإضافة
            insert_patterns = [
                (r'(renderQuestions\(\);\s*updateMeta\(\);)', 'بعد renderQuestions'),
                (r'(updateMeta\(\);)', 'بعد updateMeta'),
                (r'(\s*</script>)', 'قبل نهاية script')
            ]
            
            aos_code = '''
    
    // تهيئة AOS للأنيميشن
    AOS.init({
      duration: 700,
      easing: 'ease',
      once: true,
      offset: 50
    });
    
    console.log('✨ تم تهيئة AOS للأنيميشن');'''
            
            inserted = False
            for pattern, description in insert_patterns:
                if re.search(pattern, content):
                    content = re.sub(pattern, r'\1' + aos_code, content)
                    fixes_applied.append(f"إضافة AOS.init {description}")
                    inserted = True
                    break
        
        # 5. تنظيف الأسطر الفارغة المتعددة
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        fixes_applied.append("تنظيف الأسطر الفارغة")
        
        # 6. إصلاح أخطاء JavaScript شائعة
        # إصلاح الأقواس المفقودة
        content = re.sub(r'(\w+)\.addEventListener\([\'"]click[\'"],\s*\(\s*\)\s*=>\s*\{[^}]*\}(?!\);)', r'\1.addEventListener("click", () => {\g<0>});', content)
        
        # كتابة الملف المحدث
        with open(lesson_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True, fixes_applied
        
    except Exception as e:
        return False, [f"خطأ: {str(e)}"]

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
    
    print("🔧 إصلاح شامل لجميع الدروس...")
    print("=" * 80)
    
    total_lessons = len(lessons)
    fixed_count = 0
    error_count = 0
    
    for lesson in sorted(lessons, key=lambda x: x['full_name']):
        print(f"\n📚 معالجة الدرس: {lesson['full_name']}")
        
        success, fixes = comprehensive_lesson_fix(lesson['path'])
        
        if success:
            if fixes:
                print(f"✅ تم تطبيق {len(fixes)} إصلاح:")
                for fix in fixes:
                    print(f"  - {fix}")
                fixed_count += 1
            else:
                print("⏭️ لا يحتاج إصلاح")
        else:
            print(f"❌ فشل الإصلاح:")
            for error in fixes:
                print(f"  - {error}")
            error_count += 1
    
    print("\n" + "=" * 80)
    print(f"📈 ملخص النتائج:")
    print(f"📚 إجمالي الدروس: {total_lessons}")
    print(f"✅ الدروس المُصلحة: {fixed_count}")
    print(f"❌ الدروس التي فشل إصلاحها: {error_count}")
    
    if fixed_count > 0:
        print(f"\n🎉 تم إصلاح {fixed_count} درس بشكل شامل!")
        print(f"💡 يجب أن تعمل جميع الدروس الآن بشكل صحيح")

if __name__ == "__main__":
    main()