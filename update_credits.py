#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحديث أسماء المصممين والأستاذة في جميع الدروس
Update designers' names and teacher's name in all lessons
"""

import os
import re
import glob

def update_credits_in_file(file_path):
    """تحديث معلومات التصميم والإشراف في ملف واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # النص القديم
        old_text = "🎨 تصميم: الوتين الضامرية |لمار السيابية|مها المعمرية|مريم محمود البلوشية|مريم وائل البلوشية|</span> — 🏫 مدرسة عاتكة بنت زيد — تحت إشراف الأستاذة سامية 👩‍🏫"
        
        # النص الجديد مع إضافة مريم زكي العويسية وتغيير اسم الأستاذة إلى وفاء
        new_text = "🎨 تصميم: الوتين الضامرية |لمار السيابية|مها المعمرية|مريم محمود البلوشية|مريم وائل البلوشية|مريم زكي العويسية|</span> — 🏫 مدرسة عاتكة بنت زيد — تحت إشراف الأستاذة وفاء 👩‍🏫"
        
        # التحديث الأول
        if old_text in content:
            content = content.replace(old_text, new_text)
            updated = True
        else:
            # البحث عن نمط مختلف في الملفات (مع spaces)
            old_text_alt = "🎨 تصميم: الوتين الضامرية | لمار السيابية | مها المعمرية | مريم محمود البلوشية | مريم وائل البلوشية — 🏫 مدرسة عاتكة بنت زيد — تحت إشراف الأستاذة سامية 👩‍🏫"
            new_text_alt = "🎨 تصميم: الوتين الضامرية | لمار السيابية | مها المعمرية | مريم محمود البلوشية | مريم وائل البلوشية | مريم زكي العويسية — 🏫 مدرسة عاتكة بنت زيد — تحت إشراف الأستاذة وفاء 👩‍🏫"
            
            if old_text_alt in content:
                content = content.replace(old_text_alt, new_text_alt)
                updated = True
            else:
                # البحث عن أي نمط يحتوي على "سامية" و تحديثه
                pattern = r'(🎨 تصميم:.*?)— 🏫 مدرسة عاتكة بنت زيد — تحت إشراف الأستاذة سامية.*?👩‍🏫'
                replacement = r'\1 مريم زكي العويسية| — 🏫 مدرسة عاتكة بنت زيد — تحت إشراف الأستاذة وفاء 👩‍🏫'
                
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    updated = True
                else:
                    # تحديث اسم الأستاذة فقط إذا وُجد
                    if 'الأستاذة سامية' in content:
                        content = content.replace('الأستاذة سامية', 'الأستاذة وفاء')
                        updated = True
                    else:
                        updated = False
        
        # إضافة مريم زكي العويسية إذا لم تكن موجودة
        if 'مريم زكي العويسية' not in content and 'تصميم:' in content:
            # البحث عن نهاية قائمة المصممين وإضافة الاسم
            pattern = r'(مريم وائل البلوشية)(\|?)(</span>)'
            replacement = r'\1|مريم زكي العويسية|\3'
            content = re.sub(pattern, replacement, content)
            updated = True
        
        if updated:
            # حفظ الملف المحدث
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ خطأ في معالجة {file_path}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔄 بدء تحديث أسماء المصممين والأستاذة...")
    print("✨ إضافة: مريم زكي العويسية")
    print("🔄 تغيير: الأستاذة سامية → الأستاذة وفاء")
    
    # البحث عن جميع ملفات HTML
    html_files = []
    
    # إضافة الملف الرئيسي
    if os.path.exists('index.html'):
        html_files.append('index.html')
    
    # إضافة قالب الدرس
    if os.path.exists('lesson_template.html'):
        html_files.append('lesson_template.html')
    
    # إضافة ملف النسخة الاحتياطية
    if os.path.exists('lesson-1-2-backup.html'):
        html_files.append('lesson-1-2-backup.html')
    
    # البحث في مجلدات الوحدات
    units = [
        'unit-1-cells',
        'unit-2-transport', 
        'unit-3-biomolecules',
        'unit-4-nutrition',
        'unit-5-respiration',
        'unit-6-homeostasis'
    ]
    
    for unit in units:
        if os.path.exists(unit):
            for lesson_dir in os.listdir(unit):
                lesson_path = os.path.join(unit, lesson_dir)
                if os.path.isdir(lesson_path) and lesson_dir.startswith('lesson-'):
                    index_file = os.path.join(lesson_path, 'index.html')
                    if os.path.exists(index_file):
                        html_files.append(index_file)
    
    updated_count = 0
    total_count = len(html_files)
    
    for file_path in html_files:
        print(f"🔄 معالجة: {file_path}")
        if update_credits_in_file(file_path):
            updated_count += 1
            print(f"✅ تم التحديث: {file_path}")
        else:
            print(f"ℹ️  لا يحتاج تحديث: {file_path}")
    
    print(f"\n🎉 انتهاء العملية!")
    print(f"✅ تم تحديث {updated_count} ملف من أصل {total_count}")
    
    if updated_count > 0:
        print("🌟 تم إضافة مريم زكي العويسية إلى قائمة المصممين!")
        print("🌟 تم تغيير اسم الأستاذة من سامية إلى وفاء!")
    else:
        print("ℹ️  لم يتم العثور على ملفات تحتاج تحديث")

if __name__ == "__main__":
    main()