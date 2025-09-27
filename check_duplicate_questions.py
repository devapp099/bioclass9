#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
التحقق من الأسئلة المكررة في جميع الدروس
Check for duplicate questions across all lessons
"""

import os
import re
from collections import defaultdict

def extract_questions_from_lesson(file_path):
    """استخراج الأسئلة من درس واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # استخراج عنوان الدرس
        title_match = re.search(r'<title>([^<]+)</title>', content)
        lesson_title = title_match.group(1) if title_match else "درس غير محدد"
        
        # البحث عن الأسئلة في JavaScript
        question_pattern = r'\{\s*q:\s*["\']([^"\']+)["\']\s*,\s*c:\s*\[(.*?)\]\s*,\s*a:\s*(\d+)\s*\}'
        question_matches = re.findall(question_pattern, content, re.DOTALL)
        
        questions = []
        for i, (question, choices_str, answer_idx) in enumerate(question_matches, 1):
            # تنظيف النص
            clean_question = question.strip()
            questions.append({
                'text': clean_question,
                'number': i,
                'choices': choices_str,
                'answer': answer_idx
            })
        
        return lesson_title, questions
        
    except Exception as e:
        print(f"❌ خطأ في قراءة {file_path}: {e}")
        return None, []

def find_duplicate_questions():
    """العثور على الأسئلة المكررة"""
    
    print("🔄 بدء التحقق من الأسئلة المكررة في جميع الدروس...")
    print("=" * 70)
    
    # قائمة الدروس
    lessons = [
        ("unit-1-cells/lesson-1-1/index.html", "🔬 درس 1-1"),
        ("unit-1-cells/lesson-1-2/index.html", "🧪 درس 1-2"),
        ("unit-1-cells/lesson-1-3/index.html", "🔍 درس 1-3"),
        ("unit-2-transport/lesson-2-1/index.html", "🚛 درس 2-1"),
        ("unit-2-transport/lesson-2-2/index.html", "💧 درس 2-2"),
        ("unit-2-transport/lesson-2-3/index.html", "⚡ درس 2-3"),
        ("unit-3-biomolecules/lesson-3-1/index.html", "🧬 درس 3-1"),
        ("unit-3-biomolecules/lesson-3-2/index.html", "🧪 درس 3-2"),
        ("unit-3-biomolecules/lesson-3-3/index.html", "⚗️ درس 3-3"),
        ("unit-4-nutrition/lesson-4-1/index.html", "🍎 درس 4-1"),
        ("unit-4-nutrition/lesson-4-2/index.html", "🔄 درس 4-2"),
        ("unit-5-respiration/lesson-5-1/index.html", "💨 درس 5-1"),
        ("unit-6-homeostasis/lesson-6-1/index.html", "⚖️ درس 6-1"),
        ("unit-6-homeostasis/lesson-6-2/index.html", "🌡️ درس 6-2"),
        ("unit-6-homeostasis/lesson-6-3/index.html", "🍬 درس 6-3"),
        ("unit-6-homeostasis/lesson-6-4/index.html", "🧠 درس 6-4")
    ]
    
    # قاموس لتتبع الأسئلة
    all_questions = {}  # question_text -> [(lesson, question_number), ...]
    lesson_questions = {}  # lesson -> questions
    
    # استخراج الأسئلة من جميع الدروس
    for lesson_path, lesson_short_name in lessons:
        if os.path.exists(lesson_path):
            print(f"🔄 معالجة: {lesson_short_name}")
            
            title, questions = extract_questions_from_lesson(lesson_path)
            lesson_questions[lesson_short_name] = questions
            
            for q in questions:
                question_text = q['text'].lower().strip()
                if question_text not in all_questions:
                    all_questions[question_text] = []
                all_questions[question_text].append((lesson_short_name, q['number']))
            
            print(f"✅ تم استخراج {len(questions)} سؤال")
        else:
            print(f"❌ الملف غير موجود: {lesson_path}")
    
    # البحث عن الأسئلة المكررة
    duplicates = {}
    similar_questions = {}
    
    for question_text, occurrences in all_questions.items():
        if len(occurrences) > 1:
            duplicates[question_text] = occurrences
    
    # البحث عن الأسئلة المتشابهة (تحتوي على كلمات مشتركة)
    question_texts = list(all_questions.keys())
    for i, q1 in enumerate(question_texts):
        for j, q2 in enumerate(question_texts[i+1:], i+1):
            # حساب نسبة التشابه
            words1 = set(q1.split())
            words2 = set(q2.split())
            common_words = words1.intersection(words2)
            if len(common_words) >= 3 and len(common_words) / len(words1.union(words2)) > 0.6:
                if q1 not in similar_questions:
                    similar_questions[q1] = []
                similar_questions[q1].append(q2)
    
    # إنشاء التقرير
    report = []
    report.append("=" * 80)
    report.append("📊 تقرير التحقق من الأسئلة المكررة - مادة الأحياء للصف التاسع")
    report.append("=" * 80)
    report.append("")
    report.append("🎨 تصميم: الوتين الضامرية | لمار السيابية | مها المعمرية")
    report.append("         مريم محمود البلوشية | مريم وائل البلوشية | مريم زكي العويسية")
    report.append("🏫 مدرسة عاتكة بنت زيد")
    report.append("👩‍🏫 تحت إشراف الأستاذة وفاء")
    report.append("")
    report.append("=" * 80)
    report.append("")
    
    # إحصائيات عامة
    total_questions = sum(len(questions) for questions in lesson_questions.values())
    report.append("📊 الإحصائيات العامة:")
    report.append("-" * 30)
    report.append(f"📚 عدد الدروس: {len(lesson_questions)}")
    report.append(f"❓ إجمالي الأسئلة: {total_questions}")
    report.append(f"🔄 الأسئلة المكررة: {len(duplicates)}")
    report.append(f"📊 الأسئلة الفريدة: {len(all_questions)}")
    report.append("")
    
    # تفاصيل الأسئلة المكررة
    if duplicates:
        report.append("🔄 الأسئلة المكررة:")
        report.append("=" * 50)
        report.append("")
        
        for i, (question_text, occurrences) in enumerate(duplicates.items(), 1):
            report.append(f"التكرار رقم {i}:")
            report.append(f"السؤال: {question_text}")
            report.append("موجود في:")
            for lesson, q_num in occurrences:
                report.append(f"  • {lesson} - السؤال رقم {q_num}")
            report.append("-" * 40)
            report.append("")
    else:
        report.append("✅ لا توجد أسئلة مكررة!")
        report.append("")
    
    # تفاصيل الأسئلة المتشابهة
    if similar_questions:
        report.append("🔍 الأسئلة المتشابهة:")
        report.append("=" * 50)
        report.append("")
        
        for i, (q1, similar_list) in enumerate(similar_questions.items(), 1):
            report.append(f"مجموعة متشابهة رقم {i}:")
            report.append(f"السؤال الأول: {q1}")
            for similar_q in similar_list:
                report.append(f"مشابه لـ: {similar_q}")
            report.append("-" * 40)
            report.append("")
    
    # إحصائيات كل درس
    report.append("📚 إحصائيات الدروس:")
    report.append("=" * 50)
    report.append("")
    
    for lesson_name, questions in lesson_questions.items():
        report.append(f"{lesson_name}: {len(questions)} سؤال")
        
        # حساب الأسئلة المكررة في هذا الدرس
        lesson_duplicates = 0
        for q in questions:
            q_text = q['text'].lower().strip()
            if q_text in duplicates:
                lesson_duplicates += 1
        
        if lesson_duplicates > 0:
            report.append(f"  🔄 يحتوي على {lesson_duplicates} سؤال مكرر")
        else:
            report.append(f"  ✅ جميع الأسئلة فريدة")
        report.append("")
    
    # معلومات التقرير
    report.append("=" * 80)
    report.append("📄 معلومات التقرير:")
    report.append("=" * 80)
    report.append(f"📅 تاريخ الإنشاء: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"🔍 طريقة التحقق: مقارنة نصوص الأسئلة")
    report.append(f"📊 معدل التكرار: {len(duplicates)/len(all_questions)*100:.1f}%")
    report.append("")
    
    # حفظ التقرير
    report_file = "تقرير_الاسئلة_المكررة.txt"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print("\n" + "=" * 70)
        print("🎉 تم إنشاء تقرير التحقق من الأسئلة المكررة بنجاح!")
        print(f"📁 اسم الملف: {report_file}")
        print(f"📊 النتائج:")
        print(f"   • إجمالي الأسئلة: {total_questions}")
        print(f"   • الأسئلة الفريدة: {len(all_questions)}")
        print(f"   • الأسئلة المكررة: {len(duplicates)}")
        print(f"   • معدل التكرار: {len(duplicates)/len(all_questions)*100:.1f}%")
        
        if duplicates:
            print("⚠️ تم العثور على أسئلة مكررة - راجع التقرير للتفاصيل")
        else:
            print("✅ جميع الأسئلة فريدة - لا توجد تكرارات!")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في حفظ التقرير: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    find_duplicate_questions()

if __name__ == "__main__":
    main()