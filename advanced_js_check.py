#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def check_javascript_syntax(lesson_path):
    """فحص أخطاء JavaScript المحتملة"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        warnings = []
        
        # استخراج كل JavaScript
        js_blocks = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
        
        for i, js_content in enumerate(js_blocks):
            # فحص الأقواس
            open_braces = js_content.count('{')
            close_braces = js_content.count('}')
            open_parens = js_content.count('(')
            close_parens = js_content.count(')')
            open_brackets = js_content.count('[')
            close_brackets = js_content.count(']')
            
            if open_braces != close_braces:
                issues.append(f"❌ Script {i+1}: عدم توازن الأقواس المجعدة - فتح: {open_braces}, إغلاق: {close_braces}")
            
            if open_parens != close_parens:
                issues.append(f"❌ Script {i+1}: عدم توازن الأقواس العادية - فتح: {open_parens}, إغلاق: {close_parens}")
            
            if open_brackets != close_brackets:
                issues.append(f"❌ Script {i+1}: عدم توازن الأقواس المربعة - فتح: {open_brackets}, إغلاق: {close_brackets}")
            
            # فحص أخطاء شائعة
            if 'addEventListener(' in js_content:
                # فحص addEventListener غير مكتمل
                listeners = re.findall(r'addEventListener\([^)]*\)', js_content)
                for listener in listeners:
                    if listener.count('(') != listener.count(')'):
                        issues.append(f"❌ Script {i+1}: addEventListener غير مكتمل: {listener[:50]}...")
            
            # فحص function declarations
            functions = re.findall(r'function\s+\w+\s*\([^)]*\)\s*{', js_content)
            for func in functions:
                if '{' not in func:
                    issues.append(f"❌ Script {i+1}: تعريف دالة غير صحيح: {func}")
            
            # فحص el. definitions
            if 'const el =' in js_content or 'let el =' in js_content or 'var el =' in js_content:
                el_match = re.search(r'(?:const|let|var)\s+el\s*=\s*{([^}]*)}', js_content, re.DOTALL)
                if not el_match:
                    issues.append(f"❌ Script {i+1}: تعريف متغير el غير مكتمل")
            
            # فحص AOS.init()
            if 'AOS.init(' in js_content:
                aos_init = re.search(r'AOS\.init\([^)]*\)', js_content)
                if aos_init and aos_init.group().count('(') != aos_init.group().count(')'):
                    issues.append(f"❌ Script {i+1}: AOS.init غير مكتمل")
            
        # فحص HTML structure
        if not re.search(r'<div\s+class=["\']wrap["\']', content):
            issues.append("❌ عنصر .wrap الرئيسي مفقود")
        
        if not re.search(r'id=["\']btnStart["\']', content):
            issues.append("❌ زر البداية مفقود")
        
        # فحص CSS
        if not re.search(r'<style>', content):
            issues.append("❌ قسم CSS مفقود")
        
        return {
            'issues': issues,
            'warnings': warnings,
            'js_blocks_count': len(js_blocks),
            'total_js_size': sum(len(block) for block in js_blocks)
        }
        
    except Exception as e:
        return {'error': str(e)}

def create_minimal_working_template():
    """إنشاء قالب أساسي يعمل"""
    return '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <title>اختبار سريع</title>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@500;700;900&display=swap" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
  <style>
    :root {
      --bg: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
      --card: #ffffff;
      --text: #1f2937;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      min-height: 100vh;
      color: var(--text);
      font-family: "Cairo", system-ui, sans-serif;
    }
    .wrap {
      max-width: 1100px;
      margin: 0 auto;
      padding: 24px;
    }
    .card {
      background: white;
      border-radius: 22px;
      padding: 22px;
      margin-bottom: 16px;
      box-shadow: 0 20px 40px rgba(0,0,0,.1);
    }
    .btn {
      background: #f59e0b;
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 12px;
      font-size: 16px;
      cursor: pointer;
      font-family: inherit;
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>🧪 اختبار سريع</h1>
      <p>هذا اختبار للتأكد من أن الصفحة تعمل</p>
      <button id="testBtn" class="btn">اختبار</button>
    </div>
  </div>
  
  <script>
    document.getElementById('testBtn').addEventListener('click', function() {
      Swal.fire({
        title: 'نجح الاختبار!',
        text: 'الصفحة تعمل بشكل صحيح',
        icon: 'success'
      });
    });
    
    console.log('✅ الصفحة تم تحميلها بنجاح');
  </script>
</body>
</html>'''

def main():
    base_path = Path(".")
    lessons = []
    
    # البحث عن جميع دروس الوحدات
    for unit_dir in base_path.glob("unit-*"):
        if unit_dir.is_dir():
            for lesson_dir in unit_dir.glob("lesson-*"):
                if lesson_dir.is_dir():
                    index_file = lesson_dir / "index.html"
                    if index_file.exists():
                        lessons.append({
                            'path': str(index_file),
                            'unit': unit_dir.name,
                            'lesson': lesson_dir.name,
                            'full_name': f"{unit_dir.name}/{lesson_dir.name}"
                        })
    
    print("🔍 فحص متقدم لأخطاء JavaScript...")
    print("=" * 80)
    
    critical_issues = []
    
    for lesson in sorted(lessons, key=lambda x: x['full_name'])[:5]:  # فحص أول 5 دروس فقط
        print(f"\n📚 فحص الدرس: {lesson['full_name']}")
        print("-" * 40)
        
        diagnosis = check_javascript_syntax(lesson['path'])
        
        if 'error' in diagnosis:
            print(f"❌ خطأ في القراءة: {diagnosis['error']}")
            continue
        
        if diagnosis['issues']:
            print("🚨 مشاكل حرجة:")
            for issue in diagnosis['issues']:
                print(f"  {issue}")
            critical_issues.append(lesson['full_name'])
        else:
            print("✅ لا توجد مشاكل JavaScript واضحة")
        
        print(f"📊 عدد كتل JavaScript: {diagnosis['js_blocks_count']}")
        print(f"📦 حجم JavaScript: {diagnosis['total_js_size']} حرف")
    
    if critical_issues:
        print(f"\n🚨 دروس تحتاج إصلاح فوري:")
        for lesson in critical_issues:
            print(f"  - {lesson}")
        
        print(f"\n💡 اقتراح: إنشاء صفحة اختبار بسيطة")
        
        # إنشاء صفحة اختبار
        test_path = base_path / "test-simple.html"
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(create_minimal_working_template())
        
        print(f"✅ تم إنشاء صفحة اختبار: {test_path}")
        print(f"🔗 افتحها في المتصفح للتأكد من أن المشكلة في الدروس وليس في البيئة")
    
    else:
        print(f"\n🤔 لا توجد أخطاء JavaScript واضحة")
        print(f"💭 المشكلة قد تكون في:")
        print(f"   - تحميل المكتبات الخارجية")
        print(f"   - إعدادات الخادم")
        print(f"   - مشاكل الشبكة")

if __name__ == "__main__":
    main()