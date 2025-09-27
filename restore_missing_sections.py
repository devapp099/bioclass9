#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
استعادة الأقسام المفقودة من المرجع الأصلي
"""

import os
import re

def restore_missing_sections(main_file, reference_file):
    """استعادة الأقسام المفقودة من المرجع"""
    try:
        # قراءة الملفات
        with open(main_file, 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        if not os.path.exists(reference_file):
            print(f"❌ الملف المرجعي غير موجود: {reference_file}")
            return False
        
        with open(reference_file, 'r', encoding='utf-8') as f:
            ref_content = f.read()
        
        print(f"🔧 استعادة الأقسام المفقودة في {main_file}")
        updated = False
        
        # 1. استعادة قسم أهداف الدرس
        if '🎯 أهداف الدرس' in ref_content and '🎯 أهداف الدرس' not in main_content:
            # استخراج قسم الأهداف من المرجع
            objectives_match = re.search(
                r'<!-- أهداف الدرس -->(.*?)<!-- الأسئلة',
                ref_content, re.DOTALL
            )
            
            if objectives_match:
                objectives_section = objectives_match.group(1).strip()
                
                # البحث عن مكان الإدراج (قبل قسم الأسئلة)
                insertion_point = '<section id="quiz"'
                if insertion_point in main_content:
                    main_content = main_content.replace(
                        insertion_point,
                        f'    <!-- أهداف الدرس -->\n{objectives_section}\n\n    {insertion_point}'
                    )
                    updated = True
                    print("  ✅ تم إضافة قسم أهداف الدرس")
        
        # 2. إضافة أزرار التنقل المفقودة
        if ('السابق' in ref_content or 'التالي' in ref_content) and 'السابق' not in main_content:
            # إضافة أزرار التنقل في footer
            navigation_buttons = '''
      <div style="display:flex; gap:12px; justify-content:space-between; margin-top:16px; flex-wrap:wrap">
        <button class="btn-ghost" onclick="history.back()">← السابق</button>
        <button class="btn-ghost" onclick="window.location.href='../lesson-1-2/index.html'">التالي →</button>
      </div>'''
            
            # إضافة قبل إغلاق footer
            footer_pattern = r'(<footer class="card"[^>]*>.*?)(</footer>)'
            if re.search(footer_pattern, main_content, re.DOTALL):
                main_content = re.sub(
                    footer_pattern,
                    r'\1' + navigation_buttons + '\n    \\2',
                    main_content, flags=re.DOTALL
                )
                updated = True
                print("  ✅ تم إضافة أزرار التنقل")
        
        # 3. إضافة قسم الملخص
        if 'ملخص' not in main_content:
            summary_section = '''
    <!-- ملخص الدرس -->
    <section class="card" style="margin-top:16px" data-aos="fade-up">
      <h2>📋 ملخص الدرس</h2>
      <div style="background:rgba(16,185,129,.1); padding:16px; border-radius:12px; border-left:4px solid #10b981">
        <p><strong>النقاط الرئيسية:</strong></p>
        <ul>
          <li>الخلايا النباتية تحتوي على: جدار خلوي، بلاستيدات خضراء، فجوة عصارية كبيرة</li>
          <li>الخلايا الحيوانية أصغر حجماً وأكثر مرونة في الشكل</li>
          <li>جميع الخلايا تشترك في: غشاء خلوي، سيتوبلازم، نواة</li>
        </ul>
      </div>
    </section>'''
            
            # إضافة قبل footer
            footer_position = main_content.find('<footer')
            if footer_position != -1:
                main_content = main_content[:footer_position] + summary_section + '\n\n    ' + main_content[footer_position:]
                updated = True
                print("  ✅ تم إضافة قسم الملخص")
        
        # 4. تحديث الرابط إلى المراجع
        if 'devapp099.github.io' not in main_content:
            # إضافة رابط المراجع في footer
            reference_link = '''
      <div style="margin-top:12px; padding-top:12px; border-top:1px solid rgba(0,0,0,.1)">
        <p><strong>📖 المراجع:</strong> <a href="https://devapp099.github.io/bioclass9" target="_blank" style="color:#10b981">المشروع الأصلي</a></p>
      </div>'''
            
            # إضافة في footer قبل الإغلاق
            footer_end = '</footer>'
            if footer_end in main_content:
                main_content = main_content.replace(
                    footer_end,
                    reference_link + '\n    ' + footer_end
                )
                updated = True
                print("  ✅ تم إضافة رابط المراجع")
        
        # 5. تحديث عنوان الصفحة ليطابق المرجع
        ref_title_match = re.search(r'<title>(.*?)</title>', ref_content)
        main_title_match = re.search(r'<title>(.*?)</title>', main_content)
        
        if ref_title_match and main_title_match:
            ref_title = ref_title_match.group(1)
            main_title = main_title_match.group(1)
            
            if ref_title != main_title:
                main_content = main_content.replace(
                    f'<title>{main_title}</title>',
                    f'<title>{ref_title}</title>'
                )
                updated = True
                print(f"  ✅ تم تحديث العنوان: {ref_title}")
        
        # حفظ الملف إذا تم التحديث
        if updated:
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(main_content)
            return True
        else:
            print(f"  ℹ️  لا يحتاج تحديث: {main_file}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في معالجة {main_file}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔄 استعادة الأقسام المفقودة...")
    print("=" * 60)
    
    # قائمة الدروس للإصلاح
    lessons_to_fix = [
        ("unit-1-cells/lesson-1-1/index.html", "Q/unit-1-cells/lesson-1-1/index.html"),
        ("unit-1-cells/lesson-1-2/index.html", "Q/unit-1-cells/lesson-1-2/index.html"),
        ("unit-1-cells/lesson-1-3/index.html", "Q/unit-1-cells/lesson-1-3/index.html"),
        ("unit-2-transport/lesson-2-1/index.html", "Q/unit-2-transport/lesson-2-1/index.html"),
        ("unit-2-transport/lesson-2-2/index.html", "Q/unit-2-transport/lesson-2-2/index.html"),
        ("unit-2-transport/lesson-2-3/index.html", "Q/unit-2-transport/lesson-2-3/index.html"),
        ("unit-3-biomolecules/lesson-3-1/index.html", "Q/unit-3-biomolecules/lesson-3-1/index.html"),
        ("unit-3-biomolecules/lesson-3-2/index.html", "Q/unit-3-biomolecules/lesson-3-2/index.html"),
        ("unit-3-biomolecules/lesson-3-3/index.html", "Q/unit-3-biomolecules/lesson-3-3/index.html"),
        ("unit-4-nutrition/lesson-4-1/index.html", "Q/unit-4-nutrition/lesson-4-1/index.html"),
        ("unit-4-nutrition/lesson-4-2/index.html", "Q/unit-4-nutrition/lesson-4-2/index.html"),
        ("unit-5-respiration/lesson-5-1/index.html", "Q/unit-5-respiration/lesson-5-1/index.html"),
        ("unit-6-homeostasis/lesson-6-1/index.html", "Q/unit-6-homeostasis/lesson-6-1/index.html"),
        ("unit-6-homeostasis/lesson-6-2/index.html", "Q/unit-6-homeostasis/lesson-6-2/index.html"),
        ("unit-6-homeostasis/lesson-6-3/index.html", "Q/unit-6-homeostasis/lesson-6-3/index.html"),
        ("unit-6-homeostasis/lesson-6-4/index.html", "Q/unit-6-homeostasis/lesson-6-4/index.html")
    ]
    
    fixed_count = 0
    
    for main_file, ref_file in lessons_to_fix:
        if os.path.exists(main_file):
            if restore_missing_sections(main_file, ref_file):
                fixed_count += 1
        else:
            print(f"❌ الملف الرئيسي غير موجود: {main_file}")
    
    print("\n" + "=" * 60)
    print(f"🎉 انتهاء العملية!")
    print(f"✅ تم إصلاح {fixed_count} درس من أصل {len(lessons_to_fix)}")
    print("🔄 الأقسام المستعادة:")
    print("   🎯 أهداف الدرس")
    print("   🧭 أزرار التنقل (السابق/التالي)")
    print("   📋 قسم الملخص")
    print("   📖 رابط المراجع")
    print("   🏷️  عناوين الصفحات")

if __name__ == "__main__":
    main()