#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نسخ الأسئلة المتخصصة من مجلد Q إلى الدروس الرئيسية
Copy specialized questions from Q folder to main lessons
"""

import os
import re

def extract_questions_from_q_folder(q_file_path):
    """استخراج الأسئلة من ملف في مجلد Q"""
    try:
        with open(q_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # البحث عن الأسئلة بالنمط الجديد (HTML format)
        html_questions = []
        question_pattern = r'<article class="q" data-qid="([^"]+)">(.*?)</article>'
        question_matches = re.findall(question_pattern, content, re.DOTALL)
        
        if question_matches:
            for qid, q_content in question_matches:
                # استخراج نص السؤال
                question_text_match = re.search(r'<div><strong>[^)]*\)\s*([^<]+)</strong></div>', q_content)
                question_text = question_text_match.group(1).strip() if question_text_match else ""
                
                # استخراج الخيارات
                choices = []
                correct_answer_idx = -1
                choice_pattern = r'<div class="choice" data-correct="([^"]+)">([^<]+)</div>'
                choice_matches = re.findall(choice_pattern, q_content)
                
                for i, (is_correct, choice_text) in enumerate(choice_matches):
                    choices.append(choice_text.strip())
                    if is_correct == "true":
                        correct_answer_idx = i
                
                if question_text and choices and correct_answer_idx >= 0:
                    html_questions.append({
                        'q': question_text,
                        'c': choices,
                        'a': correct_answer_idx
                    })
        
        # إذا لم نجد أسئلة بالنمط HTML، ابحث عن النمط الجافا سكريبت
        if not html_questions:
            js_pattern = r'\{\s*q:\s*["\']([^"\']+)["\']\s*,\s*c:\s*\[(.*?)\]\s*,\s*a:\s*(\d+)\s*\}'
            js_matches = re.findall(js_pattern, content, re.DOTALL)
            
            for question, choices_str, answer_idx in js_matches:
                choices_pattern = r'["\']([^"\']+)["\']'
                choices = re.findall(choices_pattern, choices_str)
                
                html_questions.append({
                    'q': question.strip(),
                    'c': [choice.strip() for choice in choices],
                    'a': int(answer_idx)
                })
        
        return html_questions
        
    except Exception as e:
        print(f"❌ خطأ في قراءة {q_file_path}: {e}")
        return []

def update_lesson_questions(lesson_path, new_questions):
    """تحديث الأسئلة في درس محدد"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not new_questions:
            print(f"⚠️ لا توجد أسئلة جديدة لـ {lesson_path}")
            return False
        
        # تحويل الأسئلة إلى تنسيق JavaScript
        js_questions = []
        for q in new_questions:
            choices_str = ', '.join([f'"{choice}"' for choice in q['c']])
            js_questions.append(f'      {{q:"{q["q"]}", c:[{choices_str}], a:{q["a"]}}}')
        
        questions_block = ',\n'.join(js_questions)
        
        # البحث عن مصفوفة الأسئلة الحالية واستبدالها
        current_questions_pattern = r'(\s*)(//.*أسئلة.*\n)?\s*(\[[\s\S]*?\];)'
        
        # البحث عن النمط الأكثر تحديداً
        questions_array_pattern = r'(\s*\[[\s\S]*?\{[\s\S]*?q:[\s\S]*?\}[\s\S]*?\];)'
        
        replacement = f'    [\n{questions_block}\n    ];'
        
        if re.search(questions_array_pattern, content):
            content = re.sub(questions_array_pattern, replacement, content, count=1)
            print(f"✅ تم استبدال الأسئلة في {lesson_path}")
        else:
            print(f"⚠️ لم يتم العثور على مصفوفة الأسئلة في {lesson_path}")
            return False
        
        # حفظ الملف المحدث
        with open(lesson_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تحديث {lesson_path}: {e}")
        return False

def copy_specialized_questions():
    """نسخ الأسئلة المتخصصة من مجلد Q"""
    
    print("📚 بدء نسخ الأسئلة المتخصصة من مجلد Q...")
    print("=" * 70)
    
    # قائمة الدروس مع مساراتها
    lessons_mapping = [
        ("Q/unit-1-cells/lesson-1-1/index.html", "unit-1-cells/lesson-1-1/index.html", "🔬 درس 1-1"),
        ("Q/unit-1-cells/lesson-1-2/index.html", "unit-1-cells/lesson-1-2/index.html", "🧪 درس 1-2"),
        ("Q/unit-1-cells/lesson-1-3/index.html", "unit-1-cells/lesson-1-3/index.html", "🔍 درس 1-3"),
        ("Q/unit-2-transport/lesson-2-1/index.html", "unit-2-transport/lesson-2-1/index.html", "🚛 درس 2-1"),
        ("Q/unit-2-transport/lesson-2-2/index.html", "unit-2-transport/lesson-2-2/index.html", "💧 درس 2-2"),
        ("Q/unit-2-transport/lesson-2-3/index.html", "unit-2-transport/lesson-2-3/index.html", "⚡ درس 2-3"),
        ("Q/unit-3-biomolecules/lesson-3-1/index.html", "unit-3-biomolecules/lesson-3-1/index.html", "🧬 درس 3-1"),
        ("Q/unit-3-biomolecules/lesson-3-2/index.html", "unit-3-biomolecules/lesson-3-2/index.html", "🧪 درس 3-2"),
        ("Q/unit-3-biomolecules/lesson-3-3/index.html", "unit-3-biomolecules/lesson-3-3/index.html", "⚗️ درس 3-3"),
        ("Q/unit-4-nutrition/lesson-4-1/index.html", "unit-4-nutrition/lesson-4-1/index.html", "🍎 درس 4-1"),
        ("Q/unit-4-nutrition/lesson-4-2/index.html", "unit-4-nutrition/lesson-4-2/index.html", "🔄 درس 4-2"),
        ("Q/unit-5-respiration/lesson-5-1/index.html", "unit-5-respiration/lesson-5-1/index.html", "💨 درس 5-1"),
        ("Q/unit-6-homeostasis/lesson-6-1/index.html", "unit-6-homeostasis/lesson-6-1/index.html", "⚖️ درس 6-1"),
        ("Q/unit-6-homeostasis/lesson-6-2/index.html", "unit-6-homeostasis/lesson-6-2/index.html", "🌡️ درس 6-2"),
        ("Q/unit-6-homeostasis/lesson-6-3/index.html", "unit-6-homeostasis/lesson-6-3/index.html", "🍬 درس 6-3"),
        ("Q/unit-6-homeostasis/lesson-6-4/index.html", "unit-6-homeostasis/lesson-6-4/index.html", "🧠 درس 6-4")
    ]
    
    updated_count = 0
    total_questions = 0
    
    for q_path, main_path, lesson_name in lessons_mapping:
        if os.path.exists(q_path) and os.path.exists(main_path):
            print(f"🔄 معالجة: {lesson_name}")
            
            # استخراج الأسئلة من مجلد Q
            questions = extract_questions_from_q_folder(q_path)
            
            if questions:
                print(f"📖 تم استخراج {len(questions)} سؤال من {q_path}")
                
                # تحديث الدرس الرئيسي
                if update_lesson_questions(main_path, questions):
                    updated_count += 1
                    total_questions += len(questions)
                    print(f"✅ تم تحديث {lesson_name} بـ {len(questions)} سؤال متخصص")
                else:
                    print(f"❌ فشل تحديث {lesson_name}")
            else:
                print(f"⚠️ لم يتم العثور على أسئلة في {q_path}")
        else:
            if not os.path.exists(q_path):
                print(f"❌ ملف Q غير موجود: {q_path}")
            if not os.path.exists(main_path):
                print(f"❌ الدرس الرئيسي غير موجود: {main_path}")
        
        print("-" * 50)
    
    print("\n" + "=" * 70)
    print("🎉 انتهاء عملية نسخ الأسئلة المتخصصة!")
    print(f"✅ تم تحديث {updated_count} درس من أصل {len(lessons_mapping)}")
    print(f"📊 إجمالي الأسئلة المنسوخة: {total_questions}")
    
    if updated_count == len(lessons_mapping):
        print("🌟 جميع الدروس تحتوي الآن على أسئلة متخصصة فريدة!")
    else:
        print(f"⚠️ {len(lessons_mapping) - updated_count} دروس تحتاج مراجعة")

def main():
    """الدالة الرئيسية"""
    copy_specialized_questions()

if __name__ == "__main__":
    main()