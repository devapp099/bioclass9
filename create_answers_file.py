#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
استخراج الأسئلة والإجابات من جميع الدروس وإنشاء ملف نصي
Extract questions and answers from all lessons and create text file
"""

import os
import re

def extract_questions_from_lesson(file_path):
    """استخراج الأسئلة والإجابات من درس واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # استخراج عنوان الدرس
        title_match = re.search(r'<title>([^<]+)</title>', content)
        lesson_title = title_match.group(1) if title_match else "درس غير محدد"
        
        # استخراج الأسئلة من JavaScript
        questions = []
        
        # البحث عن الأسئلة في JavaScript - النمط الجديد
        # البحث عن بنية {q:"...", c:[...], a:n}
        question_pattern = r'\{\s*q:\s*["\']([^"\']+)["\']\s*,\s*c:\s*\[(.*?)\]\s*,\s*a:\s*(\d+)\s*\}'
        question_matches = re.findall(question_pattern, content, re.DOTALL)
        
        if question_matches:
            for i, (question, choices_str, answer_idx) in enumerate(question_matches, 1):
                # تحليل الخيارات
                choices_pattern = r'["\']([^"\']+)["\']'
                choices = re.findall(choices_pattern, choices_str)
                
                # الحصول على الإجابة الصحيحة
                answer_idx = int(answer_idx)
                correct_answer = choices[answer_idx] if answer_idx < len(choices) else "غير محدد"
                
                questions.append({
                    'number': i,
                    'question': question.strip(),
                    'choices': [choice.strip() for choice in choices],
                    'correct_answer': correct_answer.strip(),
                    'answer_index': answer_idx
                })
        
        return lesson_title, questions
        
    except Exception as e:
        print(f"❌ خطأ في استخراج الأسئلة من {file_path}: {e}")
        return None, []

def create_answers_file():
    """إنشاء ملف الأسئلة والإجابات"""
    
    print("📚 بدء استخراج الأسئلة والإجابات من جميع الدروس...")
    
    # قائمة الدروس
    lessons = [
        ("unit-1-cells/lesson-1-1/index.html", "🔬 درس 1-1 — مقدمة في الخلايا"),
        ("unit-1-cells/lesson-1-2/index.html", "🧪 درس 1-2 — رسم الخلايا وحساب التكبير"),
        ("unit-1-cells/lesson-1-3/index.html", "🔍 درس 1-3 — أجزاء الخلية ووظائفها"),
        ("unit-2-transport/lesson-2-1/index.html", "🚛 درس 2-1 — النقل عبر الأغشية"),
        ("unit-2-transport/lesson-2-2/index.html", "💧 درس 2-2 — الانتشار والخاصية الأسموزية"),
        ("unit-2-transport/lesson-2-3/index.html", "⚡ درس 2-3 — النقل النشط والسلبي"),
        ("unit-3-biomolecules/lesson-3-1/index.html", "🧬 درس 3-1 — الكربوهيدرات والدهون"),
        ("unit-3-biomolecules/lesson-3-2/index.html", "🧪 درس 3-2 — البروتينات والأحماض النووية"),
        ("unit-3-biomolecules/lesson-3-3/index.html", "⚗️ درس 3-3 — الإنزيمات وآلية عملها"),
        ("unit-4-nutrition/lesson-4-1/index.html", "🍎 درس 4-1 — التغذية والهضم"),
        ("unit-4-nutrition/lesson-4-2/index.html", "🔄 درس 4-2 — الامتصاص والنقل"),
        ("unit-5-respiration/lesson-5-1/index.html", "💨 درس 5-1 — التنفس الخلوي"),
        ("unit-6-homeostasis/lesson-6-1/index.html", "⚖️ درس 6-1 — التوازن المائي"),
        ("unit-6-homeostasis/lesson-6-2/index.html", "🌡️ درس 6-2 — تنظيم درجة الحرارة"),
        ("unit-6-homeostasis/lesson-6-3/index.html", "🍬 درس 6-3 — تنظيم السكر في الدم"),
        ("unit-6-homeostasis/lesson-6-4/index.html", "🧠 درس 6-4 — الجهاز العصبي والتوازن")
    ]
    
    # محتوى الملف النصي
    output_content = []
    output_content.append("=" * 80)
    output_content.append("📚 ملف الأسئلة والإجابات - مادة الأحياء للصف التاسع")
    output_content.append("=" * 80)
    output_content.append("")
    output_content.append("🎨 تصميم: الوتين الضامرية | لمار السيابية | مها المعمرية")
    output_content.append("         مريم محمود البلوشية | مريم وائل البلوشية | مريم زكي العويسية")
    output_content.append("🏫 مدرسة عاتكة بنت زيد")
    output_content.append("👩‍🏫 تحت إشراف الأستاذة وفاء")
    output_content.append("")
    output_content.append("=" * 80)
    output_content.append("")
    
    total_questions = 0
    
    for lesson_path, lesson_title in lessons:
        if os.path.exists(lesson_path):
            print(f"🔄 معالجة: {lesson_title}")
            
            title, questions = extract_questions_from_lesson(lesson_path)
            
            if questions:
                output_content.append(f"\n{lesson_title}")
                output_content.append("-" * len(lesson_title))
                output_content.append("")
                
                for q in questions:
                    output_content.append(f"السؤال {q['number']}: {q['question']}")
                    output_content.append("")
                    
                    for i, choice in enumerate(q['choices']):
                        marker = "✅" if i == q['answer_index'] else "  "
                        output_content.append(f"{marker} {chr(65+i)}) {choice}")
                    
                    output_content.append("")
                    output_content.append(f"الإجابة الصحيحة: {chr(65+q['answer_index'])}) {q['correct_answer']}")
                    output_content.append("")
                    output_content.append("-" * 40)
                    output_content.append("")
                
                total_questions += len(questions)
                print(f"✅ تم استخراج {len(questions)} سؤال")
            else:
                print(f"⚠️ لم يتم العثور على أسئلة في {lesson_title}")
        else:
            print(f"❌ الملف غير موجود: {lesson_path}")
    
    # إضافة الإحصائيات
    output_content.append("=" * 80)
    output_content.append("📊 إحصائيات المحتوى")
    output_content.append("=" * 80)
    output_content.append(f"📚 عدد الدروس: {len(lessons)}")
    output_content.append(f"❓ إجمالي الأسئلة: {total_questions}")
    output_content.append(f"📅 تاريخ الإنشاء: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_content.append("")
    
    # حفظ الملف
    output_file = "اجابات_الاسئلة_احياء_صف_تاسع.txt"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_content))
        
        print(f"\n🎉 تم إنشاء ملف الأسئلة والإجابات بنجاح!")
        print(f"📁 اسم الملف: {output_file}")
        print(f"📊 إجمالي الأسئلة: {total_questions}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في حفظ الملف: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    create_answers_file()

if __name__ == "__main__":
    main()