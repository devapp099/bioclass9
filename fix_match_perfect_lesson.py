#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح شامل لجعل جميع الدروس متطابقة مع الدرس الأول المثالي
Complete fix to make all lessons identical to the perfect lesson 1-1
"""

import os
import re

def fix_lesson_to_match_perfect(file_path):
    """إصلاح درس واحد ليطابق الدرس المثالي 1-1"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. إصلاح مكان مكتبة Howler.js - يجب أن تكون في head
        # إزالة Howler من المكان الخطأ (بعد CSS)
        content = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/howler@2\.2\.4/dist/howler\.min\.js"></script>\s*</head>', '</head>', content)
        
        # إضافة Howler في المكان الصحيح (في head قبل إغلاقه)
        if 'howler' not in content[:500]:  # إذا لم تكن موجودة في head
            content = content.replace(
                '<script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>',
                '<script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>\n  <script src="https://cdn.jsdelivr.net/npm/howler@2.2.4/dist/howler.min.js"></script>'
            )
        
        # 2. إصلاح أنماط CSS للخلفيات والحدود
        # تصحيح ألوان الخلفية للأسئلة
        content = content.replace(
            'background:rgba(0,0,0,.03)',
            'background:rgba(255,255,255,.03)'
        )
        
        # تصحيح ألوان الحدود للاختيارات
        content = content.replace(
            'border:1px solid rgba(0,0,0,.08)',  
            'border:1px solid rgba(255,255,255,.08)'
        )
        
        # تصحيح hover للاختيارات
        content = content.replace(
            'background:rgba(0,0,0,.06)',
            'background:rgba(255,255,255,.10)'
        )
        
        # 3. إصلاح ألوان الاختيارات الصحيحة والخاطئة
        content = content.replace(
            'border-color: rgba(16,185,129,.55); background: rgba(16,185,129,.12)',
            'border-color: rgba(52,211,153,.7); background: rgba(52,211,153,.10)'
        )
        
        content = content.replace(
            'border-color: rgba(239,68,68,.55); background: rgba(239,68,68,.12)',
            'border-color: rgba(251,113,133,.7); background: rgba(251,113,133,.10)'
        )
        
        # 4. إضافة النمط المفقود للاختيارات
        if '.choice{ display:flex; align-items:center; gap:10px; padding:12px 14px; border:1px solid rgba(255,255,255,.08);' not in content:
            choice_style = '''    .choice{ display:flex; align-items:center; gap:10px; padding:12px 14px; border:1px solid rgba(255,255,255,.08);
      border-radius:14px; background:rgba(0,0,0,.18); cursor:pointer; user-select:none;
      transition:transform .1s ease, background .2s ease, border .2s ease; color:var(--text) }'''
            
            # البحث عن مكان مناسب لإضافة النمط
            if '.choice{' in content:
                content = re.sub(
                    r'\.choice\{[^}]+\}',
                    choice_style,
                    content
                )
        
        # 5. التأكد من وجود شريط التقدم الصحيح
        progress_style = '''    .progress{display:flex; align-items:center; gap:8px; font-weight:800; color:#7c2d12; margin-top:6px}
    .bar{flex:1; height:8px; background:rgba(0,0,0,.08); border-radius:999px; overflow:hidden}
    .bar>span{display:block; height:100%; width:0%; background:linear-gradient(90deg,#f59e0b,#d97706); transition:width .25s ease}'''
        
        if '.bar>span{' not in content:
            content = content.replace(
                '.bar{flex:1; height:8px; background:rgba(0,0,0,.08); border-radius:999px; overflow:hidden}',
                progress_style
            )
        
        # 6. إصلاح مشكلة العرض المخفي
        content = content.replace(
            'display:none" data-aos="fade-up"',
            'display:block" data-aos="fade-up"'
        )
        
        # حفظ الملف
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في معالجة {file_path}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔧 بدء الإصلاح الشامل لجعل جميع الدروس متطابقة مع الدرس المثالي...")
    
    # مجلدات الوحدات
    units = [
        'unit-1-cells',
        'unit-2-transport', 
        'unit-3-biomolecules',
        'unit-4-nutrition',
        'unit-5-respiration',
        'unit-6-homeostasis'
    ]
    
    fixed_count = 0
    total_count = 0
    
    for unit in units:
        unit_path = unit
        if os.path.exists(unit_path):
            # البحث عن جميع الدروس في الوحدة
            for item in os.listdir(unit_path):
                lesson_path = os.path.join(unit_path, item)
                if os.path.isdir(lesson_path) and item.startswith('lesson-'):
                    index_file = os.path.join(lesson_path, 'index.html')
                    if os.path.exists(index_file):
                        # تخطي الدرس 1-1 لأنه المثالي
                        if item == 'lesson-1-1':
                            print(f"⭐ تخطي: {item} (الدرس المثالي)")
                            continue
                            
                        total_count += 1
                        print(f"🔄 معالجة: {item}")
                        
                        if fix_lesson_to_match_perfect(index_file):
                            fixed_count += 1
                            print(f"✅ تم إصلاح: {item}")
                        else:
                            print(f"❌ فشل إصلاح: {item}")
    
    print(f"\n🎉 انتهاء العملية!")
    print(f"✅ تم إصلاح {fixed_count} درس من أصل {total_count}")
    
    if fixed_count == total_count:
        print("🌟 جميع الدروس أصبحت متطابقة مع الدرس المثالي!")
    else:
        print(f"⚠️  {total_count - fixed_count} دروس تحتاج مراجعة")

if __name__ == "__main__":
    main()