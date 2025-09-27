#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت إزالة شعار المدرسة من جميع صفحات الدروس
يحتفظ بالشعار في الصفحة الرئيسية فقط
"""
import os
import shutil
from pathlib import Path

def create_backup(file_path):
    """إنشاء نسخة احتياطية من الملف"""
    backup_path = f"{file_path}.backup_logo_remove"
    shutil.copy2(file_path, backup_path)
    print(f"✅ تم إنشاء نسخة احتياطية: {backup_path}")
    return backup_path

def remove_school_logo_from_lesson(file_path):
    """إزالة شعار المدرسة من صفحة درس واحد"""
    try:
        # قراءة الملف
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # التحقق من وجود الشعار
        if 'school-logo-header' not in content:
            print(f"⚠️  لا يحتوي على شعار المدرسة: {file_path}")
            return False
        
        # إنشاء نسخة احتياطية
        create_backup(file_path)
        
        # إزالة CSS الخاص بالشعار
        logo_css_start = """
    
    .school-logo-header {"""
        logo_css_end = """    }
        </style>"""
        
        # البحث عن بداية ونهاية CSS الشعار
        start_index = content.find(logo_css_start)
        if start_index != -1:
            # البحث عن نهاية CSS (قبل </style>)
            end_search = content.find("    }\n        </style>", start_index)
            if end_search != -1:
                # إزالة كامل CSS الشعار
                before_css = content[:start_index]
                after_css = content[end_search + 5:]  # +5 لتخطي "    }"
                content = before_css + after_css
        
        # إزالة HTML الخاص بالشعار
        logo_html_start = """
  <div class="school-logo-header" data-aos="fade-down" data-aos-delay="300">
    <img src="../assets/images/school-logo.png" alt="شعار المدرسة" loading="eager">
  </div>
  """
        
        content = content.replace(logo_html_start, "\n  ")
        
        # إزالة padding-top الإضافي من .wrap إذا كان موجوداً
        content = content.replace("""    .wrap {
      padding-top: 20px;
    }
    """, "")
        
        # إزالة media query للشعار
        media_query = """    @media (max-width: 768px) {
      .school-logo-header {
        top: 10px;
        right: 10px;
        padding: 8px 12px;
      }
      
      .school-logo-header img {
        height: 35px;
      }
    }"""
        
        content = content.replace(media_query, "")
        
        # كتابة الملف المحدث
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ تم إزالة الشعار من: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في معالجة {file_path}: {str(e)}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🗑️  بدء إزالة شعار المدرسة من جميع صفحات الدروس...")
    print("🏫 (الاحتفاظ بالشعار في الصفحة الرئيسية فقط)")
    print("=" * 60)
    
    # العثور على جميع ملفات الدروس (بدون الصفحة الرئيسية)
    lesson_files = []
    base_path = Path('.')
    
    for unit_dir in base_path.glob('unit-*'):
        if unit_dir.is_dir():
            for lesson_dir in unit_dir.glob('lesson-*'):
                if lesson_dir.is_dir():
                    index_file = lesson_dir / 'index.html'
                    if index_file.exists():
                        lesson_files.append(str(index_file))
    
    print(f"📁 تم العثور على {len(lesson_files)} ملف درس")
    print("=" * 60)
    
    # إزالة الشعار من كل ملف درس
    success_count = 0
    total_count = len(lesson_files)
    
    for file_path in lesson_files:
        print(f"\n🔄 معالجة: {file_path}")
        if remove_school_logo_from_lesson(file_path):
            success_count += 1
    
    # التقرير النهائي
    print("\n" + "=" * 60)
    print("📊 التقرير النهائي:")
    print(f"   ✅ تم إزالة الشعار من: {success_count} ملف")
    print(f"   📁 إجمالي الملفات: {total_count}")
    print(f"   ⚠️  لم تحتاج لتعديل: {total_count - success_count} ملف")
    
    if success_count > 0:
        print("\n🎉 تم إزالة الشعار من صفحات الدروس بنجاح!")
        print("🏫 الشعار متوفر الآن في الصفحة الرئيسية فقط")
        print("💡 تم إنشاء نسخ احتياطية لجميع الملفات المُعدّلة")
    else:
        print("\n⚠️  لا توجد ملفات تحتاج لإزالة الشعار")

if __name__ == "__main__":
    main()