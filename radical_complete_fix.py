#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح جذري شامل - نسخ الدرس المثالي 1-1 وتطبيقه على جميع الدروس
Radical comprehensive fix - Copy perfect lesson 1-1 structure to all lessons
"""

import os
import re
from pathlib import Path

# قائمة الدروس مع معلوماتها
LESSONS_DATA = {
    "lesson-1-2": {
        "title": "🧪 درس 1-2 — رسم الخلايا وحساب التكبير",
        "h1": "رسم الخلايا وحساب التكبير",
        "lead": "تعلم كيفية رسم الخلايا بشكل علمي دقيق وحساب التكبير المطلوب للمشاهدة المثلى"
    },
    "lesson-1-3": {
        "title": "🔍 درس 1-3 — أجزاء الخلية ووظائفها",
        "h1": "أجزاء الخلية ووظائفها",
        "lead": "استكشف التراكيب المختلفة داخل الخلية ووظائفها الحيوية المتخصصة"
    },
    "lesson-2-1": {
        "title": "🚛 درس 2-1 — النقل عبر الأغشية",
        "h1": "النقل عبر الأغشية",
        "lead": "فهم آليات النقل المختلفة عبر أغشية الخلايا والعوامل المؤثرة عليها"
    },
    "lesson-2-2": {
        "title": "💧 درس 2-2 — الانتشار والخاصية الأسموزية",
        "h1": "الانتشار والخاصية الأسموزية",
        "lead": "تعلم مفاهيم الانتشار والأسموزية وتطبيقاتها في الخلايا الحية"
    },
    "lesson-2-3": {
        "title": "⚡ درس 2-3 — النقل النشط والسلبي",
        "h1": "النقل النشط والسلبي",
        "lead": "المقارنة بين أنواع النقل المختلفة ومتطلبات الطاقة لكل منها"
    },
    "lesson-3-1": {
        "title": "🧬 درس 3-1 — الكربوهيدرات والدهون",
        "h1": "الكربوهيدرات والدهون",
        "lead": "دراسة تركيب ووظائف الكربوهيدرات والدهون في الكائنات الحية"
    },
    "lesson-3-2": {
        "title": "🧪 درس 3-2 — البروتينات والأحماض النووية",
        "h1": "البروتينات والأحماض النووية",
        "lead": "فهم التركيب المعقد للبروتينات والأحماض النووية ووظائفها"
    },
    "lesson-3-3": {
        "title": "⚗️ درس 3-3 — الإنزيمات وآلية عملها",
        "h1": "الإنزيمات وآلية عملها",
        "lead": "استكشاف عالم الإنزيمات والعوامل المؤثرة على نشاطها"
    },
    "lesson-4-1": {
        "title": "🍎 درس 4-1 — التغذية والهضم",
        "h1": "التغذية والهضم",
        "lead": "فهم عمليات التغذية والهضم وأهميتها للكائنات الحية"
    },
    "lesson-4-2": {
        "title": "🔄 درس 4-2 — الامتصاص والنقل",
        "h1": "الامتصاص والنقل",
        "lead": "تعلم آليات امتصاص المواد الغذائية ونقلها في الجسم"
    },
    "lesson-5-1": {
        "title": "💨 درس 5-1 — التنفس الخلوي",
        "h1": "التنفس الخلوي",
        "lead": "دراسة عمليات إنتاج الطاقة في الخلايا والعوامل المؤثرة عليها"
    },
    "lesson-6-1": {
        "title": "⚖️ درس 6-1 — التوازن المائي",
        "h1": "التوازن المائي", 
        "lead": "فهم آليات المحافظة على التوازن المائي في الكائنات الحية"
    },
    "lesson-6-2": {
        "title": "🌡️ درس 6-2 — تنظيم درجة الحرارة",
        "h1": "تنظيم درجة الحرارة",
        "lead": "استكشاف طرق تنظيم درجة حرارة الجسم والتكيف مع البيئة"
    },
    "lesson-6-3": {
        "title": "🍬 درس 6-3 — تنظيم السكر في الدم",
        "h1": "تنظيم السكر في الدم",
        "lead": "تعلم آليات التحكم في مستوى السكر والهرمونات المنظمة"
    },
    "lesson-6-4": {
        "title": "🧠 درس 6-4 — الجهاز العصبي والتوازن",
        "h1": "الجهاز العصبي والتوازن",
        "lead": "فهم دور الجهاز العصبي في المحافظة على التوازن الداخلي"
    }
}

def read_perfect_lesson():
    """قراءة الدرس المثالي 1-1"""
    perfect_path = "unit-1-cells/lesson-1-1/index.html"
    try:
        with open(perfect_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ خطأ في قراءة الدرس المثالي: {e}")
        return None

def create_lesson_from_template(template_content, lesson_key, lesson_data):
    """إنشاء درس جديد من القالب المثالي"""
    content = template_content
    
    # تغيير العنوان
    content = re.sub(
        r'<title>[^<]+</title>',
        f'<title>{lesson_data["title"]}</title>',
        content
    )
    
    # تغيير H1
    content = re.sub(
        r'<h1>[^<]+</h1>',
        f'<h1>{lesson_data["h1"]}</h1>',
        content
    )
    
    # تغيير المقدمة
    content = re.sub(
        r'<p class="lead">[^<]+</p>',
        f'<p class="lead">{lesson_data["lead"]}</p>',
        content
    )
    
    return content

def fix_lesson_completely(lesson_path, lesson_key):
    """إصلاح شامل لدرس واحد"""
    try:
        # قراءة القالب المثالي
        perfect_content = read_perfect_lesson()
        if not perfect_content:
            return False
        
        # الحصول على بيانات الدرس
        lesson_data = LESSONS_DATA.get(lesson_key)
        if not lesson_data:
            print(f"⚠️  بيانات غير موجودة لـ {lesson_key}")
            return False
        
        # إنشاء المحتوى الجديد
        new_content = create_lesson_from_template(perfect_content, lesson_key, lesson_data)
        
        # حفظ الملف الجديد
        with open(lesson_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إصلاح {lesson_path}: {e}")
        return False

def main():
    """الدالة الرئيسية للإصلاح الجذري الشامل"""
    print("🚀 بدء الإصلاح الجذري الشامل...")
    print("📋 سيتم نسخ الدرس المثالي 1-1 وتطبيقه على جميع الدروس")
    
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
                            print(f"⭐ تخطي: {item} (الدرس المثالي - المرجع)")
                            continue
                        
                        total_count += 1
                        print(f"🔄 إصلاح جذري: {item}")
                        
                        if fix_lesson_completely(index_file, item):
                            fixed_count += 1
                            print(f"✅ تم الإصلاح الجذري: {item}")
                        else:
                            print(f"❌ فشل الإصلاح: {item}")
    
    print(f"\n🎉 انتهاء الإصلاح الجذري الشامل!")
    print(f"✅ تم إصلاح {fixed_count} درس من أصل {total_count}")
    
    if fixed_count == total_count:
        print("🌟 جميع الدروس أصبحت مطابقة تماماً للدرس المثالي!")
        print("🚀 كل درس يعمل بنفس الكفاءة والجودة المثالية!")
    else:
        print(f"⚠️  {total_count - fixed_count} دروس تحتاج مراجعة")

if __name__ == "__main__":
    main()