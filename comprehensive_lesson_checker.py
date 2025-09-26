#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 فاحص شامل للدروس التفاعلية
=============================
فحص جميع الدروس للتأكد من عمل:
1. زر "ابدأ النشاط"
2. النظام الصوتي
3. الرسائل التفاعلية الموجهة
"""

import os
import re
from pathlib import Path

class LessonChecker:
    def __init__(self):
        self.workspace_path = Path.cwd()
        self.issues_found = []
        
    def check_lesson_file(self, file_path):
        """فحص ملف درس واحد للمشاكل المحتملة"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return [f"❌ خطأ في قراءة الملف: {str(e)}"]
        
        issues = []
        lesson_name = f"{file_path.parent.parent.name}/{file_path.parent.name}"
        
        # 1. فحص زر "ابدأ النشاط"
        if not self.check_start_button(content):
            issues.append("🔴 زر 'ابدأ النشاط' غير موجود أو غير مرتبط")
        
        # 2. فحص النظام الصوتي
        sound_issues = self.check_sound_system(content)
        issues.extend(sound_issues)
        
        # 3. فحص الرسائل التفاعلية
        message_issues = self.check_interactive_messages(content)
        issues.extend(message_issues)
        
        # 4. فحص المكتبات المطلوبة
        library_issues = self.check_required_libraries(content)
        issues.extend(library_issues)
        
        # 5. فحص تهيئة JavaScript
        js_issues = self.check_javascript_initialization(content)
        issues.extend(js_issues)
        
        return issues
    
    def check_start_button(self, content):
        """فحص زر ابدأ النشاط"""
        # البحث عن الزر
        if 'id="btnStart"' not in content:
            return False
        
        # البحث عن ربط الزر بالحدث
        if 'el.start.addEventListener' not in content and 'btnStart.addEventListener' not in content:
            return False
            
        # البحث عن دالة askStudent
        if 'askStudent' not in content:
            return False
            
        return True
    
    def check_sound_system(self, content):
        """فحص النظام الصوتي"""
        issues = []
        
        # فحص وجود مكتبة Howler
        if 'howler' not in content.lower():
            issues.append("🔴 مكتبة Howler.js غير محملة")
        
        # فحص وجود SoundSystem
        if 'const SoundSystem' not in content:
            issues.append("🔴 SoundSystem غير معرّف")
        elif 'SoundSystem.init()' not in content:
            issues.append("🟡 SoundSystem غير مهيأ بشكل صحيح")
        
        # فحص استخدام الأصوات
        sound_usage = re.findall(r'SoundSystem\.play\([\'"]([^\'"]+)[\'"]', content)
        if len(sound_usage) == 0:
            issues.append("🟡 لا يتم استخدام أي أصوات")
        
        # فحص وجود sfx قديم
        if 'const sfx' in content:
            issues.append("🟡 نظام صوتي قديم (sfx) ما زال موجود")
        
        return issues
    
    def check_interactive_messages(self, content):
        """فحص الرسائل التفاعلية الموجهة"""
        issues = []
        
        # فحص وجود نظام الإشعارات
        if 'NotificationSystem' not in content and 'EnhancedNotificationSystem' not in content:
            issues.append("🔴 نظام الإشعارات غير موجود")
        
        # فحص وجود مكتبة SweetAlert2
        if 'sweetalert2' not in content.lower() and 'swal.fire' not in content.lower():
            issues.append("🔴 مكتبة SweetAlert2 غير محملة")
        
        # فحص الرسائل الترحيبية
        if 'showWelcomeMessage' not in content and 'welcome' not in content.lower():
            issues.append("🟡 رسائل الترحيب غير موجودة")
        
        # فحص استخدام اسم الطالب في الرسائل
        if '{name}' not in content and '{student' not in content:
            issues.append("🟡 الرسائل غير مخصصة بالاسم")
        
        return issues
    
    def check_required_libraries(self, content):
        """فحص المكتبات المطلوبة"""
        issues = []
        
        required_libs = {
            'sweetalert2': 'SweetAlert2',
            'howler': 'Howler.js',
            'gsap': 'GSAP',
            'confetti': 'Canvas Confetti'
        }
        
        for lib, name in required_libs.items():
            if lib not in content.lower():
                issues.append(f"🟡 مكتبة {name} قد تكون غير محملة")
        
        return issues
    
    def check_javascript_initialization(self, content):
        """فحص تهيئة JavaScript"""
        issues = []
        
        # فحص DOMContentLoaded
        if 'DOMContentLoaded' not in content:
            issues.append("🟡 قد لا يتم تهيئة JavaScript بشكل صحيح")
        
        # فحص المتغيرات المطلوبة
        required_vars = ['el.start', 'el.quiz', 'bank']
        for var in required_vars:
            if var not in content:
                issues.append(f"🟡 متغير مطلوب قد يكون غير معرّف: {var}")
        
        return issues
        
    def generate_fix_for_lesson(self, file_path, issues):
        """إنشاء إصلاح للدرس بناءً على المشاكل المكتشفة"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return False
        
        modified = False
        
        # إصلاح زر البداية إذا كان غير مرتبط
        if any('زر' in issue for issue in issues):
            if 'el.start.addEventListener' not in content and 'btnStart' in content:
                # البحث عن نهاية تعريف المتغيرات
                if 'el.start =' in content or 'getElementById(\'btnStart\')' in content:
                    # إضافة ربط الحدث
                    if 'askStudent' in content:
                        content = content.replace(
                            'el.start.addEventListener(\'click\', askStudent);',
                            'el.start.addEventListener(\'click\', askStudent);'
                        )
                        if 'el.start.addEventListener' not in content:
                            # البحث عن مكان مناسب لإضافة الربط
                            insert_pos = content.find('function askStudent')
                            if insert_pos > 0:
                                content = content[:insert_pos] + 'el.start.addEventListener(\'click\', askStudent);\n\n    ' + content[insert_pos:]
                                modified = True
        
        # إصلاح النظام الصوتي
        if any('SoundSystem' in issue for issue in issues):
            if 'const SoundSystem' not in content and 'howler' in content.lower():
                # إضافة النظام الصوتي
                howler_pos = content.find('</script>', content.find('howler'))
                if howler_pos != -1:
                    sound_system_code = self.get_sound_system_code()
                    insert_pos = howler_pos + len('</script>')
                    content = content[:insert_pos] + sound_system_code + content[insert_pos:]
                    modified = True
        
        # إصلاح الرسائل التفاعلية
        if any('إشعارات' in issue or 'رسائل' in issue for issue in issues):
            if 'EnhancedNotificationSystem' not in content and 'sweetalert2' in content.lower():
                notification_code = self.get_notification_system_code()
                # إضافة بعد النظام الصوتي
                sound_pos = content.rfind('};', content.find('SoundSystem'))
                if sound_pos > 0:
                    content = content[:sound_pos + 2] + notification_code + content[sound_pos + 2:]
                    modified = True
        
        if modified:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            except:
                return False
        
        return False
    
    def get_sound_system_code(self):
        """الحصول على كود النظام الصوتي"""
        return '''

    // 🔊 النظام الصوتي المحسّن
    const SoundSystem = {
      enabled: true,
      currentVolume: 0.7,
      sounds: {},
      
      init() {
        const soundMappings = {
          'correct': 'win.mp3',
          'wrong': 'wrong_answer.mp3', 
          'click': 'Click.mp3',
          'select': 'select.mp3',
          'milestone': 'g.mp3',
          'celebration': 'win-Blockbusters.mp3',
          'complete': 'end-timer.mp3',
          'start': 'start-timer.mp3',
          'welcome': 'name-start.mp3',
          'progress': 'Notification.mp3'
        };
        
        Object.keys(soundMappings).forEach(type => {
          this.sounds[type] = new Howl({
            src: [`../../assets/audio/${soundMappings[type]}`],
            volume: this.getContextualVolume(type),
            preload: true,
            onloaderror: () => console.warn(`فشل تحميل الصوت: ${type}`)
          });
        });
        
        console.log('🎵 تم تهيئة النظام الصوتي');
      },
      
      play(soundType) {
        if (!this.enabled || !this.sounds[soundType]) return;
        try {
          this.sounds[soundType].volume(this.getContextualVolume(soundType));
          this.sounds[soundType].play();
        } catch (error) {
          console.warn(`خطأ في تشغيل الصوت ${soundType}:`, error);
        }
      },
      
      getContextualVolume(soundType) {
        const contextMap = {
          'celebration': 0.9, 'milestone': 0.8, 'correct': 0.7,
          'welcome': 0.6, 'wrong': 0.5, 'progress': 0.4,
          'click': 0.4, 'select': 0.3
        };
        return contextMap[soundType] || this.currentVolume;
      }
    };'''
    
    def get_notification_system_code(self):
        """الحصول على كود نظام الإشعارات"""
        return '''

    // 🤖 نظام الرسائل التفاعلية
    const EnhancedNotificationSystem = {
      student: null,
      
      showWelcomeMessage() {
        const welcomeMessages = [
          "🎓 أهلاً وسهلاً {name}! مرحبًا بك في هذا الدرس المثير!",
          "🌟 مرحبًا {name}! أنت على وشك تعلم شيء رائع!",
          "✨ أهلاً {name}! دعنا نتعلم العلوم معًا!"
        ];
        
        const randomWelcome = welcomeMessages[Math.floor(Math.random() * welcomeMessages.length)];
        const personalizedWelcome = randomWelcome.replace('{name}', this.student?.name || 'البطل/ة');
        
        Swal.fire({
          title: '🎓 مرحباً بك!',
          text: personalizedWelcome,
          icon: 'success',
          confirmButtonText: '🚀 لنبدأ!',
          timer: 4000,
          timerProgressBar: true
        }).then(() => {
          SoundSystem.play('start');
        });
      },
      
      initForStudent(studentData) {
        this.student = studentData;
        this.showWelcomeMessage();
      }
    };'''
    
    def check_all_lessons(self):
        """فحص جميع الدروس"""
        
        print("🔍 بدء الفحص الشامل لجميع الدروس...")
        print("=" * 50)
        
        total_lessons = 0
        lessons_with_issues = 0
        all_issues = {}
        
        # فحص جميع الدروس
        for unit_dir in self.workspace_path.iterdir():
            if unit_dir.is_dir() and unit_dir.name.startswith('unit-'):
                for lesson_dir in unit_dir.iterdir():
                    if lesson_dir.is_dir() and lesson_dir.name.startswith('lesson-'):
                        index_file = lesson_dir / 'index.html'
                        
                        if index_file.exists():
                            total_lessons += 1
                            lesson_name = f"{unit_dir.name}/{lesson_dir.name}"
                            
                            print(f"\n🔍 فحص: {lesson_name}")
                            issues = self.check_lesson_file(index_file)
                            
                            if issues:
                                lessons_with_issues += 1
                                all_issues[lesson_name] = {
                                    'issues': issues,
                                    'file_path': index_file
                                }
                                
                                print(f"❌ مشاكل مكتشفة ({len(issues)}):")
                                for issue in issues:
                                    print(f"   {issue}")
                            else:
                                print("✅ لا توجد مشاكل")
        
        # تلخيص النتائج
        print(f"\n🏁 نتائج الفحص:")
        print(f"📊 إجمالي الدروس: {total_lessons}")
        print(f"❌ دروس بها مشاكل: {lessons_with_issues}")
        print(f"✅ دروس سليمة: {total_lessons - lessons_with_issues}")
        
        return all_issues
    
    def auto_fix_issues(self, all_issues):
        """إصلاح تلقائي للمشاكل"""
        
        if not all_issues:
            print("\n✅ لا توجد مشاكل تحتاج إصلاح!")
            return 0
        
        print(f"\n🔧 بدء الإصلاح التلقائي للمشاكل...")
        fixed_count = 0
        
        for lesson_name, lesson_data in all_issues.items():
            print(f"\n🔧 إصلاح: {lesson_name}")
            
            if self.generate_fix_for_lesson(lesson_data['file_path'], lesson_data['issues']):
                fixed_count += 1
                print(f"✅ تم إصلاح: {lesson_name}")
            else:
                print(f"⚠️ يحتاج إصلاح يدوي: {lesson_name}")
        
        print(f"\n🎉 تم إصلاح {fixed_count} من أصل {len(all_issues)} دروس")
        return fixed_count

def main():
    """التشغيل الرئيسي"""
    
    print("🔍 الفاحص الشامل للدروس التفاعلية")
    print("=" * 40)
    
    checker = LessonChecker()
    
    # فحص جميع الدروس
    all_issues = checker.check_all_lessons()
    
    if all_issues:
        print(f"\n🔧 هل تريد الإصلاح التلقائي؟")
        # إجراء الإصلاح التلقائي
        fixed_count = checker.auto_fix_issues(all_issues)
        
        if fixed_count > 0:
            print(f"\n✨ تم إصلاح {fixed_count} دروس بنجاح!")
            print("🚀 يُنصح بمراجعة الدروس والاختبار")
    else:
        print("\n🎉 جميع الدروس تعمل بشكل صحيح!")
    
    return True

if __name__ == "__main__":
    main()