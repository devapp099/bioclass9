#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def fix_javascript_structure(lesson_path):
    """إصلاح هيكل JavaScript المكسور"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # البحث عن قسم JavaScript الرئيسي
        main_script_pattern = r'<script>(.*?)</script>'
        scripts = re.findall(main_script_pattern, content, re.DOTALL)
        
        if len(scripts) < 2:
            return False, "هيكل غير متوقع للملف"
        
        # أخذ الجزء الأول من الملف حتى </head>
        head_end = content.find('</head>')
        if head_end == -1:
            return False, "لم يتم العثور على </head>"
        
        head_section = content[:head_end]
        
        # البحث عن قسم body
        body_start = content.find('<body>')
        if body_start == -1:
            return False, "لم يتم العثور على <body>"
        
        body_end = content.find('</body>')
        if body_end == -1:
            return False, "لم يتم العثور على </body>"
        
        body_section = content[body_start:body_end + 7]
        
        # إنشاء JavaScript صحيح - أستخدم درس يعمل كمرجع
        working_js = '''
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
            onloaderror: (id, error) => {
              console.warn(`⚠️ فشل تحميل الصوت ${type}: ${error}`);
            }
          });
        });
        
        console.log('🎵 تم تهيئة النظام الصوتي');
      },
      
      play(soundType) {
        if (!this.enabled || !this.sounds[soundType]) return;
        try {
          this.sounds[soundType].play();
        } catch (error) {
          console.error(`خطأ في تشغيل الصوت ${soundType}:`, error);
        }
      },
      
      getContextualVolume(soundType) {
        const contextMap = {
          'celebration': 0.9,
          'milestone': 0.8,
          'correct': 0.7,
          'welcome': 0.6,
          'wrong': 0.5,
          'progress': 0.4,
          'click': 0.4,
          'select': 0.3
        };
        return contextMap[soundType] || this.currentVolume;
      }
    };

    const el = {
      start: document.getElementById('btnStart'),
      quiz: document.getElementById('quiz'),
      submit: document.getElementById('btnSubmit'),
      reset: document.getElementById('btnReset'),
      meta: document.getElementById('studentMeta'),
      bar: document.getElementById('barFill'),
      done: document.getElementById('countDone'),
      total: document.getElementById('countTotal')
    };

    const storageKey = "watyn_bio_student";
    let totalAnswered = 0;
    let consecutiveCorrect = 0;
    let startTime = Date.now();
    
    function getStudent(){ 
      try{ 
        return JSON.parse(localStorage.getItem(storageKey)) || null;
      } catch { 
        return null;
      } 
    }
    
    function setStudent(obj){ 
      localStorage.setItem(storageKey, JSON.stringify(obj)); 
    }

    function getPerformanceLevel(percentage) {
      if (percentage >= 90) return 'excellent';
      if (percentage >= 75) return 'good';
      if (percentage >= 60) return 'average';
      return 'needsWork';
    }

    function getFinalResultMessage(percentage, studentName) {
      const name = studentName || 'البطل/ة';
      const messages = {
        excellent: [`🏆 مبروك ${name}! أداء استثنائي!`],
        good: [`👏 أحسنت ${name}! أداء جيد جداً!`],
        average: [`📚 أداء جيد ${name}! مراجعة بسيطة وستكون في القمة!`],
        needsWork: [`💚 لا بأس ${name}! استمر في المحاولة!`]
      };
      
      const level = getPerformanceLevel(percentage);
      const levelMessages = messages[level];
      return levelMessages[Math.floor(Math.random() * levelMessages.length)];
    }

    function showEncouragementMessage(type) {
      const s = getStudent();
      const name = s?.name || 'البطل/ة';
      
      const messages = {
        correct: [`ممتاز ${name}! إجابة صحيحة رائعة! 🌟`],
        wrong: [`لا بأس ${name}، المحاولة جزء من التعلم! 💪`]
      };
      
      const messageList = messages[type] || messages['correct'];
      const randomMessage = messageList[Math.floor(Math.random() * messageList.length)];
      
      Swal.fire({
        title: type === 'correct' ? 'رائع! 🌟' : 'لا بأس! 💪',
        text: randomMessage,
        icon: type === 'correct' ? 'success' : 'info',
        timer: 3000,
        timerProgressBar: true,
        toast: true,
        position: 'top-end',
        showConfirmButton: false
      });
    }

    async function askStudent(){
      const { value: formValues } = await Swal.fire({
        title: 'مرحبًا 👋',
        html: `<div style="text-align:right">
          <div style="margin-bottom:8px;font-weight:700">أدخل بياناتك لبدء النشاط:</div>
          <input id="swal-name" class="swal2-input" placeholder="اسم الطالب/ـة">
          <input id="swal-class" class="swal2-input" placeholder="الصف (مثال: التاسع/1)">
        </div>`,
        focusConfirm: false,
        confirmButtonText: 'ابدأ',
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
        SoundSystem.play('start');
        
        el.quiz.style.display = "block";
        gsap.from("#quiz .q", {opacity:0, y:10, stagger:.08, duration:.5});
        
        totalAnswered = 0;
        consecutiveCorrect = 0;
        startTime = Date.now();
      }
    }

    function updateMeta(){
      const s = getStudent();
      el.meta.textContent = s ? (`الطالب/ـة: ${s.name} — الصف: ${s.klass}`) : "مرحبًا! لنبدأ…";
    }

    function updateProgress(){
      const total = document.querySelectorAll('.q[data-qid]').length;
      const answered = Array.from(document.querySelectorAll('.q')).filter(q => 
        q.querySelector('.choice.correct, .choice.wrong')
      ).length;
      
      el.total.textContent = total;
      el.done.textContent = answered;
      const percentage = Math.round((answered/total)*100);
      el.bar.style.width = percentage + '%';
      
      if (answered > 0) {
        SoundSystem.play('progress');
      }
    }

    function computeScore(){
      const blocks = Array.from(document.querySelectorAll('.q[data-qid]'));
      let correct = 0;
      blocks.forEach(b => { 
        const sel = b.querySelector('.choice.correct'); 
        if(sel) correct++; 
      });
      return { correct, total: blocks.length, percent: Math.round((correct/blocks.length)*100) };
    }

    function celebrate(){
      const duration = 1500; 
      const end = Date.now() + duration;
      (function frame(){
        confetti({ particleCount: 3, angle: 60, spread: 70, origin: { x: 0 } });
        confetti({ particleCount: 3, angle: 120, spread: 70, origin: { x: 1 } });
        if (Date.now() < end) requestAnimationFrame(frame);
      })();
    }

    function resetQuiz(){
      document.querySelectorAll('.choice').forEach(c => c.classList.remove('correct','wrong'));
      totalAnswered = 0;
      consecutiveCorrect = 0;
      startTime = Date.now();
      gsap.from("#quiz .q", {opacity:0, y:10, stagger:.08, duration:.45});
      window.scrollTo({ top:0, behavior:'smooth' });
      updateProgress();
    }

    // نظام الأحداث
    document.addEventListener('click', (e) => {
      const choice = e.target.closest('.choice');
      if(!choice) return;
      
      SoundSystem.play('click');
      
      const container = choice.closest('.choices');
      const wasAnswered = container.querySelector('.choice.correct, .choice.wrong');
      
      if (wasAnswered) return;
      
      container.querySelectorAll('.choice').forEach(c => c.classList.remove('correct','wrong'));
      totalAnswered++;
      
      if(choice.dataset.correct === "true"){
        choice.classList.add('correct');
        consecutiveCorrect++;
        SoundSystem.play('correct');
        
        gsap.fromTo(choice, 
          {scale:1}, 
          {scale:1.05, y:-4, duration:.3, yoyo:true, repeat:1, ease: "back.out(1.7)"}
        );
        
        if (consecutiveCorrect >= 3) {
          setTimeout(() => showEncouragementMessage('correct'), 800);
          consecutiveCorrect = 0;
        }
      } else {
        choice.classList.add('wrong');
        consecutiveCorrect = 0;
        SoundSystem.play('wrong');
        
        gsap.fromTo(choice, {x:0}, {x:-8, duration:.08, yoyo:true, repeat:6, ease: "power2.inOut"});
        
        if (totalAnswered >= 3) {
          setTimeout(() => showEncouragementMessage('wrong'), 1000);
        }
      }
      
      updateProgress();
    });

    // تهيئة الأحداث
    el.start.addEventListener('click', askStudent);

    el.submit.addEventListener('click', () => {
      const s = getStudent();
      const { correct, total, percent } = computeScore();
      celebrate();
      
      const performanceLevel = getPerformanceLevel(percent);
      const smartMessage = getFinalResultMessage(percent, s?.name);
      
      let resultIcon = 'success';
      let resultColor = '#10b981';
      
      if (percent < 60) {
        resultIcon = 'info';
        resultColor = '#3b82f6';
      }
      
      SoundSystem.play('complete');
      
      Swal.fire({
        title: `${performanceLevel === 'excellent' ? '🏆' : performanceLevel === 'good' ? '⭐' : performanceLevel === 'average' ? '👍' : '💪'} النتائج النهائية`,
        html: `
          <div style="text-align:right;line-height:1.9;font-size:16px">
            <div style="margin-bottom:10px"><strong>👤 الاسم:</strong> ${s?.name || 'غير محدد'}</div>
            <div style="margin-bottom:10px"><strong>🏫 الصف:</strong> ${s?.klass || 'غير محدد'}</div>
            <div style="margin-bottom:10px"><strong>📊 النتيجة:</strong> ${correct} من ${total} سؤال</div>
            <div style="margin-bottom:15px"><strong>📈 النسبة المئوية:</strong> ${percent}%</div>
            <hr style="margin: 15px 0; border: none; height: 1px; background: linear-gradient(to right, transparent, #ddd, transparent);">
            <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);padding:15px;border-radius:12px;font-weight:600;color:#92400e;text-align:center">
              ${smartMessage}
            </div>
          </div>`,
        icon: resultIcon,
        width: '500px',
        confirmButtonText: '🔄 إعادة المحاولة',
        confirmButtonColor: resultColor,
        showDenyButton: true,
        denyButtonText: '🏠 العودة للرئيسية',
        denyButtonColor: '#d97706',
        allowOutsideClick: false,
        allowEscapeKey: false
      }).then(res => {
        if(res.isConfirmed) {
          resetQuiz();
        } else if (res.isDenied) {
          window.location.href='../../index.html';
        }
      });
    });

    // تهيئة الصفحة
    SoundSystem.init();
    updateMeta();
    
    AOS.init({
      duration: 700,
      easing: 'ease',
      once: true,
      offset: 50
    });
    
    document.getElementById('countTotal').textContent = document.querySelectorAll('.q[data-qid]').length;
    
    console.log('✅ تم تحميل الصفحة بنجاح');'''
        
        # إنشاء الملف الجديد
        new_content = head_section + '</head>\n' + body_section[:-7] + '\n  <script>' + working_js + '\n  </script>\n</body>\n</html>'
        
        # كتابة الملف المحدث
        with open(lesson_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "تم إصلاح JavaScript بنجاح"
        
    except Exception as e:
        return False, f"خطأ: {str(e)}"

def main():
    base_path = Path(".")
    lessons = []
    
    # البحث عن الدروس المكسورة فقط
    problematic_lessons = [
        "unit-1-cells/lesson-1-2",
        "unit-1-cells/lesson-1-3", 
        "unit-2-transport/lesson-2-1",
        "unit-2-transport/lesson-2-2",
        "unit-2-transport/lesson-2-3"
    ]
    
    for lesson_path in problematic_lessons:
        full_path = base_path / lesson_path / "index.html"
        if full_path.exists():
            lessons.append({
                'path': str(full_path),
                'full_name': lesson_path
            })
    
    print("🔧 إصلاح JavaScript في الدروس المكسورة...")
    print("=" * 80)
    
    fixed_count = 0
    error_count = 0
    
    for lesson in lessons:
        print(f"\n📚 إصلاح الدرس: {lesson['full_name']}")
        
        success, message = fix_javascript_structure(lesson['path'])
        
        if success:
            print(f"✅ {message}")
            fixed_count += 1
        else:
            print(f"❌ فشل الإصلاح: {message}")
            error_count += 1
    
    print("\n" + "=" * 80)
    print(f"📈 ملخص النتائج:")
    print(f"✅ الدروس المُصلحة: {fixed_count}")
    print(f"❌ الدروس التي فشل إصلاحها: {error_count}")
    
    if fixed_count > 0:
        print(f"\n🎉 تم إصلاح {fixed_count} درس!")
        print(f"📝 الدروس يجب أن تعمل الآن بشكل صحيح")

if __name__ == "__main__":
    main()