#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تحديث نمط أسماء المصممات - اللون الأخضر والخط العادي
Update designers names style - green color and normal font weight
"""

import os
import re

def update_designers_style(file_path):
    """تحديث نمط أسماء المصممات في ملف واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # تحديث CSS للمصممات
        old_credit_style = ".credit{color:var(--text); font-weight:800}"
        new_credit_style = """.credit{color:var(--text); font-weight:800}
    .credit .designers{color:#10b981; font-weight:400; font-style:normal}"""
        
        # استبدال النمط القديم
        if old_credit_style in content:
            content = content.replace(old_credit_style, new_credit_style)
            updated = True
        else:
            # إذا لم يجد النمط القديم، ابحث عن .credit واضف النمط الجديد
            credit_pattern = r'(\.credit\{[^}]+\})'
            if re.search(credit_pattern, content):
                content = re.sub(
                    credit_pattern,
                    r'\1\n    .credit .designers{color:#10b981; font-weight:400; font-style:normal}',
                    content
                )
                updated = True
            else:
                updated = False
        
        # تحديث HTML لتطبيق النمط على أسماء المصممات
        designers_pattern = r'(🎨 تصميم: )([^—]+)(— 🏫)'
        if re.search(designers_pattern, content):
            content = re.sub(
                designers_pattern,
                r'\1<span class="designers">\2</span>\3',
                content
            )
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
    print("🎨 بدء تحديث نمط أسماء المصممات...")
    print("✨ اللون: أخضر (#10b981)")
    print("✨ الخط: عادي (غير غامق)")
    
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
        if update_designers_style(file_path):
            updated_count += 1
            print(f"✅ تم التحديث: {file_path}")
        else:
            print(f"ℹ️  لا يحتاج تحديث: {file_path}")
    
    print(f"\n🎉 انتهاء العملية!")
    print(f"✅ تم تحديث {updated_count} ملف من أصل {total_count}")
    
    if updated_count > 0:
        print("🌟 أسماء المصممات الآن باللون الأخضر والخط العادي!")
        print("🎨 النمط: color: #10b981; font-weight: 400;")
    else:
        print("ℹ️  لم يتم العثور على ملفات تحتاج تحديث")

if __name__ == "__main__":
    main()