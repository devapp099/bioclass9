#!/usr/bin/env python3
"""
إصلاح مشكلة إخفاء المحتوى وتوحيد الأنظمة
"""
import os
import re
from pathlib import Path

def fix_hidden_content(lesson_path):
    """إصلاح مشكلة المحتوى المخفي"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lesson_name = str(lesson_path).split(os.sep)[-2]
        
        # تخطي lesson-1-1 لأنه يعمل بشكل مثالي
        if 'lesson-1-1' in str(lesson_path):
            return True
        
        # إزالة الكود المكرر والمتضارب
        # البحث عن تعريفات متعددة لنفس الوظائف
        content = re.sub(r'async function askStudent\(\)\{[^}]*\}[^}]*\}', '', content, flags=re.DOTALL)
        
        # إزالة تعريفات el المكررة
        content = re.sub(r'const el = \{[^}]*\};', '', content)
        
        # إزالة storageKey المكرر
        content = re.sub(r'const storageKey = "watyn_bio_student";', '', content)
        
        # إضافة نظام موحد وبسيط في نهاية الـ script
        unified_system = '''
    // النظام الموحد والبسيط
    const elements = {
      start: document.getElementById('btnStart'),
      quiz: document.getElementById('quiz'),
      submit: document.getElementById('btnSubmit'),
      reset: document.getElementById('btnReset'),
      studentMeta: document.getElementById('studentMeta')
    };

    const storageKey = "watyn_bio_student";

    function getStudent() {
      try {
        return JSON.parse(localStorage.getItem(storageKey));
      } catch {
        return null;
      }
    }

    function setStudent(data) {
      localStorage.setItem(storageKey, JSON.stringify(data));
    }

    function updateStudentDisplay() {
      const student = getStudent();
      if (elements.studentMeta && student) {
        elements.studentMeta.textContent = `الطالب/ـة: ${student.name} — الصف: ${student.klass}`;
      }
    }

    async function startQuiz() {
      SoundSystem.play('start');
      
      const { value: formValues } = await Swal.fire({
        title: 'بيانات الطالب',
        html: `
          <div style="text-align:right">
            <input id="swal-name" class="swal2-input" placeholder="اسم الطالب/ـة" value="">
            <input id="swal-class" class="swal2-input" placeholder="الصف" value="">
          </div>`,
        focusConfirm: false,
        confirmButtonText: 'ابدأ النشاط',
        showCancelButton: true,
        cancelButtonText: 'إلغاء',
        preConfirm: () => {
          const name = document.getElementById('swal-name').value.trim();
          const klass = document.getElementById('swal-class').value.trim();
          if (!name || !klass) {
            Swal.showValidationMessage('يرجى إدخال الاسم والصف');
            return false;
          }
          return { name, klass };
        }
      });

      if (formValues) {
        setStudent(formValues);
        updateStudentDisplay();
        SmartNotifications.showWelcome(formValues.name);
        
        // إظهار منطقة الأسئلة
        if (elements.quiz) {
          elements.quiz.style.display = 'block';
          if (typeof gsap !== 'undefined') {
            gsap.from("#quiz .q", {opacity:0, y:20, stagger:0.1, duration:0.6});
          }
        }
      }
    }

    function computeScore() {
      const questions = document.querySelectorAll('.q[data-qid]');
      let correct = 0;
      
      questions.forEach(q => {
        const correctChoice = q.querySelector('.choice.correct');
        if (correctChoice) correct++;
      });
      
      return { correct, total: questions.length };
    }

    function resetQuiz() {
      document.querySelectorAll('.choice').forEach(choice => {
        choice.classList.remove('correct', 'wrong');
      });
      
      if (typeof gsap !== 'undefined') {
        gsap.from("#quiz .q", {opacity:0, y:20, stagger:0.05, duration:0.5});
      }
      
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function submitQuiz() {
      const student = getStudent();
      const { correct, total } = computeScore();
      
      if (typeof confetti !== 'undefined') {
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 }
        });
      }
      
      SmartNotifications.showResult(correct, total, student?.name || 'الطالب/ة');
    }

    // ربط الأحداث
    document.addEventListener('DOMContentLoaded', function() {
      // تهيئة النظام الصوتي
      if (typeof Howl !== 'undefined') {
        SoundSystem.init();
      }
      
      // تهيئة AOS
      if (typeof AOS !== 'undefined') {
        AOS.init({
          duration: 800,
          easing: 'ease-out-cubic',
          once: true
        });
      }
      
      // ربط الأحداث
      if (elements.start) {
        elements.start.addEventListener('click', startQuiz);
      }
      
      if (elements.submit) {
        elements.submit.addEventListener('click', submitQuiz);
      }
      
      if (elements.reset) {
        elements.reset.addEventListener('click', resetQuiz);
      }
      
      // تحديث عرض الطالب
      updateStudentDisplay();
      
      // تهيئة شريط التقدم
      updateProgress();
      
      console.log('✅ تم تحميل جميع الأنظمة بنجاح');
    });'''
        
        # إضافة النظام الموحد قبل إغلاق script
        script_end_pattern = r'(\s*</script>\s*</body>)'
        content = re.sub(script_end_pattern, f'{unified_system}\\1', content, flags=re.DOTALL)
        
        # كتابة الملف المحدث
        with open(lesson_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"  ❌ خطأ: {str(e)}")
        return False

def main():
    print("🔧 إصلاح مشكلة المحتوى المخفي")
    print("=" * 50)
    
    # العثور على جميع الدروس
    lessons = []
    units = ['unit-1-cells', 'unit-2-transport', 'unit-3-biomolecules', 
             'unit-4-nutrition', 'unit-5-respiration', 'unit-6-homeostasis']
    
    for unit in units:
        if os.path.exists(unit):
            for lesson_dir in os.listdir(unit):
                if lesson_dir.startswith('lesson-'):
                    lesson_path = Path(unit) / lesson_dir / 'index.html'
                    if lesson_path.exists():
                        lessons.append((f"{unit}/{lesson_dir}", lesson_path))
    
    print(f"📚 تم العثور على {len(lessons)} درس")
    print()
    
    success_count = 0
    for lesson_name, lesson_path in lessons:
        print(f"🔧 معالجة: {lesson_name}")
        if fix_hidden_content(lesson_path):
            success_count += 1
            print(f"  ✅ تم الإصلاح")
        else:
            print(f"  ❌ فشل")
    
    print("\n" + "=" * 50)
    print(f"📊 النتائج:")
    print(f"✅ تم الإصلاح: {success_count} درس")
    print(f"❌ فشل: {len(lessons) - success_count} درس")

if __name__ == "__main__":
    main()