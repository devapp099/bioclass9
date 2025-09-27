#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح عاجل - إعادة ترتيب الكود JavaScript بالكامل
"""

import os
import re

def fix_javascript_structure(file_path):
    """إصلاح بنية JavaScript بالكامل"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"🔧 إعادة ترتيب JavaScript في {file_path}")
        
        # استخراج الأسئلة
        questions_pattern = r'\{q:"[^"]+",\s*c:\[[^\]]+\],\s*a:\d+\}'
        questions = re.findall(questions_pattern, content)
        
        if not questions:
            print(f"❌ لا توجد أسئلة للاستخراج في {file_path}")
            return False
        
        print(f"📝 تم العثور على {len(questions)} سؤال")
        
        # إنشاء SoundSystem صحيح
        sound_system_code = '''// النظام الصوتي المتقدم
    const SoundSystem = {
      enabled: true,
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
            src: [`assets/audio/${soundMappings[type]}`],
            volume: 0.3,
            html5: true
          });
        });
      },
      
      play(type) {
        if (this.enabled && this.sounds[type]) {
          this.sounds[type].play();
        }
      }
    };'''
        
        # إنشاء bank صحيح
        bank_code = f'''
    const bank = [
      {chr(10).join("      " + q + "," for q in questions)}
    ];'''
        
        # البحث عن نهاية </script> الأخير وإضافة الكود الصحيح
        # إزالة الكود القديم المكسور أولاً
        # إزالة كل شيء من AOS.init حتى نهاية script
        aos_pattern = r'AOS\.init\([^;]+\);.*?</script>'
        match = re.search(aos_pattern, content, re.DOTALL)
        
        if match:
            # استبدال بالكود الصحيح
            new_script_section = f'''AOS.init({{ duration: 700, once: true }});

{sound_system_code}
{bank_code}

    const el = {{
      start: document.getElementById('btnStart'),
      quiz: document.getElementById('quiz'),
      list: document.getElementById('quizList'),
      submit: document.getElementById('btnSubmit'),
      reset: document.getElementById('btnReset'),
      progress: document.getElementById('progressBar'),
      total: document.getElementById('countTotal'),
      done: document.getElementById('countDone')
    }};

    const storageKey = 'quizProgress_' + window.location.pathname;

    function getStudent(){{ try{{ return JSON.parse(localStorage.getItem(storageKey)) || null }}catch{{ return null }} }}
    function setStudent(obj){{ localStorage.setItem(storageKey, JSON.stringify(obj)); }}

    function renderQuestions(){{
      el.total.textContent = bank.length;
      el.list.innerHTML = "";
      bank.forEach((item, idx)=>{{
        const art = document.createElement('article');
        art.className = "q"; art.setAttribute('data-qid', 'q'+(idx+1));
        art.innerHTML = `
          <div><strong>${{idx+1}}) ${{item.q}}</strong></div>
          <div class="choices">
            ${{item.c.map((txt,i)=>`<div class="choice" data-correct="${{i===item.a}}">${{txt}}</div>`).join('')}}
          </div>
        `;
        el.list.appendChild(art);
      }});
    }}

    function answeredCount(){{
      let n=0;
      document.querySelectorAll('.q').forEach(q=>{{
        if(q.querySelector('.choice.correct, .choice.wrong')) n++;
      }});
      return n;
    }}

    function updateProgress(){{
      const total = document.querySelectorAll('.q[data-qid]').length;
      const answered = Array.from(document.querySelectorAll('.q')).filter(q => 
        q.querySelector('.choice.correct, .choice.wrong')
      ).length;
      
      const barFill = document.getElementById('barFill');
      const countDone = document.getElementById('countDone');
      const countTotal = document.getElementById('countTotal');
      
      if (countTotal) countTotal.textContent = total;
      if (countDone) countDone.textContent = answered;
      if (barFill) barFill.style.width = Math.round((answered/total)*100) + '%';
    }}

    // النشاط الرئيسي
    document.addEventListener('click', e => {{
      if (e.target.matches('.choice')) {{
        const isCorrect = e.target.dataset.correct === 'true';
        
        // إزالة الحالات السابقة من هذا السؤال
        e.target.parentNode.querySelectorAll('.choice').forEach(ch => {{
          ch.classList.remove('correct', 'wrong');
        }});
        
        // إضافة الحالة الجديدة
        e.target.classList.add(isCorrect ? 'correct' : 'wrong');
        
        // تشغيل الصوت
        SoundSystem.play(isCorrect ? 'correct' : 'wrong');
        
        // تحديث التقدم
        updateProgress();
      }}
    }});

    // بدء التطبيق
    SoundSystem.init();
    renderQuestions();
    updateProgress();
  </script>'''
            
            content = content.replace(match.group(0), new_script_section)
            
            # حفظ الملف
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ تم إصلاح JavaScript بنجاح في {file_path}")
            return True
        
        else:
            print(f"❌ لم يتم العثور على نمط AOS.init في {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في إصلاح {file_path}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 إصلاح عاجل - إعادة ترتيب JavaScript...")
    print("=" * 60)
    
    # تطبيق على جميع الدروس
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
            if fix_javascript_structure(lesson):
                fixed_count += 1
        else:
            print(f"❌ الملف غير موجود: {lesson}")
    
    print("\n" + "=" * 60)
    print(f"🎉 انتهاء العملية!")
    print(f"✅ تم إصلاح {fixed_count} درس من أصل {len(lessons)}")
    print("🌟 الأسئلة ستظهر الآن في جميع الدروس!")

if __name__ == "__main__":
    main()