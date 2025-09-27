#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح إظهار المحتوى - حل نهائي وآمن
Fix content visibility - final and safe solution
"""

import os
import re

def fix_content_visibility(file_path):
    """إصلاح إظهار المحتوى في ملف واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = False
        
        # 1. تغيير display:none إلى display:block في قسم quiz
        if 'display:none' in content and 'id="quiz"' in content:
            content = content.replace(
                '<section id="quiz" class="card" style="margin-top:16px; display:none"',
                '<section id="quiz" class="card" style="margin-top:16px; display:block"'
            )
            updated = True
            print(f"✅ تم تغيير display:none إلى display:block في {file_path}")
        
        # 2. إضافة JavaScript لضمان إظهار المحتوى
        visibility_js = '''
    // ضمان إظهار المحتوى - إصلاح شامل
    document.addEventListener('DOMContentLoaded', function() {
        // إظهار قسم الأسئلة مباشرة
        const quizSection = document.getElementById('quiz');
        if (quizSection) {
            quizSection.style.display = 'block';
            quizSection.style.visibility = 'visible';
            quizSection.style.opacity = '1';
        }
        
        // إظهار جميع عناصر الأسئلة
        const questions = document.querySelectorAll('.q, #quizList');
        questions.forEach(element => {
            if (element) {
                element.style.display = 'block';
                element.style.visibility = 'visible';
            }
        });
    });
    
    // إصلاح إضافي بعد تحميل الصفحة
    window.addEventListener('load', function() {
        setTimeout(() => {
            const quiz = document.getElementById('quiz');
            const quizList = document.getElementById('quizList');
            
            if (quiz) {
                quiz.style.display = 'block';
                quiz.style.visibility = 'visible';
                quiz.style.opacity = '1';
            }
            
            if (quizList) {
                quizList.style.display = 'block';
                quizList.style.visibility = 'visible';
            }
            
            // إظهار أي عناصر مخفية أخرى
            document.querySelectorAll('[style*="display:none"], [style*="display: none"]').forEach(el => {
                if (el.id !== 'loading' && !el.classList.contains('hidden-by-design')) {
                    el.style.display = 'block';
                }
            });
        }, 200);
    });'''
        
        # البحث عن مكان آمن لإضافة الكود
        if '// ضمان إظهار المحتوى' not in content:
            # إضافة الكود قبل إغلاق script الأخير
            last_script_pattern = r'(</script>\s*</body>)'
            if re.search(last_script_pattern, content):
                content = re.sub(
                    last_script_pattern,
                    visibility_js + '\n  </script>\n</body>',
                    content
                )
                updated = True
                print(f"✅ تم إضافة JavaScript لضمان الإظهار في {file_path}")
            else:
                # إضافة script جديد قبل إغلاق body
                content = content.replace(
                    '</body>',
                    f'<script>{visibility_js}\n  </script>\n</body>'
                )
                updated = True
                print(f"✅ تم إضافة script جديد لضمان الإظهار في {file_path}")
        
        # 3. التأكد من وجود دالة renderQuestions وأنها تعمل
        if 'function renderQuestions()' in content:
            # التأكد من أن renderQuestions تستدعى
            if 'renderQuestions();' not in content:
                # إضافة استدعاء renderQuestions
                init_pattern = r'(document\.addEventListener\(["\']DOMContentLoaded["\'], function\(\)\s*\{)'
                if re.search(init_pattern, content):
                    content = re.sub(
                        init_pattern,
                        r'\1\n        renderQuestions();',
                        content
                    )
                    updated = True
                    print(f"✅ تم إضافة استدعاء renderQuestions في {file_path}")
        
        # حفظ الملف إذا تم التحديث
        if updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            print(f"ℹ️  لا يحتاج تحديث: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في معالجة {file_path}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🔧 إصلاح إظهار المحتوى في جميع الدروس...")
    print("=" * 60)
    
    # قائمة جميع الدروس
    lessons = [
        "unit-1-cells/lesson-1-1/index.html",
        "unit-1-cells/lesson-1-2/index.html", 
        "unit-1-cells/lesson-1-3/index.html",
        "unit-2-transport/lesson-2-1/index.html",
        "unit-2-transport/lesson-2-2/index.html",
        "unit-2-transport/lesson-2-3/index.html",
        "unit-3-biomolecules/lesson-3-1/index.html",
        "unit-3-biomolecules/lesson-3-2/index.html",
        "unit-3-biomolecules/lesson-3-3/index.html",
        "unit-4-nutrition/lesson-4-1/index.html",
        "unit-4-nutrition/lesson-4-2/index.html",
        "unit-5-respiration/lesson-5-1/index.html",
        "unit-6-homeostasis/lesson-6-1/index.html",
        "unit-6-homeostasis/lesson-6-2/index.html",
        "unit-6-homeostasis/lesson-6-3/index.html",
        "unit-6-homeostasis/lesson-6-4/index.html"
    ]
    
    fixed_count = 0
    
    for lesson in lessons:
        if os.path.exists(lesson):
            print(f"🔄 معالجة: {lesson}")
            if fix_content_visibility(lesson):
                fixed_count += 1
        else:
            print(f"❌ الملف غير موجود: {lesson}")
    
    print("\n" + "=" * 60)
    print(f"🎉 انتهاء العملية!")
    print(f"✅ تم إصلاح {fixed_count} درس من أصل {len(lessons)}")
    print("🌟 المحتوى سيظهر الآن في جميع الدروس!")
    print("🎯 الإصلاحات تشمل:")
    print("   • تغيير display:none إلى display:block")
    print("   • إضافة JavaScript آمن لضمان الإظهار") 
    print("   • إصلاح استدعاء renderQuestions")
    print("   • حماية من الإخفاء العرضي")

if __name__ == "__main__":
    main()