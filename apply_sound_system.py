#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام تطبيق النظام الصوتي والتفاعلي المتقدم
على جميع صفحات الأنشطة التعليمية

المطور: مساعد GitHub Copilot
التاريخ: 2025/09/26
"""

import os
import re
from pathlib import Path
import shutil
from datetime import datetime

class SoundSystemApplier:
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
        for path in self.lessons_paths:
            print(f"   📄 {path.relative_to(self.base_path)}")
    
    def backup_file(self, file_path):
        """إنشاء نسخة احتياطية من الملف"""
        backup_path = file_path.with_suffix('.html.backup')
        shutil.copy2(file_path, backup_path)
        print(f"💾 تم إنشاء نسخة احتياطية: {backup_path.name}")
    
    def check_if_already_has_sound_system(self, content):
        """فحص ما إذا كان الملف يحتوي على النظام الصوتي بالفعل"""
        return "howler" in content.lower() and "SoundSystem" in content
    
    def add_howler_library(self, content):
        """إضافة مكتبة Howler للصوت"""
        if "howler" in content.lower():
            return content
            
        # البحث عن نهاية المكتبات الحالية
        pattern = r'(<script src="https://cdn\.jsdelivr\.net/npm/aos@2\.3\.4/dist/aos\.js"></script>)'
        replacement = r'\1\n  <script src="https://cdn.jsdelivr.net/npm/howler@2.2.4/dist/howler.min.js"></script>'
        
        return re.sub(pattern, replacement, content)
    
    def get_sound_system_code(self, lesson_title="الدرس"):
        """الحصول على كود النظام الصوتي الكامل"""
        return f'''
    // 🎵 نظام صوتي ذكي متقدم
    const SoundSystem = {{
      sounds: {{
        // أصوات الإجابات
        correct: new Howl({{ src: ['../../assets/audio/clap.mp3'], volume: 0.6 }}),
        wrong: new Howl({{ src: ['../../assets/audio/wrong_answer.mp3'], volume: 0.5 }}),
        
        // أصوات التفاعل
        click: new Howl({{ src: ['../../assets/audio/Click.mp3'], volume: 0.4 }}),
        select: new Howl({{ src: ['../../assets/audio/select.mp3'], volume: 0.4 }}),
        
        // أصوات التقدم والإنجاز
        progress: new Howl({{ src: ['../../assets/audio/Notification.mp3'], volume: 0.3 }}),
        milestone: new Howl({{ src: ['../../assets/audio/long-beep.mp3'], volume: 0.4 }}),
        
        // أصوات الاحتفال
        celebration: new Howl({{ src: ['../../assets/audio/win.mp3'], volume: 0.7 }}),
        firework: new Howl({{ src: ['../../assets/audio/win-Blockbusters.mp3'], volume: 0.5 }}),
        
        // أصوات التطبيق
        start: new Howl({{ src: ['../../assets/audio/startapp.mp3'], volume: 0.5 }}),
        reset: new Howl({{ src: ['../../assets/audio/reveal.mp3'], volume: 0.4 }})
      }},
      
      // تشغيل صوت مع تأثيرات بصرية
      play(soundName, visualEffect = null) {{
        if (this.sounds[soundName]) {{
          this.sounds[soundName].play();
          if (visualEffect) visualEffect();
        }}
      }},
      
      // تشغيل سلسلة أصوات
      playSequence(soundNames, delay = 300) {{
        soundNames.forEach((name, index) => {{
          setTimeout(() => this.play(name), index * delay);
        }});
      }}
    }};

    // 🔔 نظام الإشعارات والرسائل التفاعلية الذكي
    const NotificationSystem = {{
      student: null,
      
      // رسائل متنوعة حسب الأداء
      messages: {{
        welcome: [
          "أهلاً وسهلاً {{name}}! مرحبًا بك في {lesson_title} المثير! 🧬",
          "مرحبًا {{name}}! أنت على وشك خوض مغامرة علمية رائعة! 🔬",
          "أهلاً {{name}}! دعنا نكتشف أسرار العلوم معًا! ✨"
        ],
        
        encouragement: [
          "ممتاز {{name}}! أنت تتقدم بشكل رائع! 🌟",
          "أحسنت {{name}}! استمر على هذا الأداء المميز! 💪",
          "رائع {{name}}! أنت تبهرني بذكائك! 🧠",
          "عظيم {{name}}! كل إجابة تقربك من النجاح! 🎯"
        ],
        
        motivation: [
          "لا تستسلم {{name}}! المحاولة جزء من التعلم! 💚",
          "فكر مرة أخرى {{name}}، أنت أقرب للإجابة الصحيحة! 🤔",
          "المحاولة الجيدة {{name}}! التعلم من الأخطاء يجعلنا أقوى! 💎",
          "تركيزك يتحسن {{name}}! المحاولة القادمة ستكون أفضل! ⚡"
        ],
        
        milestone: [
          "🎉 ممتاز {{name}}! لقد أكملت 25% من الأسئلة!",
          "🚀 رائع {{name}}! وصلت لمنتصف الطريق - 50%!",
          "⭐ مذهل {{name}}! 75% مكتملة - أنت بطل/ة!",
          "🏆 تهانينا {{name}}! أكملت جميع الأسئلة بنجاح!"
        ],
        
        finalResults: {{
          excellent: [
            "🏆 مذهل {{name}}! أداء استثنائي - أنت عالم/ة حقيقي/ة!",
            "⭐ رائع جداً {{name}}! إتقان كامل للموضوع!"
          ],
          good: [
            "👏 أحسنت {{name}}! أداء جيد جداً - استمر في التفوق!",
            "💪 عمل ممتاز {{name}}! أنت على الطريق الصحيح!"
          ],
          average: [
            "📚 أداء جيد {{name}}! مراجعة بسيطة وستكون في القمة!",
            "🎯 استمر {{name}}! أنت تتحسن مع كل محاولة!"
          ],
          needsWork: [
            "💚 لا بأس {{name}}! التعلم رحلة - استمر في المحاولة!",
            "🌱 كل خطأ فرصة للتعلم {{name}}! أنت في الطريق الصحيح!"
          ]
        }}
      }},
      
      // تحديد مستوى الأداء
      getPerformanceLevel(percentage) {{
        if (percentage >= 90) return 'excellent';
        if (percentage >= 75) return 'good';
        if (percentage >= 60) return 'average';
        return 'needsWork';
      }},
      
      // اختيار رسالة عشوائية
      getRandomMessage(category, percentage = null) {{
        let messages = this.messages[category];
        if (percentage !== null && this.messages[category][this.getPerformanceLevel(percentage)]) {{
          messages = this.messages[category][this.getPerformanceLevel(percentage)];
        }}
        
        const randomMsg = messages[Math.floor(Math.random() * messages.length)];
        return randomMsg.replace('{{name}}', this.student?.name || 'البطل/ة');
      }},
      
      // عرض إشعار ذكي
      showSmart(category, options = {{}}) {{
        const message = this.getRandomMessage(category, options.percentage);
        
        Swal.fire({{
          title: options.title || 'رسالة ذكية 🤖',
          text: message,
          icon: options.icon || 'info',
          timer: options.timer || 3000,
          timerProgressBar: true,
          showConfirmButton: false,
          toast: options.toast || true,
          position: options.position || 'top-end',
          customClass: {{
            popup: 'animated-notification'
          }}
        }});
        
        // تشغيل صوت مناسب
        if (options.sound) {{
          SoundSystem.play(options.sound);
        }}
      }}
    }};
'''
    
    def extract_lesson_title(self, content):
        """استخراج عنوان الدرس من المحتوى"""
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1)
            # تنظيف العنوان
            title = re.sub(r'[🧪🔬📐✏️🧬⚛️🌱💊🫁🏠]', '', title).strip()
            return title
        return "الدرس"
    
    def enhance_javascript_functions(self, content):
        """تحسين دوال JavaScript الموجودة"""
        
        # تحسين دالة setStudent
        content = re.sub(
            r'function setStudent\(obj\)\s*{\s*localStorage\.setItem\(storageKey,\s*JSON\.stringify\(obj\)\);\s*}',
            '''function setStudent(obj){ 
      localStorage.setItem(storageKey, JSON.stringify(obj)); 
      NotificationSystem.student = obj;
    }''',
            content
        )
        
        # إضافة متغيرات التتبع
        content = re.sub(
            r'(const storageKey = "watyn_bio_student";)',
            r'''\1
    let consecutiveCorrect = 0; // متتبع الإجابات الصحيحة المتتالية
    let totalAnswered = 0; // إجمالي الأسئلة المجابة
''',
            content
        )
        
        return content
    
    def apply_sound_system_to_file(self, file_path):
        """تطبيق النظام الصوتي على ملف واحد"""
        print(f"🎵 معالجة: {file_path.relative_to(self.base_path)}")
        
        # قراءة المحتوى
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # فحص ما إذا كان النظام موجود بالفعل
        if self.check_if_already_has_sound_system(content):
            print(f"   ✅ النظام الصوتي موجود بالفعل - تخطي")
            return False
        
        # إنشاء نسخة احتياطية
        self.backup_file(file_path)
        
        # إضافة مكتبة Howler
        content = self.add_howler_library(content)
        
        # استخراج عنوان الدرس
        lesson_title = self.extract_lesson_title(content)
        
        # إضافة النظام الصوتي بعد AOS.init
        sound_system_code = self.get_sound_system_code(lesson_title)
        
        # البحث عن AOS.init وإضافة النظام بعده
        aos_pattern = r'(AOS\.init\(\s*{\s*duration:\s*\d+,\s*once:\s*true\s*}\s*\);)'
        replacement = r'\1' + sound_system_code
        
        if re.search(aos_pattern, content):
            content = re.sub(aos_pattern, replacement, content)
        else:
            # إذا لم نجد AOS، نضع النظام في بداية <script>
            script_pattern = r'(<script>\s*)'
            replacement = r'\1' + sound_system_code + '\n'
            content = re.sub(script_pattern, replacement, content)
        
        # تحسين دوال JavaScript الموجودة
        content = self.enhance_javascript_functions(content)
        
        # كتابة المحتوى المحدث
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ تم تطبيق النظام الصوتي بنجاح")
        return True
    
    def apply_to_all_lessons(self):
        """تطبيق النظام الصوتي على جميع الدروس"""
        print(f"🚀 بدء تطبيق النظام الصوتي والتفاعلي على {len(self.lessons_paths)} درس")
        print(f"⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        success_count = 0
        skip_count = 0
        
        for lesson_path in self.lessons_paths:
            try:
                if self.apply_sound_system_to_file(lesson_path):
                    success_count += 1
                else:
                    skip_count += 1
            except Exception as e:
                print(f"   ❌ خطأ: {str(e)}")
        
        print("="*60)
        print(f"📊 ملخص العملية:")
        print(f"   ✅ تم التطبيق على: {success_count} درس")
        print(f"   ⏭️  تم تخطي: {skip_count} درس (موجود مسبقاً)")
        print(f"   📝 إجمالي: {len(self.lessons_paths)} درس")
        print(f"🎉 تم الانتهاء بنجاح!")

def main():
    """الدالة الرئيسية"""
    base_path = r"c:\Users\ahm7d\Desktop\W"
    
    print("🎵 نظام تطبيق النظام الصوتي والتفاعلي المتقدم")
    print("=" * 60)
    
    applier = SoundSystemApplier(base_path)
    applier.apply_to_all_lessons()

if __name__ == "__main__":
    main()