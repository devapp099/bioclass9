#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت إصلاح عناوين جميع الدروس بحذر شديد
يقوم بتحديث العناوين دون التأثير على المحتوى الأساسي
"""
import os
import re
import shutil
from pathlib import Path

# قاموس العناوين الصحيحة لكل درس
LESSON_TITLES = {
    # الوحدة 1 - الخلايا
    'unit-1-cells/lesson-1-1': '🧬 نشاط تفاعلي — الدرس 1-1: الخلايا الحيوانية والنباتية',
    'unit-1-cells/lesson-1-2': '🧪 نشاط تفاعلي — الدرس 1-2: رسم الخلايا وحساب التكبير',
    'unit-1-cells/lesson-1-3': '🔬 نشاط تفاعلي — الدرس 1-3: الخلايا المتخصصة',
    
    # الوحدة 2 - النقل
    'unit-2-transport/lesson-2-1': '💧 نشاط تفاعلي — الدرس 2-1: الانتشار والتناضح',
    'unit-2-transport/lesson-2-2': '🫀 نشاط تفاعلي — الدرس 2-2: نقل المواد في النباتات',
    'unit-2-transport/lesson-2-3': '🩸 نشاط تفاعلي — الدرس 2-3: الدورة الدموية في الإنسان',
    
    # الوحدة 3 - الجزيئات الحيوية
    'unit-3-biomolecules/lesson-3-1': '🍞 نشاط تفاعلي — الدرس 3-1: الكربوهيدرات والدهون',
    'unit-3-biomolecules/lesson-3-2': '🥩 نشاط تفاعلي — الدرس 3-2: البروتينات والاختبارات الغذائية',
    'unit-3-biomolecules/lesson-3-3': '🧪 نشاط تفاعلي — الدرس 3-3: الإنزيمات',
    
    # الوحدة 4 - التغذية
    'unit-4-nutrition/lesson-4-1': '🦷 نشاط تفاعلي — الدرس 4-1: التغذية في الإنسان',
    'unit-4-nutrition/lesson-4-2': '🌿 نشاط تفاعلي — الدرس 4-2: التمثيل الضوئي',
    
    # الوحدة 5 - التنفس
    'unit-5-respiration/lesson-5-1': '🫁 نشاط تفاعلي — الدرس 5-1: التنفس في الإنسان',
    'unit-5-respiration/lesson-5-2': '🔬 نشاط تفاعلي — الدرس 5-2: التنفس الخلوي',
    
    # الوحدة 6 - التوازن الداخلي
    'unit-6-homeostasis/lesson-6-1': '🧠 نشاط تفاعلي — الدرس 6-1: التنسيق والاستجابة',
    'unit-6-homeostasis/lesson-6-2': '👁️ نشاط تفاعلي — الدرس 6-2: الجهاز العصبي',
    'unit-6-homeostasis/lesson-6-3': '👀 نشاط تفاعلي — الدرس 6-3: العين والرؤية',
    'unit-6-homeostasis/lesson-6-4': '🔬 نشاط تفاعلي — الدرس 6-4: الهرمونات',
    'unit-6-homeostasis/lesson-6-5': '⚖️ نشاط تفاعلي — الدرس 6-5: التوازن الداخلي',
}

def create_backup(file_path):
    """إنشاء نسخة احتياطية من الملف"""
    backup_path = f"{file_path}.backup_title_fix"
    shutil.copy2(file_path, backup_path)
    print(f"✅ تم إنشاء نسخة احتياطية: {backup_path}")
    return backup_path

def extract_title_from_head(html_content):
    """استخراج العنوان من قسم head"""
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.DOTALL)
    if title_match:
        title = title_match.group(1).strip()
        # تحويل عنوان head إلى عنوان نشاط تفاعلي
        if '—' in title:
            parts = title.split('—', 1)
            if len(parts) == 2:
                icon_part = parts[0].strip()
                lesson_part = parts[1].strip()
                return f"{icon_part} نشاط تفاعلي — {lesson_part}"
    return None

def fix_lesson_title(file_path):
    """إصلاح عنوان درس واحد"""
    try:
        # قراءة الملف
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # التحقق من وجود العنوان الخاطئ
        wrong_title = '🧬 نشاط تفاعلي — الدرس 1-1: الخلايا الحيوانية والنباتية'
        if wrong_title not in content:
            print(f"⚠️  لا يحتوي على العنوان الخاطئ: {file_path}")
            return False
        
        # إنشاء نسخة احتياطية
        create_backup(file_path)
        
        # تحديد العنوان الصحيح
        correct_title = None
        
        # البحث في قاموس العناوين
        for lesson_key, title in LESSON_TITLES.items():
            if lesson_key in file_path.replace('\\', '/'):
                correct_title = title
                break
        
        # إذا لم نجد في القاموس، نحاول استخراج من head
        if not correct_title:
            correct_title = extract_title_from_head(content)
        
        if not correct_title:
            print(f"❌ لا يمكن تحديد العنوان الصحيح لـ: {file_path}")
            return False
        
        # استبدال العنوان
        new_content = content.replace(wrong_title, correct_title)
        
        # التحقق من التغيير
        if new_content == content:
            print(f"⚠️  لم يتم إجراء أي تغيير في: {file_path}")
            return False
        
        # كتابة الملف المحدث
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ تم إصلاح العنوان في: {file_path}")
        print(f"   العنوان الجديد: {correct_title}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في معالجة {file_path}: {str(e)}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔧 بدء إصلاح عناوين جميع الدروس...")
    print("=" * 50)
    
    # العثور على جميع ملفات الدروس
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
    print("=" * 50)
    
    # إصلاح كل ملف
    success_count = 0
    total_count = len(lesson_files)
    
    for file_path in lesson_files:
        print(f"\n🔄 معالجة: {file_path}")
        if fix_lesson_title(file_path):
            success_count += 1
    
    # التقرير النهائي
    print("\n" + "=" * 50)
    print("📊 التقرير النهائي:")
    print(f"   ✅ تم إصلاح: {success_count} ملف")
    print(f"   📁 إجمالي الملفات: {total_count}")
    print(f"   ⚠️  لم تحتاج لإصلاح: {total_count - success_count} ملف")
    
    if success_count > 0:
        print("\n🎉 تم إصلاح العناوين بنجاح!")
        print("💡 تم إنشاء نسخ احتياطية لجميع الملفات المُعدّلة")
    else:
        print("\n⚠️  لا توجد ملفات تحتاج لإصلاح")

if __name__ == "__main__":
    main()