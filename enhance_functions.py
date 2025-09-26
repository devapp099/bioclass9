#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام تحسين الدوال والتفاعل في الأنشطة التعليمية
تحسين دوال updateProgress, askStudent, resetQuiz وإضافة التفاعل الصوتي

المطور: مساعد GitHub Copilot
التاريخ: 2025/09/26
"""

import os
import re
from pathlib import Path
import shutil
from datetime import datetime

class JavaScriptEnhancer:
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
        backup_path = file_path.with_suffix('.html.backup2')
        shutil.copy2(file_path, backup_path)
        print(f"💾 تم إنشاء نسخة احتياطية: {backup_path.name}")
    
    def check_if_needs_enhancement(self, content):
        """فحص ما إذا كان الملف يحتاج تحسين"""
        return (
            "SoundSystem" in content and
            ("consecutiveCorrect" not in content or 
             "checkMilestones" not in content or
             "showSmart" not in content)
        )
    
    def enhance_ask_student_function(self, content):
        """تحسين دالة askStudent"""
        # البحث عن دالة askStudent البسيطة وتحسينها
        old_pattern = r'''async function askStudent\(\)\{
      const \{ value: formValues \} = await Swal\.fire\(\{
        title: '[^']+',
        html:
          `<div style="text-align:right">
            <div style="margin-bottom:\d+px;font-weight:\d+">أدخل بياناتك لبدء النشاط:</div>
            <input id="swal-name" class="swal2-input" placeholder="اسم الطالب/ـة">
            <input id="swal-class" class="swal2-input" placeholder="الصف \(مثال: التاسع/1\)">
          </div>`,
        focusConfirm: false,
        confirmButtonText: 'ابدأ',
        confirmButtonColor: '#d\d+',
        showCancelButton: true,
        cancelButtonText: 'إلغاء',
        preConfirm: \(\) => \{
          const name = document\.getElementById\('swal-name'\)\.value\?\.trim\(\);
          const klass = document\.getElementById\('swal-class'\)\.value\?\.trim\(\);
          if\(!name \|\| !klass\)\{
            Swal\.showValidationMessage\('يرجى إدخال الاسم والصف'\);
            return false;
          \}
          return \{ name, klass \};
        \}
      \}\);
      if\(formValues\)\{
        setStudent\(formValues\);
        updateMeta\(\);
        el\.quiz\.style\.display = "block";
        gsap\.from\("#quiz \.q", \{opacity:\d+, y:\d+, stagger:\.\d+, duration:\.\d+\}\);
      \}
    \}'''
        
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
        
        # البحث عن نمط أبسط
        simple_pattern = r'async function askStudent\(\)\{[^}]+\{[^}]+\}[^}]+\}'
        if re.search(simple_pattern, content, re.DOTALL):
            content = re.sub(simple_pattern, new_function, content, flags=re.DOTALL)
        
        return content
    
    def enhance_update_progress_function(self, content):
        """تحسين دالة updateProgress"""
        # البحث عن دالة updateProgress البسيطة
        old_pattern = r'''function updateProgress\(\)\{
      const total = document\.querySelectorAll\('\.q\[data-qid\]'\)\.length;
      const answered = Array\.from\(document\.querySelectorAll\('\.q'\)\)\.filter\(q => 
        q\.querySelector\('\.choice\.correct, \.choice\.wrong'\)
      \)\.length;
      el\.total\.textContent = total;
      el\.done\.textContent = answered;
      el\.bar\.style\.width = Math\.round\(\(answered/total\)\*100\) \+ '%';
    \}'''
        
        new_function = '''function updateProgress(){
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
          sound: null // الصوت يشتغل فوق
        });
        
        // تأثير بصري خاص للإنجازات
        gsap.fromTo('.progress', 
          { scale: 1 }, 
          { scale: 1.1, duration: 0.3, yoyo: true, repeat: 1 }
        );
      }
    }'''
        
        content = re.sub(old_pattern, new_function, content, flags=re.DOTALL)
        return content
    
    def enhance_click_handler(self, content):
        """تحسين معالج النقر على الأسئلة"""
        # البحث عن معالج النقر البسيط
        old_pattern = r'''document\.addEventListener\('click', \(e\)=>\{
      const choice = e\.target\.closest\('\.choice'\);
      if\(!choice\) return;
      const container = choice\.closest\('\.choices'\);
      container\.querySelectorAll\('\.choice'\)\.forEach\(c=> c\.classList\.remove\('correct','wrong'\)\);
      if\(choice\.dataset\.correct === "true"\)\{
        choice\.classList\.add\('correct'\);
        gsap\.fromTo\(choice, \{scale:1\}, \{scale:1\.\d+, y:-\d+, duration:\.\d+, yoyo:true, repeat:1\}\);
      \}else\{
        choice\.classList\.add\('wrong'\);
        gsap\.fromTo\(choice, \{x:0\}, \{x:-\d+, duration:\.\d+, yoyo:true, repeat:\d+\}\);
      \}
      updateProgress\(\);
    \}\);'''
        
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
          consecutiveCorrect = 0; // إعادة تعيين العداد
        }
        
      } else {
        choice.classList.add('wrong');
        consecutiveCorrect = 0; // إعادة تعيين العداد للإجابات الصحيحة
        
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
        
        content = re.sub(old_pattern, new_handler, content, flags=re.DOTALL)
        return content
    
    def enhance_celebrate_function(self, content):
        """تحسين دالة الاحتفال"""
        old_pattern = r'''function celebrate\(\)\{
      const duration = \d+; const end = Date\.now\(\) \+ duration;
      \(function frame\(\)\{
        confetti\(\{ particleCount: \d+, angle: \d+, spread: \d+, origin: \{ x: 0 \} \}\);
        confetti\(\{ particleCount: \d+, angle: \d+, spread: \d+, origin: \{ x: 1 \} \}\);
        if \(Date\.now\(\) < end\) requestAnimationFrame\(frame\);
      \}\)\(\);
    \}'''
        
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
        # البحث عن معالج زر الإرسال البسيط
        old_pattern = r'''el\.submit\.addEventListener\('click', \(\)=>\{
      const s = getStudent\(\);
      const \{ correct, total, percent \} = computeScore\(\);
      celebrate\(\);
      Swal\.fire\(\{
        title: '[^']+',
        html: `[^`]+`,
        icon: 'success',
        confirmButtonText: '[^']+',
        confirmButtonColor: '[^']+',
        showDenyButton: true,
        denyButtonText: '[^']+',
        denyButtonColor: '[^']+'
      \}\.then\(res=>\{ if\(res\.isConfirmed\) resetQuiz\(\); \}\);
    \}\);'''
        
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
          window.location.href='https://devapp099.github.io/watyn-bio-activities-/index.html'; 
        }
      });
    });'''
        
        content = re.sub(old_pattern, new_handler, content, flags=re.DOTALL)
        return content
    
    def enhance_reset_function(self, content):
        """تحسين دالة إعادة التعيين"""
        old_pattern = r'''function resetQuiz\(\)\{
      document\.querySelectorAll\('\.choice'\)\.forEach\(c=> c\.classList\.remove\('correct','wrong'\)\);
      gsap\.from\("#quiz \.q", \{opacity:\d+, y:\d+, stagger:\.\d+, duration:\.\d+\}\);
      window\.scrollTo\(\{ top:\d+, behavior:'smooth' \}\);
      updateProgress\(\);
    \}'''
        
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
        """إضافة تحسينات أخيرة"""
        # إضافة أصوات للأزرار والرسالة الترحيبية في نهاية السكريبت
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
        
        return content
    
    def enhance_file(self, file_path):
        """تحسين ملف واحد"""
        print(f"🔧 تحسين: {file_path.relative_to(self.base_path)}")
        
        # قراءة المحتوى
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # فحص ما إذا كان الملف يحتاج تحسين
        if not self.check_if_needs_enhancement(content):
            print(f"   ⏭️  لا يحتاج تحسين أو محسن بالفعل")
            return False
        
        # إنشاء نسخة احتياطية
        self.backup_file(file_path)
        
        original_content = content
        
        # تطبيق التحسينات
        content = self.enhance_ask_student_function(content)
        content = self.enhance_update_progress_function(content)
        content = self.enhance_click_handler(content)
        content = self.enhance_celebrate_function(content)
        content = self.enhance_submit_handler(content)
        content = self.enhance_reset_function(content)
        content = self.add_final_enhancements(content)
        
        # كتابة المحتوى المحدث
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        if content != original_content:
            print(f"   ✅ تم التحسين بنجاح")
            return True
        else:
            print(f"   ⚠️  لم يتم إجراء تغييرات")
            return False
    
    def enhance_all_lessons(self):
        """تحسين جميع الدروس"""
        print(f"🚀 بدء تحسين الدوال والتفاعل في {len(self.lessons_paths)} درس")
        print(f"⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        success_count = 0
        skip_count = 0
        
        for lesson_path in self.lessons_paths:
            try:
                if self.enhance_file(lesson_path):
                    success_count += 1
                else:
                    skip_count += 1
            except Exception as e:
                print(f"   ❌ خطأ: {str(e)}")
        
        print("="*60)
        print(f"📊 ملخص العملية:")
        print(f"   ✅ تم التحسين: {success_count} درس")
        print(f"   ⏭️  تم تخطي: {skip_count} درس")
        print(f"   📝 إجمالي: {len(self.lessons_paths)} درس")
        print(f"🎉 تم الانتهاء من التحسين بنجاح!")

def main():
    """الدالة الرئيسية"""
    base_path = r"c:\Users\ahm7d\Desktop\W"
    
    print("🔧 نظام تحسين الدوال والتفاعل في الأنشطة التعليمية")
    print("=" * 60)
    
    enhancer = JavaScriptEnhancer(base_path)
    enhancer.enhance_all_lessons()

if __name__ == "__main__":
    main()