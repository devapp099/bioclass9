#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح الأخطاء الحرجة في JavaScript - حل عاجل
"""

import os
import re

def fix_critical_js_errors(file_path):
    """إصلاح الأخطاء الحرجة في JavaScript"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        updated = False
        
        # البحث عن المشكلة الأساسية - JavaScript المكسور
        # 1. إصلاح مشكلة SoundSystem مع bank المعطل
        soundsystem_pattern = r'this\.sounds\s*\[\s*\{q:'
        if re.search(soundsystem_pattern, content):
            print(f"🔧 إصلاح خطأ حرج في SoundSystem في {file_path}")
            
            # نجد نهاية SoundSystem وبداية bank
            # استخراج كل ما بين Object.keys حتى بداية bank
            fix_pattern = r'(Object\.keys\(soundMappings\)\.forEach\(type => \{\s*this\.sounds)([^}]+?)(\[[\s\S]*?\{q:)'
            
            match = re.search(fix_pattern, content)
            if match:
                # إصلاح صحيح
                fixed_section = match.group(1) + '[type] = new Howl({\n            src: [`assets/audio/${soundMappings[type]}`],\n            volume: 0.3,\n            html5: true\n          });\n        });\n      },\n      play(type) {\n        if (this.enabled && this.sounds[type]) {\n          this.sounds[type].play();\n        }\n      }\n    };\n\n    const bank = ' + match.group(3)
                
                content = content.replace(match.group(0), fixed_section)
                updated = True
                print(f"✅ تم إصلاح JavaScript في {file_path}")
        
        # 2. التأكد من وجود إغلاق صحيح لـ bank
        if 'const bank =' in content and '];' not in content:
            # البحث عن آخر سؤال وإضافة إغلاق
            last_question_pattern = r'(\{q:"[^"]+",\s*c:\[[^\]]+\],\s*a:\d+\})\s*$'
            match = re.search(last_question_pattern, content, re.MULTILINE)
            if match:
                content = content.replace(match.group(1), match.group(1) + '\n    ];')
                updated = True
                print(f"✅ تم إضافة إغلاق صحيح لـ bank في {file_path}")
        
        # 3. إضافة init لـ SoundSystem إذا لم يكن موجوداً
        if 'SoundSystem = {' in content and 'SoundSystem.init()' not in content:
            # إضافة استدعاء init
            init_call = '\n    SoundSystem.init();'
            if 'renderQuestions();' in content:
                content = content.replace('renderQuestions();', 'SoundSystem.init();\n    renderQuestions();')
                updated = True
                print(f"✅ تم إضافة استدعاء SoundSystem.init() في {file_path}")
        
        # حفظ الملف إذا تم التحديث
        if updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            print(f"ℹ️  لا يحتاج إصلاح JavaScript: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في إصلاح JavaScript في {file_path}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚨 إصلاح الأخطاء الحرجة في JavaScript...")
    print("=" * 60)
    
    # فحص نفس العينة
    sample_lessons = [
        "unit-1-cells/lesson-1-1/index.html",
        "unit-1-cells/lesson-1-2/index.html", 
        "unit-2-transport/lesson-2-1/index.html",
        "unit-6-homeostasis/lesson-6-4/index.html"
    ]
    
    fixed_count = 0
    
    for lesson in sample_lessons:
        if os.path.exists(lesson):
            print(f"🔄 معالجة: {lesson}")
            if fix_critical_js_errors(lesson):
                fixed_count += 1
        else:
            print(f"❌ الملف غير موجود: {lesson}")
    
    print("\n" + "=" * 60)
    print(f"🎉 انتهاء العملية!")
    print(f"✅ تم إصلاح {fixed_count} درس من أصل {len(sample_lessons)}")
    print("🔧 إذا استمرت المشكلة، سنقوم بنسخ الأسئلة من مجلد Q مرة أخرى")

if __name__ == "__main__":
    main()