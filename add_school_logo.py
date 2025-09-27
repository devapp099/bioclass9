#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت إضافة شعار المدرسة لجميع صفحات الدروس
يضيف شعار مثبت في الأعلى بتصميم جميل ومتجاوب
"""
import os
import shutil
from pathlib import Path

def create_backup(file_path):
    """إنشاء نسخة احتياطية من الملف"""
    backup_path = f"{file_path}.backup_logo_add"
    shutil.copy2(file_path, backup_path)
    print(f"✅ تم إنشاء نسخة احتياطية: {backup_path}")
    return backup_path

def add_school_logo_to_lesson(file_path):
    """إضافة شعار المدرسة لصفحة درس واحد"""
    try:
        # قراءة الملف
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # التحقق من عدم وجود الشعار مسبقاً
        if 'school-logo-header' in content:
            print(f"⚠️  الشعار موجود مسبقاً في: {file_path}")
            return False
        
        # إنشاء نسخة احتياطية
        create_backup(file_path)
        
        # CSS للشعار - يتم إضافته قبل إغلاق </style>
        logo_css = """
    
    .school-logo-header {
      position: fixed;
      top: 15px;
      right: 20px;
      z-index: 1000;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: 10px 16px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      animation: logoFloat 3s ease-in-out infinite alternate;
      transition: all 0.3s ease;
    }
    
    .school-logo-header:hover {
      transform: scale(1.05);
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .school-logo-header img {
      height: 45px;
      width: auto;
      filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.1));
      transition: all 0.3s ease;
    }
    
    .school-logo-header:hover img {
      filter: drop-shadow(0 4px 16px rgba(0, 0, 0, 0.2));
    }
    
    @keyframes logoFloat {
      0% { transform: translateY(0px); }
      100% { transform: translateY(-3px); }
    }
    
    .wrap {
      padding-top: 20px;
    }
    
    @media (max-width: 768px) {
      .school-logo-header {
        top: 10px;
        right: 10px;
        padding: 8px 12px;
      }
      
      .school-logo-header img {
        height: 35px;
      }
    }"""
        
        # إضافة CSS قبل إغلاق </style>
        content = content.replace('        </style>', logo_css + '\n        </style>')
        
        # تحديد المسار النسبي للصورة حسب موقع الدرس
        # حساب عدد المستويات للوصول للجذر
        relative_path = os.path.relpath(file_path, '.')
        depth = len(Path(relative_path).parts) - 1  # -1 لأننا لا نحسب اسم الملف
        logo_path = '../' * (depth - 1) + 'assets/images/school-logo.png'
        
        # HTML للشعار - يتم إضافته بعد <body>
        logo_html = f"""
  <div class="school-logo-header" data-aos="fade-down" data-aos-delay="300">
    <img src="{logo_path}" alt="شعار المدرسة" loading="eager">
  </div>
  """
        
        # إضافة HTML بعد <body>
        content = content.replace('<body>\n  <div class="wrap">', f'<body>{logo_html}\n  <div class="wrap">')
        
        # كتابة الملف المحدث
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ تم إضافة الشعار لـ: {file_path}")
        print(f"   مسار الشعار: {logo_path}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في معالجة {file_path}: {str(e)}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🏫 بدء إضافة شعار المدرسة لجميع صفحات الدروس...")
    print("=" * 60)
    
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
    print("=" * 60)
    
    # إضافة الشعار لكل ملف
    success_count = 0
    total_count = len(lesson_files)
    
    for file_path in lesson_files:
        print(f"\n🔄 معالجة: {file_path}")
        if add_school_logo_to_lesson(file_path):
            success_count += 1
    
    # التقرير النهائي
    print("\n" + "=" * 60)
    print("📊 التقرير النهائي:")
    print(f"   ✅ تم إضافة الشعار لـ: {success_count} ملف")
    print(f"   📁 إجمالي الملفات: {total_count}")
    print(f"   ⚠️  لم تحتاج لتعديل: {total_count - success_count} ملف")
    
    if success_count > 0:
        print("\n🎉 تم إضافة شعار المدرسة بنجاح!")
        print("💡 تم إنشاء نسخ احتياطية لجميع الملفات المُعدّلة")
        print("🏫 الشعار سيظهر في الجانب الأيمن العلوي لكل درس")
    else:
        print("\n⚠️  لا توجد ملفات تحتاج لإضافة الشعار")

if __name__ == "__main__":
    main()