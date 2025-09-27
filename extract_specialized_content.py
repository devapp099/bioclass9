#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
استخراج الأسئلة والأهداف المتخصصة من مجلد Q وترتيبها في المشروع الأصلي
Extract specialized questions and objectives from Q folder and organize them in the main project
"""

import os
import re
import json

def extract_questions_from_q_folder(q_file_path):
    """استخراج الأسئلة من ملف في مجلد Q"""
    try:
        if not os.path.exists(q_file_path):
            return []
        
        with open(q_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # البحث عن bank الأسئلة
        bank_match = re.search(r'const bank\s*=\s*\[(.*?)\];', content, re.DOTALL)
        if not bank_match:
            return []
        
        # استخراج الأسئلة الفردية
        questions_text = bank_match.group(1)
        questions = re.findall(r'\{q:"([^"]+)",\s*c:\[([^\]]+)\],\s*a:(\d+)\}', questions_text)
        
        formatted_questions = []
        for q_text, choices_text, answer_index in questions:
            # استخراج الخيارات
            choices = re.findall(r'"([^"]+)"', choices_text)
            
            formatted_questions.append({
                'question': q_text,
                'choices': choices,
                'answer': int(answer_index)
            })
        
        return formatted_questions
        
    except Exception as e:
        print(f"❌ خطأ في استخراج الأسئلة من {q_file_path}: {e}")
        return []

def extract_objectives_from_q_folder(q_file_path):
    """استخراج الأهداف من ملف في مجلد Q"""
    try:
        if not os.path.exists(q_file_path):
            return None
        
        with open(q_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # البحث عن قسم الأهداف
        objectives_section = re.search(r'<h1>🎯 أهداف الدرس</h1>\s*<p class="lead">([^<]+)</p>\s*<ul>(.*?)</ul>', content, re.DOTALL)
        
        if not objectives_section:
            return None
        
        description = objectives_section.group(1).strip()
        objectives_html = objectives_section.group(2)
        
        # استخراج الأهداف الفردية
        objectives = re.findall(r'<li>([^<]+(?:<[^>]*>[^<]*</[^>]*>[^<]*)*)</li>', objectives_html)
        
        return {
            'description': description,
            'objectives': [obj.strip() for obj in objectives if obj.strip()]
        }
        
    except Exception as e:
        print(f"❌ خطأ في استخراج الأهداف من {q_file_path}: {e}")
        return None

def format_questions_for_js(questions):
    """تنسيق الأسئلة لكود JavaScript"""
    if not questions:
        return "[]"
    
    js_questions = []
    for q in questions:
        choices_str = ', '.join(f'"{choice}"' for choice in q['choices'])
        js_question = f'{{q:"{q["question"]}", c:[{choices_str}], a:{q["answer"]}}}'
        js_questions.append(js_question)
    
    return "[\n      " + ",\n      ".join(js_questions) + "\n    ]"

def update_lesson_with_specialized_content(main_lesson_file, questions, objectives):
    """تحديث ملف الدرس بالمحتوى المتخصص"""
    try:
        if not os.path.exists(main_lesson_file):
            print(f"❌ الملف الرئيسي غير موجود: {main_lesson_file}")
            return False
        
        with open(main_lesson_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = False
        
        # 1. تحديث الأسئلة
        if questions:
            new_bank = format_questions_for_js(questions)
            
            # البحث عن bank الحالي واستبداله
            bank_pattern = r'const bank\s*=\s*\[.*?\];'
            if re.search(bank_pattern, content, re.DOTALL):
                content = re.sub(bank_pattern, f'const bank = {new_bank};', content, flags=re.DOTALL)
                updated = True
                print(f"  ✅ تم تحديث {len(questions)} سؤال")
            else:
                print(f"  ⚠️ لم يتم العثور على bank في {main_lesson_file}")
        
        # 2. تحديث الأهداف
        if objectives:
            # البحث عن قسم الأهداف الحالي
            objectives_pattern = r'(<h1>🎯 أهداف الدرس</h1>\s*<p class="lead">)[^<]+(</p>\s*<ul>).*?(</ul>)'
            
            if re.search(objectives_pattern, content, re.DOTALL):
                # إنشاء HTML للأهداف الجديدة
                objectives_html = '\n        '.join(f'<li>{obj}</li>' for obj in objectives['objectives'])
                
                new_objectives_section = f'\\1{objectives["description"]}\\2\n        {objectives_html}\n      \\3'
                
                content = re.sub(objectives_pattern, new_objectives_section, content, flags=re.DOTALL)
                updated = True
                print(f"  ✅ تم تحديث {len(objectives['objectives'])} هدف")
            else:
                print(f"  ⚠️ لم يتم العثور على قسم الأهداف في {main_lesson_file}")
        
        # حفظ الملف إذا تم التحديث
        if updated:
            with open(main_lesson_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            print(f"  ℹ️ لا يحتاج تحديث: {main_lesson_file}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في تحديث {main_lesson_file}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("📚 استخراج المحتوى المتخصص من مجلد Q...")
    print("=" * 70)
    
    # تعريف جميع الدروس
    lessons_mapping = [
        ("unit-1-cells/lesson-1-1/index.html", "Q/unit-1-cells/lesson-1-1/index.html", "🔬 درس 1-1"),
        ("unit-1-cells/lesson-1-2/index.html", "Q/unit-1-cells/lesson-1-2/index.html", "🧪 درس 1-2"),
        ("unit-1-cells/lesson-1-3/index.html", "Q/unit-1-cells/lesson-1-3/index.html", "🔍 درس 1-3"),
        ("unit-2-transport/lesson-2-1/index.html", "Q/unit-2-transport/lesson-2-1/index.html", "🚛 درس 2-1"),
        ("unit-2-transport/lesson-2-2/index.html", "Q/unit-2-transport/lesson-2-2/index.html", "💧 درس 2-2"),
        ("unit-2-transport/lesson-2-3/index.html", "Q/unit-2-transport/lesson-2-3/index.html", "⚡ درس 2-3"),
        ("unit-3-biomolecules/lesson-3-1/index.html", "Q/unit-3-biomolecules/lesson-3-1/index.html", "🧬 درس 3-1"),
        ("unit-3-biomolecules/lesson-3-2/index.html", "Q/unit-3-biomolecules/lesson-3-2/index.html", "🧪 درس 3-2"),
        ("unit-3-biomolecules/lesson-3-3/index.html", "Q/unit-3-biomolecules/lesson-3-3/index.html", "⚗️ درس 3-3"),
        ("unit-4-nutrition/lesson-4-1/index.html", "Q/unit-4-nutrition/lesson-4-1/index.html", "🍎 درس 4-1"),
        ("unit-4-nutrition/lesson-4-2/index.html", "Q/unit-4-nutrition/lesson-4-2/index.html", "🔄 درس 4-2"),
        ("unit-5-respiration/lesson-5-1/index.html", "Q/unit-5-respiration/lesson-5-1/index.html", "💨 درس 5-1"),
        ("unit-6-homeostasis/lesson-6-1/index.html", "Q/unit-6-homeostasis/lesson-6-1/index.html", "⚖️ درس 6-1"),
        ("unit-6-homeostasis/lesson-6-2/index.html", "Q/unit-6-homeostasis/lesson-6-2/index.html", "🌡️ درس 6-2"),
        ("unit-6-homeostasis/lesson-6-3/index.html", "Q/unit-6-homeostasis/lesson-6-3/index.html", "🍬 درس 6-3"),
        ("unit-6-homeostasis/lesson-6-4/index.html", "Q/unit-6-homeostasis/lesson-6-4/index.html", "🧠 درس 6-4")
    ]
    
    successful_updates = 0
    total_questions = 0
    total_objectives = 0
    
    for main_file, q_file, lesson_name in lessons_mapping:
        print(f"\n🔄 معالجة: {lesson_name}")
        print("-" * 50)
        
        # استخراج الأسئلة من مجلد Q
        questions = extract_questions_from_q_folder(q_file)
        print(f"📝 تم استخراج {len(questions)} سؤال من {q_file}")
        
        # استخراج الأهداف من مجلد Q
        objectives = extract_objectives_from_q_folder(q_file)
        if objectives:
            print(f"🎯 تم استخراج {len(objectives['objectives'])} هدف من {q_file}")
        else:
            print(f"⚠️ لم يتم العثور على أهداف في {q_file}")
        
        # تحديث الملف الرئيسي
        if questions or objectives:
            if update_lesson_with_specialized_content(main_file, questions, objectives):
                successful_updates += 1
                total_questions += len(questions) if questions else 0
                total_objectives += len(objectives['objectives']) if objectives else 0
        
        print(f"✅ تم تحديث {lesson_name} بنجاح")
    
    print("\n" + "=" * 70)
    print("🎉 انتهاء عملية الاستخراج والترتيب!")
    print(f"✅ تم تحديث {successful_updates} درس من أصل {len(lessons_mapping)}")
    print(f"📝 إجمالي الأسئلة المستخرجة: {total_questions}")
    print(f"🎯 إجمالي الأهداف المستخرجة: {total_objectives}")
    
    print("\n🎯 ما تم إنجازه:")
    print("   📚 استخراج المحتوى المتخصص من مجلد Q")
    print("   🔄 ترتيب الأسئلة والأهداف حسب كل درس")
    print("   ✨ الحفاظ على التخصص والتنوع")
    print("   🎨 تنسيق صحيح للكود JavaScript")
    
    print("\n💡 الخطوة التالية:")
    print("بعد أن تقوم بتحديث المشروع بالنسخة الاحتياطية،")
    print("شغل هذا السكريبت لاستعادة المحتوى المتخصص!")

if __name__ == "__main__":
    main()