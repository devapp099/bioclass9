#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت إصلاح التكرار والتداخل في ملفات الدروس
"""

import os
import re
from pathlib import Path
import shutil
from datetime import datetime

class CodeDuplicationFixer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.lessons_paths = []
        self.find_all_lessons()
        
    def find_all_lessons(self):
        """العثور على جميع دروس HTML"""
        for unit_dir in self.base_path.glob("unit-*"):
            if unit_dir.is_dir():
                for lesson_dir in unit_dir.glob("lesson-*"):
                    if lesson_dir.is_dir():
                        html_file = lesson_dir / "index.html"
                        if html_file.exists():
                            self.lessons_paths.append(html_file)
        
        print(f"🔍 تم العثور على {len(self.lessons_paths)} درس")
    
    def backup_file(self, file_path):
        """إنشاء نسخة احتياطية من الملف"""
        backup_path = file_path.with_suffix('.html.backup_fix')
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def analyze_file_issues(self, file_path):
        """تحليل مشاكل الملف"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # فحص تكرار SoundSystem
        sound_system_matches = re.findall(r'const SoundSystem\s*=\s*{', content)
        if len(sound_system_matches) > 1:
            issues.append(f"SoundSystem مكرر {len(sound_system_matches)} مرات")
        
        # فحص تكرار NotificationSystem  
        notification_matches = re.findall(r'const NotificationSystem\s*=\s*{', content)
        if len(notification_matches) > 1:
            issues.append(f"NotificationSystem مكرر {len(notification_matches)} مرات")
        
        # فحص تداخل HTML
        script_tags = re.findall(r'<script>', content)
        if len(script_tags) > 1:
            issues.append(f"تعدد تاجات script: {len(script_tags)}")
        
        # فحص تداخل footer
        footer_tags = re.findall(r'<footer', content)
        if len(footer_tags) > 1:
            issues.append(f"تعدد footer: {len(footer_tags)}")
        
        return issues
    
    def clean_html_structure(self, content):
        """تنظيف هيكل HTML"""
        # إصلاح تداخل footer
        content = re.sub(r'</footer>>\s*</div>\s*<footer[^>]*>[^<]*<script>>', 
                        '</footer>\n  </div>\n\n  <script>', content)
        
        # إصلاح تداخل div و span
        content = re.sub(r'<span class="credit">[^<]*</span></div>', 
                        '<span class="credit">🎨 تصميم: الوتين الضامرية |لمار السيابية|مها المعمرية|مريم محمود البلوشية|مريم وائل البلوشية|</span> — 🏫 مدرسة عاتكة بنت زيد — تحت إشراف الأستاذة سامية 👩‍🏫</div>', content)
        
        return content
    
    def remove_duplicate_systems(self, content):
        """إزالة تكرار الأنظمة الصوتية والإشعارات"""
        
        # البحث عن جميع مواضع SoundSystem
        sound_system_pattern = r'(// 🎵 نظام صوتي ذكي متقدم.*?};)\s*'
        sound_matches = list(re.finditer(sound_system_pattern, content, re.DOTALL))
        
        if len(sound_matches) > 1:
            # احتفظ بالأول فقط واحذف الباقي
            for i in range(1, len(sound_matches)):
                content = content[:sound_matches[i].start()] + content[sound_matches[i].end():]
                # إعادة حساب المواضع بعد الحذف
                sound_matches = list(re.finditer(sound_system_pattern, content, re.DOTALL))
        
        # البحث عن جميع مواضع NotificationSystem
        notification_pattern = r'(// 🔔 نظام الإشعارات والرسائل التفاعلية الذكي.*?};)\s*'
        notification_matches = list(re.finditer(notification_pattern, content, re.DOTALL))
        
        if len(notification_matches) > 1:
            # احتفظ بالأول فقط واحذف الباقي
            for i in range(1, len(notification_matches)):
                content = content[:notification_matches[i].start()] + content[notification_matches[i].end():]
                # إعادة حساب المواضع بعد الحذف
                notification_matches = list(re.finditer(notification_pattern, content, re.DOTALL))
        
        return content
    
    def fix_javascript_structure(self, content):
        """إصلاح هيكل JavaScript"""
        
        # التأكد من وجود AOS.init في المكان الصحيح
        if 'AOS.init({ duration: 700, once: true });' not in content:
            # إضافة AOS.init إذا لم يكن موجود
            script_start = content.find('<script>')
            if script_start != -1:
                insert_pos = content.find('\n', script_start) + 1
                content = content[:insert_pos] + '    AOS.init({ duration: 700, once: true });\n\n' + content[insert_pos:]
        
        return content
    
    def validate_fixed_file(self, content):
        """التحقق من أن الملف تم إصلاحه بنجاح"""
        issues = []
        
        # التحقق من عدم وجود تكرار
        sound_count = len(re.findall(r'const SoundSystem', content))
        if sound_count != 1:
            issues.append(f"SoundSystem count: {sound_count} (should be 1)")
        
        notification_count = len(re.findall(r'const NotificationSystem', content))
        if notification_count != 1:
            issues.append(f"NotificationSystem count: {notification_count} (should be 1)")
        
        # التحقق من هيكل HTML صحيح
        if content.count('<footer') > 1:
            issues.append("Multiple footer tags")
        
        if content.count('<script>') > 1:
            issues.append("Multiple script tags")
        
        return issues
    
    def fix_file(self, file_path):
        """إصلاح ملف واحد"""
        print(f"🔧 فحص وإصلاح: {file_path.relative_to(self.base_path)}")
        
        # تحليل المشاكل أولاً
        issues = self.analyze_file_issues(file_path)
        
        if not issues:
            print(f"   ✅ لا توجد مشاكل")
            return False
        
        print(f"   ⚠️  مشاكل موجودة: {', '.join(issues)}")
        
        # إنشاء نسخة احتياطية
        backup_path = self.backup_file(file_path)
        print(f"   💾 نسخة احتياطية: {backup_path.name}")
        
        # قراءة المحتوى
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # تطبيق الإصلاحات
        content = self.clean_html_structure(content)
        content = self.remove_duplicate_systems(content)
        content = self.fix_javascript_structure(content)
        
        # التحقق من الإصلاح
        validation_issues = self.validate_fixed_file(content)
        
        if validation_issues:
            print(f"   ❌ فشل في الإصلاح: {', '.join(validation_issues)}")
            return False
        
        # كتابة المحتوى المُصلح
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ تم الإصلاح بنجاح")
        return True
    
    def fix_all_files(self):
        """إصلاح جميع الملفات"""
        print(f"🚀 بدء فحص وإصلاح {len(self.lessons_paths)} درس")
        print(f"⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        fixed_count = 0
        clean_count = 0
        
        for lesson_path in self.lessons_paths:
            try:
                if self.fix_file(lesson_path):
                    fixed_count += 1
                else:
                    clean_count += 1
            except Exception as e:
                print(f"   ❌ خطأ: {str(e)}")
        
        print("="*60)
        print(f"📊 ملخص العملية:")
        print(f"   ✅ تم إصلاحها: {fixed_count} ملف")
        print(f"   ✨ نظيفة بالفعل: {clean_count} ملف")
        print(f"   📝 إجمالي: {len(self.lessons_paths)} ملف")
        print(f"🎉 انتهت عملية الإصلاح!")

def main():
    """الدالة الرئيسية"""
    base_path = r"c:\Users\ahm7d\Desktop\W"
    
    print("🔧 سكريبت إصلاح التكرار والتداخل في ملفات الدروس")
    print("=" * 60)
    
    fixer = CodeDuplicationFixer(base_path)
    fixer.fix_all_files()

if __name__ == "__main__":
    main()