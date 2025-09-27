#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص شامل للأقسام المفقودة - مقارنة مع المرجع الأصلي
"""

import os
import re

def comprehensive_check(main_file, reference_file):
    """فحص شامل لمقارنة الملف الرئيسي مع المرجع"""
    try:
        # قراءة الملفات
        with open(main_file, 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        if os.path.exists(reference_file):
            with open(reference_file, 'r', encoding='utf-8') as f:
                ref_content = f.read()
        else:
            print(f"❌ الملف المرجعي غير موجود: {reference_file}")
            return False
        
        print(f"\n🔍 فحص شامل للدرس: {main_file}")
        print("=" * 70)
        
        # 1. فحص أهداف الدرس
        print("🎯 أهداف الدرس:")
        if '<section class="objectives"' in ref_content or 'الأهداف' in ref_content:
            if '<section class="objectives"' in main_content or 'الأهداف' in main_content:
                print("  ✅ أهداف الدرس موجودة")
            else:
                print("  ❌ أهداف الدرس مفقودة!")
        else:
            print("  ℹ️  لا توجد أهداف في المرجع")
        
        # 2. فحص ميزة تسجيل الاسم والصف
        print("\n👤 ميزة تسجيل الاسم والصف:")
        if 'askStudent()' in main_content:
            print("  ✅ ميزة تسجيل الاسم موجودة")
            if 'swal-name' in main_content and 'swal-class' in main_content:
                print("  ✅ حقول الاسم والصف موجودة")
            else:
                print("  ⚠️  حقول الاسم والصف قد تكون ناقصة")
        else:
            print("  ❌ ميزة تسجيل الاسم مفقودة!")
        
        # 3. فحص المحتوى التعليمي
        print("\n📚 المحتوى التعليمي:")
        main_paragraphs = len(re.findall(r'<p[^>]*>', main_content))
        ref_paragraphs = len(re.findall(r'<p[^>]*>', ref_content))
        
        print(f"  📝 فقرات في الملف الرئيسي: {main_paragraphs}")
        print(f"  📝 فقرات في المرجع: {ref_paragraphs}")
        
        if main_paragraphs < ref_paragraphs * 0.7:  # إذا فقد أكثر من 30%
            print("  ❌ محتوى تعليمي كبير مفقود!")
        elif main_paragraphs < ref_paragraphs:
            print("  ⚠️  بعض المحتوى التعليمي مفقود")
        else:
            print("  ✅ المحتوى التعليمي سليم")
        
        # 4. فحص الصور والوسائط
        print("\n🖼️ الصور والوسائط:")
        main_images = len(re.findall(r'<img[^>]*>', main_content))
        ref_images = len(re.findall(r'<img[^>]*>', ref_content))
        
        print(f"  🖼️  صور في الملف الرئيسي: {main_images}")
        print(f"  🖼️  صور في المرجع: {ref_images}")
        
        if main_images < ref_images:
            print("  ❌ بعض الصور مفقودة!")
        else:
            print("  ✅ الصور سليمة")
        
        # 5. فحص الأنشطة التفاعلية
        print("\n🎮 الأنشطة التفاعلية:")
        interactive_elements = []
        
        if 'drag' in main_content or 'drop' in main_content:
            interactive_elements.append("سحب وإفلات")
        if 'animation' in main_content or 'gsap' in main_content:
            interactive_elements.append("رسوم متحركة")
        if 'canvas' in main_content:
            interactive_elements.append("رسم تفاعلي")
        if 'video' in main_content:
            interactive_elements.append("فيديو")
        
        if interactive_elements:
            print(f"  ✅ أنشطة تفاعلية: {', '.join(interactive_elements)}")
        else:
            print("  ⚠️  لا توجد أنشطة تفاعلية خاصة")
        
        # 6. فحص التنقل
        print("\n🧭 التنقل:")
        if 'السابق' in main_content and 'التالي' in main_content:
            print("  ✅ أزرار التنقل موجودة")
        else:
            print("  ❌ أزرار التنقل مفقودة!")
        
        # 7. فحص الملخص والخلاصة
        print("\n📋 الملخص والخلاصة:")
        if 'ملخص' in main_content or 'خلاصة' in main_content or 'تلخيص' in main_content:
            print("  ✅ قسم الملخص موجود")
        else:
            print("  ❌ قسم الملخص مفقود!")
        
        # 8. فحص المراجع والمصادر
        print("\n📖 المراجع والمصادر:")
        if 'مراجع' in main_content or 'مصادر' in main_content or 'المرجع' in main_content:
            print("  ✅ المراجع موجودة")
        else:
            print("  ⚠️  المراجع غير واضحة")
        
        # 9. فحص الأنظمة التقنية
        print("\n⚙️ الأنظمة التقنية:")
        systems = []
        if 'SoundSystem' in main_content:
            systems.append("النظام الصوتي")
        if 'Swal.fire' in main_content:
            systems.append("نظام الإشعارات")
        if 'updateProgress' in main_content:
            systems.append("شريط التقدم")
        if 'localStorage' in main_content:
            systems.append("حفظ البيانات")
        
        print(f"  ✅ الأنظمة الفعالة: {', '.join(systems)}")
        
        # 10. فحص الميزات المتقدمة من المرجع
        print("\n🌟 الميزات المتقدمة:")
        advanced_features = []
        
        # البحث في المرجع عن ميزات متقدمة
        if 'timeline' in ref_content and 'timeline' not in main_content:
            print("  ❌ الخط الزمني مفقود!")
        if 'calculator' in ref_content and 'calculator' not in main_content:
            print("  ❌ الحاسبة التفاعلية مفقودة!")
        if 'simulator' in ref_content and 'simulator' not in main_content:
            print("  ❌ المحاكي التفاعلي مفقود!")
        if 'diagram' in ref_content and 'diagram' not in main_content:
            print("  ❌ الرسوم التوضيحية التفاعلية مفقودة!")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في فحص {main_file}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔍 فحص شامل للأقسام المفقودة...")
    print("=" * 80)
    
    # قائمة الدروس للفحص
    lessons_to_check = [
        ("unit-1-cells/lesson-1-1/index.html", "Q/unit-1-cells/lesson-1-1/index.html"),
        ("unit-1-cells/lesson-1-2/index.html", "Q/unit-1-cells/lesson-1-2/index.html"),
        ("unit-2-transport/lesson-2-1/index.html", "Q/unit-2-transport/lesson-2-1/index.html"),
        ("unit-3-biomolecules/lesson-3-1/index.html", "Q/unit-3-biomolecules/lesson-3-1/index.html"),
        ("unit-6-homeostasis/lesson-6-4/index.html", "Q/unit-6-homeostasis/lesson-6-4/index.html")
    ]
    
    checked_count = 0
    
    for main_file, ref_file in lessons_to_check:
        if os.path.exists(main_file):
            if comprehensive_check(main_file, ref_file):
                checked_count += 1
        else:
            print(f"❌ الملف الرئيسي غير موجود: {main_file}")
    
    print("\n" + "=" * 80)
    print(f"🎉 انتهاء الفحص الشامل!")
    print(f"✅ تم فحص {checked_count} درس من أصل {len(lessons_to_check)}")
    print("\n🎯 الأقسام المفحوصة:")
    print("   🎯 أهداف الدرس")
    print("   👤 ميزة تسجيل الاسم والصف")
    print("   📚 المحتوى التعليمي")
    print("   🖼️ الصور والوسائط")
    print("   🎮 الأنشطة التفاعلية")
    print("   🧭 التنقل")
    print("   📋 الملخص والخلاصة")
    print("   📖 المراجع والمصادر")
    print("   ⚙️ الأنظمة التقنية")
    print("   🌟 الميزات المتقدمة")

if __name__ == "__main__":
    main()