#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح شامل ونهائي للنظام الصوتي والتفاعلي
إزالة التكرارات وتطبيق النظام بشكل موحد على جميع الدروس

المطور: مساعد GitHub Copilot
التاريخ: 2025/09/26
"""

import os
import re
from pathlib import Path
import shutil
from datetime import datetime

class CompleteSoundSystemFixer:
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
        backup_path = file_path.with_suffix('.html.backup_final')
        shutil.copy2(file_path, backup_path)
        print(f"💾 تم إنشاء نسخة احتياطية: {backup_path.name}")
    
    def extract_lesson_title(self, content):
        """استخراج عنوان الدرس من المحتوى"""
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1)
            # تنظيف العنوان
            title = re.sub(r'[🧪🔬📐✏️🧬⚛️🌱💊🫁🏠]', '', title).strip()
            return title
        return "الدرس"
    
    def get_complete_sound_system_code(self, lesson_title="الدرس"):
        """الحصول على النظام الصوتي الكامل والمحسن"""
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

    const storageKey = "watyn_bio_student";
    let consecutiveCorrect = 0; // متتبع الإجابات الصحيحة المتتالية
    let totalAnswered = 0; // إجمالي الأسئلة المجابة

    function getStudent(){{ try{{ return JSON.parse(localStorage.getItem(storageKey)) || null }}catch{{ return null }} }}
    function setStudent(obj){{ 
      localStorage.setItem(storageKey, JSON.stringify(obj)); 
      NotificationSystem.student = obj;
    }}
'''
    
    def clean_existing_sound_system(self, content):
        """إزالة أي نظام صوتي موجود مسبقاً لتجنب التكرار"""
        # إزالة النظام الصوتي المكرر
        content = re.sub(r'// 🎵 نظام صوتي ذكي متقدم.*?}};', '', content, flags=re.DOTALL)
        content = re.sub(r'// 🔔 نظام الإشعارات والرسائل التفاعلية الذكي.*?}};', '', content, flags=re.DOTALL)
        content = re.sub(r'const SoundSystem = \{.*?\};', '', content, flags=re.DOTALL)
        content = re.sub(r'const NotificationSystem = \{.*?\};', '', content, flags=re.DOTALL)
        
        # إزالة المتغيرات المكررة
        content = re.sub(r'let consecutiveCorrect = 0;.*?let totalAnswered = 0;', '', content, flags=re.DOTALL)
        
        # تنظيف دالة setStudent المكررة
        content = re.sub(r'function setStudent\(obj\)\{ \s*localStorage\.setItem\(storageKey,\s*JSON\.stringify\(obj\)\);\s*NotificationSystem\.student = obj;\s*\}', '', content, flags=re.DOTALL)
        
        return content
    
    def ensure_howler_library(self, content):
        """التأكد من وجود مكتبة Howler"""
        if "howler" not in content.lower():
            # البحث عن نهاية المكتبات الحالية
            pattern = r'(<script src="https://cdn\.jsdelivr\.net/npm/aos@2\.3\.4/dist/aos\.js"></script>)'
            replacement = r'\1\n  <script src="https://cdn.jsdelivr.net/npm/howler@2.2.4/dist/howler.min.js"></script>'
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def fix_lesson_completely(self, file_path):
        """إصلاح درس واحد بشكل كامل ونهائي"""
        print(f"🔧 إصلاح شامل: {file_path.relative_to(self.base_path)}")
        
        # قراءة المحتوى
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # إنشاء نسخة احتياطية
        self.backup_file(file_path)
        
        # استخراج عنوان الدرس
        lesson_title = self.extract_lesson_title(content)
        
        # إضافة مكتبة Howler إذا لم تكن موجودة
        content = self.ensure_howler_library(content)
        
        # إزالة أي نظام صوتي موجود مسبقاً
        content = self.clean_existing_sound_system(content)
        
        # إضافة النظام الصوتي الكامل الجديد
        sound_system_code = self.get_complete_sound_system_code(lesson_title)
        
        # البحث عن AOS.init وإضافة النظام بعده
        aos_pattern = r'(AOS\.init\(\s*\{[^}]*\}\s*\);)'
        if re.search(aos_pattern, content):
            content = re.sub(aos_pattern, r'\1' + sound_system_code, content)
        else:
            # إذا لم نجد AOS، نضع النظام في بداية <script>
            script_pattern = r'(<script>\s*)'
            content = re.sub(script_pattern, r'\1' + sound_system_code + '\n', content)
        
        # إصلاح وتحسين الدوال الموجودة
        content = self.enhance_all_functions(content)
        
        # كتابة المحتوى المحسن
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ تم الإصلاح الشامل بنجاح")
        return True
    
    def enhance_all_functions(self, content):
        """تحسين جميع الدوال في الملف"""
        
        # تحسين دالة askStudent
        content = self.enhance_ask_student_function(content)
        
        # تحسين دالة updateProgress
        content = self.enhance_update_progress_function(content)
        
        # تحسين معالج النقر
        content = self.enhance_click_handler(content)
        
        # تحسين دالة الاحتفال
        content = self.enhance_celebrate_function(content)
        
        # تحسين معالج الإرسال
        content = self.enhance_submit_handler(content)
        
        # تحسين دالة إعادة التعيين
        content = self.enhance_reset_function(content)
        
        # إضافة التحسينات الأخيرة
        content = self.add_final_enhancements(content)
        
        return content
    
    def enhance_ask_student_function(self, content):
        """تحسين دالة askStudent"""
        # نمط مرن للعثور على الدالة
        old_pattern = r'async function askStudent\(\)\{[^}]*\{[^}]*\}[^}]*\}'
        
        new_function = '''async function askStudent(){
      SoundSystem.play('start');
      
      const { value: formValues } = await Swal.fire({
        title: 'مرحبًا في عالم العلوم! 🧬',
        html:
          `<div style="text-align:right">
            <div style="margin-bottom:12px;font-weight:700;color:#d97706">أدخل بياناتك لتبدأ رحلتك العلمية:</div>
            <input id="swal-name" class="swal2-input" placeholder="اسم الطالب/ـة" style="text-align:right">
            <input id="swal-class" class="swal2-input" placeholder="الصف (مثال: التاسع/1)" style="text-align:right">
            <div style="font-size:13px;color:#6b7280;margin-top:8px">
              💡 سيتم استخدام اسمك لإرسال رسائل تشجيعية مخصصة!
            </div>
          </div>`,
        focusConfirm: false,
        confirmButtonText: '🚀 ابدأ المغامرة',
        confirmButtonColor: '#d97706',
        showCancelButton: true,
        cancelButtonText: 'إلغاء',
        preConfirm: () => {
          const name = document.getElementById('swal-name').value?.trim();
          const klass = document.getElementById('swal-class').value?.trim();
          if(!name || !klass){
            Swal.showValidationMessage('يرجى إدخال الاسم والصف');
            return false;
          }
          return { name, klass };
        }
      });
      
      if(formValues){
        setStudent(formValues);
        updateMeta();
        
        // رسالة ترحيب ذكية
        setTimeout(() => {
          NotificationSystem.showSmart('welcome', {
            title: 'أهلاً وسهلاً! 👋',
            icon: 'success',
            timer: 4000,
            sound: 'select'
          });
        }, 500);
        
        el.quiz.style.display = "block";
        gsap.from("#quiz .q", {opacity:0, y:20, stagger:.08, duration:.6});
      }
    }'''
        
        if re.search(old_pattern, content, re.DOTALL):
            content = re.sub(old_pattern, new_function, content, flags=re.DOTALL)
        
        return content
    
    def enhance_update_progress_function(self, content):
        """تحسين دالة updateProgress مع إضافة checkMilestones"""
        
        new_functions = '''function updateProgress(){
      const total = document.querySelectorAll('.q[data-qid]').length;
      const answered = Array.from(document.querySelectorAll('.q')).filter(q => 
        q.querySelector('.choice.correct, .choice.wrong')
      ).length;
      const oldProgress = parseInt(el.done.textContent) || 0;
      
      el.total.textContent = total;
      el.done.textContent = answered;
      const pc = Math.round((answered / total) * 100);
      
      // تأثير بصري لشريط التقدم مع صوت
      gsap.to(el.bar, {
        width: pc + "%",
        duration: 0.5,
        ease: "power2.out",
        onComplete: () => {
          if (answered > oldProgress) {
            SoundSystem.play('progress');
          }
        }
      });
      
      // إشعارات عند النقاط المهمة
      if (answered > oldProgress) {
        checkMilestones(pc, answered, total);
      }
    }
    
    // فحص النقاط المهمة في التقدم
    function checkMilestones(percentage, questionCount, totalQuestions) {
      const milestones = [25, 50, 75, 100];
      const reached = milestones.find(m => percentage >= m && (percentage - 5) < m);
      
      if (reached && questionCount === Math.ceil(totalQuestions * reached / 100)) {
        SoundSystem.play('milestone');
        NotificationSystem.showSmart('milestone', {
          title: 'إنجاز رائع! 🎯',
          icon: 'success',
          timer: 4000,
          percentage: reached,
          sound: null
        });
        
        // تأثير بصري خاص للإنجازات
        gsap.fromTo('.progress', 
          { scale: 1 }, 
          { scale: 1.1, duration: 0.3, yoyo: true, repeat: 1 }
        );
      }
    }'''
        
        # البحث عن دالة updateProgress وإزالتها
        old_pattern = r'function updateProgress\(\)\{[^}]*(?:\{[^}]*\}[^}]*)*\}'
        content = re.sub(old_pattern, '', content, flags=re.DOTALL)
        
        # البحث عن checkMilestones وإزالتها إذا كانت موجودة
        milestone_pattern = r'function checkMilestones\([^}]*(?:\{[^}]*\}[^}]*)*\}'
        content = re.sub(milestone_pattern, '', content, flags=re.DOTALL)
        
        # إضافة الدوال الجديدة قبل معالج النقر
        click_pattern = r'(document\.addEventListener\(\'click\')'
        content = re.sub(click_pattern, new_functions + r'\n    \1', content)
        
        return content
    
    def enhance_click_handler(self, content):
        """تحسين معالج النقر"""
        # إزالة معالج النقر القديم
        old_pattern = r'document\.addEventListener\(\'click\', \(e\)=>\{[^}]*(?:\{[^}]*\}[^}]*)*\}\);'
        content = re.sub(old_pattern, '', content, flags=re.DOTALL)
        
        new_handler = '''// نظام الإجابة المحسن مع الذكاء الاصطناعي
    document.addEventListener('click', (e)=>{
      const choice = e.target.closest('.choice');
      if(!choice) return;
      
      // تشغيل صوت النقر
      SoundSystem.play('click');
      
      const container = choice.closest('.choices');
      const wasAnswered = container.querySelector('.choice.correct, .choice.wrong');
      
      // منع إعادة الإجابة على نفس السؤال
      if (wasAnswered) return;
      
      container.querySelectorAll('.choice').forEach(c=> c.classList.remove('correct','wrong'));
      
      totalAnswered++;
      
      if(choice.dataset.correct === "true"){
        choice.classList.add('correct');
        consecutiveCorrect++;
        
        SoundSystem.play('correct');
        
        // تأثير بصري للإجابة الصحيحة
        gsap.fromTo(choice, 
          {scale:1, backgroundColor: 'rgba(52,211,153,.10)'}, 
          {scale:1.05, y:-4, duration:.3, yoyo:true, repeat:1, ease: "back.out(1.7)"}
        );
        
        // رسائل تشجيع ذكية حسب الأداء
        if (consecutiveCorrect >= 5) {
          NotificationSystem.showSmart('encouragement', {
            title: 'أداء استثنائي! 🔥',
            icon: 'success',
            timer: 2500
          });
          consecutiveCorrect = 0;
        }
        
      } else {
        choice.classList.add('wrong');
        consecutiveCorrect = 0;
        
        SoundSystem.play('wrong');
        
        // تأثير بصري للإجابة الخاطئة
        gsap.fromTo(choice, 
          {x:0}, 
          {x:-8, duration:.08, yoyo:true, repeat:6, ease: "power2.inOut"}
        );
        
        // رسائل تحفيز ذكية
        if (totalAnswered >= 3) {
          setTimeout(() => {
            NotificationSystem.showSmart('motivation', {
              title: 'استمر في المحاولة! 💪',
              icon: 'info',
              timer: 2500
            });
          }, 1000);
        }
      }
      
      updateProgress();
    });

    // إضافة أصوات للأزرار وتأثيرات تفاعلية
    document.addEventListener('DOMContentLoaded', () => {
      document.querySelectorAll('.choice').forEach(choice => {
        choice.addEventListener('mouseenter', () => {
          SoundSystem.play('select');
        });
      });
    });'''
        
        # إضافة المعالج الجديد
        content += '\n' + new_handler
        
        return content
    
    def enhance_celebrate_function(self, content):
        """تحسين دالة الاحتفال"""
        old_pattern = r'function celebrate\(\)\{[^}]*(?:\{[^}]*\}[^}]*)*\}'
        
        new_function = '''function celebrate(){
      // احتفال متقدم مع أصوات متعددة
      SoundSystem.playSequence(['celebration', 'firework'], 500);
      
      const duration = 2500; 
      const end = Date.now() + duration;
      
      // تأثيرات الكونفيتي المحسنة
      (function frame(){
        confetti({ 
          particleCount: 5, 
          angle: 60, 
          spread: 80, 
          origin: { x: 0 },
          colors: ['#f59e0b', '#10b981', '#3b82f6', '#ef4444', '#8b5cf6']
        });
        confetti({ 
          particleCount: 5, 
          angle: 120, 
          spread: 80, 
          origin: { x: 1 },
          colors: ['#f59e0b', '#10b981', '#3b82f6', '#ef4444', '#8b5cf6']
        });
        if (Date.now() < end) requestAnimationFrame(frame);
      })();
      
      // تأثير بصري للشاشة كاملة
      gsap.fromTo('body', 
        {backgroundColor: 'transparent'}, 
        {backgroundColor: 'rgba(245,158,11,0.1)', duration: 0.5, yoyo: true, repeat: 1}
      );
    }'''
        
        content = re.sub(old_pattern, new_function, content, flags=re.DOTALL)
        return content
    
    def enhance_submit_handler(self, content):
        """تحسين معالج زر الإرسال"""
        # البحث عن معالج الإرسال وإزالته
        old_pattern = r'el\.submit\.addEventListener\(\'click\', \(\)=>\{[^}]*(?:\{[^}]*\}[^}]*)*\}\);'
        content = re.sub(old_pattern, '', content, flags=re.DOTALL)
        
        new_handler = '''el.submit.addEventListener('click', ()=>{
      const s = getStudent();
      const { correct, total, percent } = computeScore();
      
      celebrate();
      
      // رسالة نتائج ذكية مخصصة
      const performanceLevel = NotificationSystem.getPerformanceLevel(percent);
      const smartMessage = NotificationSystem.getRandomMessage('finalResults', percent);
      
      let resultIcon = 'success';
      let resultColor = '#10b981';
      
      if (percent < 60) {
        resultIcon = 'info';
        resultColor = '#3b82f6';
      }
      
      Swal.fire({
        title: `${performanceLevel === 'excellent' ? '🏆' : performanceLevel === 'good' ? '⭐' : performanceLevel === 'average' ? '👍' : '💪'} النتائج النهائية`,
        html: `
          <div style="text-align:right;line-height:2.2;padding:10px">
            <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);padding:15px;border-radius:12px;margin-bottom:15px">
              <div><strong>👤 الاسم:</strong> ${s?.name || '-'}</div>
              <div><strong>🏫 الصف:</strong> ${s?.klass || '-'}</div>
            </div>
            <div style="background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);padding:15px;border-radius:12px;margin-bottom:15px">
              <div><strong>📊 النتيجة:</strong> ${correct} من ${total} سؤال</div>
              <div><strong>📈 النسبة المئوية:</strong> <span style="color:#059669;font-size:18px;font-weight:900">${percent}%</span></div>
            </div>
            <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);padding:15px;border-radius:12px;font-weight:600;color:#92400e">
              ${smartMessage}
            </div>
          </div>`,
        icon: resultIcon,
        confirmButtonText: '🔄 إعادة المحاولة',
        confirmButtonColor: resultColor,
        showDenyButton: true,
        denyButtonText: '🏠 العودة للرئيسية',
        denyButtonColor: '#d97706'
      }).then(res=>{ 
        if(res.isConfirmed) {
          resetQuiz(); 
        } else {
          window.location.href='https://devapp099.github.io/bioclass9/'; 
        }
      });
    });'''
        
        # إضافة المعالج الجديد
        content += '\n' + new_handler
        
        return content
    
    def enhance_reset_function(self, content):
        """تحسين دالة إعادة التعيين"""
        old_pattern = r'function resetQuiz\(\)\{[^}]*(?:\{[^}]*\}[^}]*)*\}'
        
        new_function = '''function resetQuiz(){
      SoundSystem.play('reset');
      
      // إعادة تعيين المتغيرات
      consecutiveCorrect = 0;
      totalAnswered = 0;
      
      document.querySelectorAll('.choice').forEach(c=> c.classList.remove('correct','wrong'));
      updateProgress();
      
      gsap.from("#quiz .q", {opacity:0, y:15, stagger:.06, duration:.5});
      window.scrollTo({ top:0, behavior:'smooth' });
      
      // رسالة تحفيز لإعادة المحاولة
      setTimeout(() => {
        NotificationSystem.showSmart('encouragement', {
          title: 'بداية جديدة! 🌟',
          icon: 'info',
          timer: 2000
        });
      }, 1000);
    }'''
        
        content = re.sub(old_pattern, new_function, content, flags=re.DOTALL)
        return content
    
    def add_final_enhancements(self, content):
        """إضافة التحسينات الأخيرة"""
        final_additions = '''
    el.reset.addEventListener('click', resetQuiz);

    // إضافة أصوات للأزرار
    [el.start, el.submit, el.reset].forEach(btn => {
      if (btn) {
        btn.addEventListener('mouseenter', () => SoundSystem.play('select'));
        btn.addEventListener('click', () => SoundSystem.play('click'));
      }
    });

    // رسالة ترحيب عامة عند تحميل الصفحة
    setTimeout(() => {
      const student = getStudent();
      if (student) {
        NotificationSystem.student = student;
        NotificationSystem.showSmart('welcome', {
          title: 'مرحباً بعودتك! 👋',
          timer: 3000,
          sound: 'select'
        });
      }
    }, 1000);'''
        
        # البحث عن نهاية السكريبت وإضافة التحسينات
        end_pattern = r'(updateMeta\(\);[^<]*</script>)'
        replacement = r'updateMeta();\n    updateProgress();' + final_additions + '\n  </script>'
        
        if re.search(end_pattern, content, re.DOTALL):
            content = re.sub(end_pattern, replacement, content, flags=re.DOTALL)
        else:
            # إذا لم نجد النمط، نضيف في النهاية
            content = content.replace('</script>', final_additions + '\n  </script>')
        
        return content
    
    def fix_all_lessons(self):
        """إصلاح جميع الدروس بشكل شامل"""
        print(f"🚀 بدء الإصلاح الشامل للنظام الصوتي والتفاعلي")
        print(f"📊 إجمالي الدروس: {len(self.lessons_paths)}")
        print(f"⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        success_count = 0
        
        for lesson_path in self.lessons_paths:
            try:
                if self.fix_lesson_completely(lesson_path):
                    success_count += 1
            except Exception as e:
                print(f"   ❌ خطأ: {str(e)}")
        
        print("="*70)
        print(f"🎉 تم الإصلاح بنجاح!")
        print(f"   ✅ تم إصلاح: {success_count} درس")
        print(f"   📝 إجمالي: {len(self.lessons_paths)} درس")
        print(f"🎵 النظام الصوتي والإشعارات الذكية مفعلة على جميع الدروس!")

def main():
    """الدالة الرئيسية"""
    base_path = r"c:\Users\ahm7d\Desktop\W"
    
    print("🔧 الإصلاح الشامل والنهائي للنظام الصوتي والتفاعلي")
    print("=" * 70)
    
    fixer = CompleteSoundSystemFixer(base_path)
    fixer.fix_all_lessons()

if __name__ == "__main__":
    main()