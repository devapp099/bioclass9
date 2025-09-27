#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
حفظ المحتوى المتخصص من مجلد Q كنسخة احتياطية
Save specialized content from Q folder as backup
"""

import os
import re
import json

def extract_and_save_all_content():
    """استخراج وحفظ جميع المحتوى المتخصص"""
    
    print("💾 حفظ المحتوى المتخصص كنسخة احتياطية...")
    print("=" * 60)
    
    # تعريف جميع الدروس
    lessons_mapping = [
        ("unit-1-cells/lesson-1-1", "Q/unit-1-cells/lesson-1-1/index.html", "الخلايا الحيوانية والنباتية"),
        ("unit-1-cells/lesson-1-2", "Q/unit-1-cells/lesson-1-2/index.html", "المجهر والقياسات المجهرية"),
        ("unit-1-cells/lesson-1-3", "Q/unit-1-cells/lesson-1-3/index.html", "العُضيّات ووظائفها"),
        ("unit-2-transport/lesson-2-1", "Q/unit-2-transport/lesson-2-1/index.html", "الانتشار"),
        ("unit-2-transport/lesson-2-2", "Q/unit-2-transport/lesson-2-2/index.html", "كيف تحصل النباتات على الماء؟"),
        ("unit-2-transport/lesson-2-3", "Q/unit-2-transport/lesson-2-3/index.html", "الأسموزية والبطاطس"),
        ("unit-3-biomolecules/lesson-3-1", "Q/unit-3-biomolecules/lesson-3-1/index.html", "الكربوهيدرات"),
        ("unit-3-biomolecules/lesson-3-2", "Q/unit-3-biomolecules/lesson-3-2/index.html", "اختبار الفرضية (البروتين)"),
        ("unit-3-biomolecules/lesson-3-3", "Q/unit-3-biomolecules/lesson-3-3/index.html", "أسئلة حول الإنزيمات"),
        ("unit-4-nutrition/lesson-4-1", "Q/unit-4-nutrition/lesson-4-1/index.html", "النظام الغذائي"),
        ("unit-4-nutrition/lesson-4-2", "Q/unit-4-nutrition/lesson-4-2/index.html", "امتصاص فيتامين د"),
        ("unit-5-respiration/lesson-5-1", "Q/unit-5-respiration/lesson-5-1/index.html", "تأثير الحرارة على معدل التنفس"),
        ("unit-6-homeostasis/lesson-6-1", "Q/unit-6-homeostasis/lesson-6-1/index.html", "الكافيين وزمن الاستجابة"),
        ("unit-6-homeostasis/lesson-6-2", "Q/unit-6-homeostasis/lesson-6-2/index.html", "تكيّف العين"),
        ("unit-6-homeostasis/lesson-6-3", "Q/unit-6-homeostasis/lesson-6-3/index.html", "ثابتة ومتغيرة الحرارة"),
        ("unit-6-homeostasis/lesson-6-4", "Q/unit-6-homeostasis/lesson-6-4/index.html", "مرض السكري")
    ]
    
    specialized_content = {}
    
    for lesson_id, q_file, lesson_title in lessons_mapping:
        print(f"🔄 استخراج: {lesson_title}")
        
        if not os.path.exists(q_file):
            print(f"  ❌ الملف غير موجود: {q_file}")
            continue
        
        try:
            with open(q_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lesson_data = {
                'title': lesson_title,
                'questions': [],
                'objectives': None
            }
            
            # استخراج الأسئلة
            bank_match = re.search(r'const bank\s*=\s*\[(.*?)\];', content, re.DOTALL)
            if bank_match:
                questions_text = bank_match.group(1)
                questions = re.findall(r'\{q:"([^"]+)",\s*c:\[([^\]]+)\],\s*a:(\d+)\}', questions_text)
                
                for q_text, choices_text, answer_index in questions:
                    choices = re.findall(r'"([^"]+)"', choices_text)
                    lesson_data['questions'].append({
                        'question': q_text,
                        'choices': choices,
                        'answer': int(answer_index)
                    })
            
            # استخراج الأهداف
            objectives_section = re.search(r'<h1>🎯 أهداف الدرس</h1>\s*<p class="lead">([^<]+)</p>\s*<ul>(.*?)</ul>', content, re.DOTALL)
            if objectives_section:
                description = objectives_section.group(1).strip()
                objectives_html = objectives_section.group(2)
                objectives = re.findall(r'<li>([^<]+(?:<[^>]*>[^<]*</[^>]*>[^<]*)*)</li>', objectives_html)
                
                lesson_data['objectives'] = {
                    'description': description,
                    'objectives': [obj.strip() for obj in objectives if obj.strip()]
                }
            
            specialized_content[lesson_id] = lesson_data
            print(f"  ✅ {len(lesson_data['questions'])} سؤال، {len(lesson_data['objectives']['objectives']) if lesson_data['objectives'] else 0} هدف")
            
        except Exception as e:
            print(f"  ❌ خطأ: {e}")
    
    # حفظ البيانات في ملف JSON
    try:
        with open('specialized_content_backup.json', 'w', encoding='utf-8') as f:
            json.dump(specialized_content, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ تم حفظ المحتوى في: specialized_content_backup.json")
        
        # إحصائيات
        total_questions = sum(len(data['questions']) for data in specialized_content.values())
        total_objectives = sum(len(data['objectives']['objectives']) if data['objectives'] else 0 for data in specialized_content.values())
        
        print(f"📊 الإحصائيات:")
        print(f"   📚 {len(specialized_content)} درس")
        print(f"   📝 {total_questions} سؤال متخصص")
        print(f"   🎯 {total_objectives} هدف تعليمي")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الحفظ: {e}")
        return False

def load_and_apply_specialized_content():
    """تحميل وتطبيق المحتوى المتخصص من الملف الاحتياطي"""
    
    if not os.path.exists('specialized_content_backup.json'):
        print("❌ ملف النسخة الاحتياطية غير موجود!")
        return False
    
    print("🔄 تطبيق المحتوى المتخصص من النسخة الاحتياطية...")
    print("=" * 60)
    
    try:
        with open('specialized_content_backup.json', 'r', encoding='utf-8') as f:
            specialized_content = json.load(f)
        
        successful_updates = 0
        
        for lesson_id, lesson_data in specialized_content.items():
            main_file = f"{lesson_id}/index.html"
            
            if not os.path.exists(main_file):
                print(f"❌ الملف الرئيسي غير موجود: {main_file}")
                continue
            
            print(f"🔄 تحديث: {lesson_data['title']}")
            
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            updated = False
            
            # تحديث الأسئلة
            if lesson_data['questions']:
                js_questions = []
                for q in lesson_data['questions']:
                    choices_str = ', '.join(f'"{choice}"' for choice in q['choices'])
                    js_question = f'{{q:"{q["question"]}", c:[{choices_str}], a:{q["answer"]}}}'
                    js_questions.append(js_question)
                
                new_bank = "[\n      " + ",\n      ".join(js_questions) + "\n    ]"
                
                bank_pattern = r'const bank\s*=\s*\[.*?\];'
                if re.search(bank_pattern, content, re.DOTALL):
                    content = re.sub(bank_pattern, f'const bank = {new_bank};', content, flags=re.DOTALL)
                    updated = True
                    print(f"  ✅ تم تحديث {len(lesson_data['questions'])} سؤال")
            
            # تحديث الأهداف
            if lesson_data['objectives']:
                objectives_pattern = r'(<h1>🎯 أهداف الدرس</h1>\s*<p class="lead">)[^<]+(</p>\s*<ul>).*?(</ul>)'
                
                if re.search(objectives_pattern, content, re.DOTALL):
                    objectives_html = '\n        '.join(f'<li>{obj}</li>' for obj in lesson_data['objectives']['objectives'])
                    new_objectives_section = f'\\1{lesson_data["objectives"]["description"]}\\2\n        {objectives_html}\n      \\3'
                    
                    content = re.sub(objectives_pattern, new_objectives_section, content, flags=re.DOTALL)
                    updated = True
                    print(f"  ✅ تم تحديث {len(lesson_data['objectives']['objectives'])} هدف")
            
            if updated:
                with open(main_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                successful_updates += 1
        
        print(f"\n🎉 تم تحديث {successful_updates} درس بنجاح!")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في التطبيق: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--apply':
        # تطبيق المحتوى من النسخة الاحتياطية
        load_and_apply_specialized_content()
    else:
        # استخراج وحفظ المحتوى
        extract_and_save_all_content()
        
        print("\n💡 كيفية الاستخدام:")
        print("1. شغل هذا السكريبت لحفظ النسخة الاحتياطية")
        print("2. قم بتحديث المشروع بالنسخة التي تعمل")
        print("3. شغل: python backup_specialized_content.py --apply")
        print("   لتطبيق المحتوى المتخصص على النسخة الجديدة")

if __name__ == "__main__":
    main()