#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
أداة إنشاء نسخة نظيفة من درس 1-2 بمحتوى أنواع الخلايا
"""

html_content = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <title>🔬 درس 1-2 — أنواع الخلايا</title>
  
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@500;700;900&display=swap" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css"/>
  <script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/howler@2.2.4/dist/howler.min.js"></script>

  <style>
    :root{
      --bg:linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); --card:#ffffff; --muted:#6b7280; --text:#1f2937;
      --primary:#f59e0b; --primary-2:#d97706; --accent:#ef4444;
      --success:#10b981; --warn:#f59e0b; --danger:#ef4444; --ring:rgba(245,158,11,.4);
      --card-shadow:0 20px 40px rgba(0,0,0,.1), 0 8px 16px rgba(0,0,0,.08);
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0; background: var(--bg);
      min-height:100vh;
      color:var(--text); font-family:"Cairo", system-ui, sans-serif; line-height:1.7; letter-spacing:.2px;
    }
    .wrap{max-width:1100px; margin-inline:auto; padding:24px}
    .card{
      background:rgba(255,255,255,.9); border-radius:20px; padding:24px;
      border:1px solid rgba(255,255,255,.25); backdrop-filter:blur(10px);
      box-shadow: var(--card-shadow); margin-bottom:20px; color:var(--text)
    }
    .card h1{margin:0 0 16px; color:var(--primary); font-weight:900; font-size:24px}
    .card p{margin:8px 0; line-height:1.7}
    .btn{
      background:linear-gradient(135deg, var(--primary) 0%, var(--primary-2) 100%);
      color:white; border:0; padding:12px 20px; border-radius:16px; font-size:16px; font-weight:700;
      cursor:pointer; text-decoration:none; display:inline-flex; align-items:center; gap:8px;
      transition:all 0.3s ease; box-shadow: var(--card-shadow)
    }
    .btn:hover{transform:translateY(-2px); box-shadow:0 24px 50px rgba(245,158,11,.4)}
    .btn:active{transform:scale(.98)}
    .progress{
      background:rgba(255,255,255,.3); height:12px; border-radius:10px; overflow:hidden; margin:12px 0;
      border:1px solid rgba(255,255,255,.4)
    }
    .progress-fill{
      background:linear-gradient(90deg, var(--success), #22c55e); height:100%; width:0%;
      transition:width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)
    }
    .quiz-container{display:none; margin-top:20px}
    .quiz-stats{
      display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;
      font-weight:700; color:var(--primary)
    }
    .q{
      background:rgba(255,255,255,.9); border-radius:16px; padding:20px; margin-bottom:16px;
      border:1px solid rgba(255,255,255,.3); backdrop-filter:blur(10px); position:relative;
      transition:all 0.3s ease; box-shadow: 0 8px 20px rgba(0,0,0,.08)
    }
    .q:hover{transform:translateY(-2px); box-shadow: 0 12px 30px rgba(0,0,0,.12)}
    .choices{display:flex; flex-direction:column; gap:8px; margin-top:12px}
    .choice{
      padding:12px 16px; border:2px solid rgba(0,0,0,.1); border-radius:12px; cursor:pointer;
      transition:all 0.3s ease; background:rgba(255,255,255,.7); font-weight:500
    }
    .choice:hover{background:var(--primary); color:white; transform:translateX(4px)}
    .choice.correct{background:var(--success); color:white; border-color:var(--success)}
    .choice.wrong{background:var(--danger); color:white; border-color:var(--danger)}
    footer{
      text-align:center; margin-top:40px; padding:20px; color:var(--muted);
      font-size:14px; line-height:1.6
    }
    .credit{font-weight:700; color:var(--primary)}
    @media (max-width: 768px) {
      .wrap{padding:12px}
      .card{padding:16px}
      .btn{padding:10px 16px; font-size:14px}
    }
  </style>
</head>

<body>
  <div class="wrap">
    <div class="card">
      <h1>🧬 أنواع الخلايا</h1>
      <p><strong>الطالب/ـة:</strong> <span id="studentMeta">مرحبًا! لنبدأ…</span></p>
      <div class="quiz-stats">
        <div>📊 التقدم: <span id="countDone">0</span>/<span id="countTotal">0</span></div>
        <div class="progress">
          <div class="progress-fill" id="barFill"></div>
        </div>
      </div>
      <p>مرحبًا بك في الدرس الثاني من وحدة الخلايا! ستتعرف اليوم على أنواع الخلايا المختلفة وخصائص كل نوع.</p>
      <button class="btn" id="btnStart">
        <span>🚀</span>
        <span>ابدأ النشاط</span>
      </button>
    </div>

    <div id="quiz" class="quiz-container">
      <div class="card">
        <div id="quizList"></div>
        
        <div style="margin-top:20px; text-align:center">
          <button class="btn" id="btnSubmit">📋 إنهاء النشاط</button>
          <button class="btn" id="btnReset" style="margin-right:12px; background:var(--accent)">🔄 إعادة تعيين</button>
        </div>
      </div>
    </div>

    <footer class="card">
      <div><span class="credit">🎨 تصميم: الوتين الضامرية |لمار السيابية|مها المعمرية|مريم محمود البلوشية|مريم وائل البلوشية|</span> — 🏫 مدرسة عاتكة بنت زيد — تحت إشراف الأستاذة سامية 👩‍🏫</div>
      <div>© انشطة تعليمية الوتين 🌟</div>
    </footer>
  </div>

  <script>
    AOS.init({ duration: 700, once: true });

    // النظام الصوتي المتقدم
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
            src: [`../../assets/audio/${soundMappings[type]}`],
            volume: 0.7,
            preload: true,
            onloaderror: () => console.warn(`فشل تحميل ${type}`)
          });
        });
        
        console.log('🎵 تم تهيئة النظام الصوتي');
      },
      
      play(soundType) {
        if (this.enabled && this.sounds[soundType]) {
          this.sounds[soundType].play();
        }
      }
    };

    // تهيئة النظام الصوتي
    SoundSystem.init();

    // بنك الأسئلة — درس أنواع الخلايا
    const bank = [
      {q:"تنقسم الخلايا إلى نوعين رئيسيين حسب وجود النواة:", c:["بدائية وحقيقية النواة","نباتية وحيوانية","كبيرة وصغيرة","ميتة وحية"], a:0},
      {q:"الخلايا بدائية النواة تتميز بـ:", c:["وجود نواة محاطة بغشاء","عدم وجود نواة محاطة بغشاء","وجود بلاستيدات","كبر الحجم"], a:1},
      {q:"مثال على الكائنات بدائية النواة:", c:["النباتات","الحيوانات","البكتيريا","الفطريات"], a:2},
      {q:"الخلايا حقيقية النواة تتميز بـ:", c:["عدم وجود نواة","وجود نواة محاطة بغشاء نووي","البساطة التركيبية","صغر الحجم فقط"], a:1},
      {q:"أمثلة على الكائنات حقيقية النواة:", c:["البكتيريا فقط","النباتات والحيوانات والفطريات","الفيروسات","البكتيريا الزرقاء"], a:1},
      {q:"المادة الوراثية في الخلايا بدائية النواة:", c:["محاطة بغشاء نووي","موزعة في السيتوبلازم","غائبة تماماً","في الميتوكندريا"], a:1},
      {q:"المادة الوراثية في الخلايا حقيقية النواة:", c:["موزعة في السيتوبلازم","محاطة بغشاء نووي داخل النواة","غائبة","في الجدار الخلوي"], a:1},
      {q:"العُضيات الخلوية توجد في:", c:["الخلايا بدائية النواة فقط","الخلايا حقيقية النواة","جميع أنواع الخلايا","الفيروسات"], a:1},
      {q:"حجم الخلايا بدائية النواة مقارنة بحقيقية النواة:", c:["أكبر عادة","أصغر عادة","نفس الحجم","متغير جداً"], a:1},
      {q:"الريبوسومات في الخلايا بدائية النواة:", c:["غائبة تماماً","موجودة وحرة في السيتوبلازم","مرتبطة بالشبكة الإندوبلازمية","في النواة فقط"], a:1},
      {q:"الغشاء النووي موجود في:", c:["جميع أنواع الخلايا","الخلايا حقيقية النواة فقط","الخلايا بدائية النواة فقط","البكتيريا"], a:1},
      {q:"مثال على كائن وحيد الخلية بدائي النواة:", c:["الأميبا","بكتيريا E.coli","الخميرة","البراميسيوم"], a:1},
      {q:"مثال على كائن وحيد الخلية حقيقي النواة:", c:["البكتيريا","الأميبا","الفيروس","البكتيريا الزرقاء"], a:1},
      {q:"التركيب الداخلي للخلايا بدائية النواة:", c:["معقد جداً","بسيط نسبياً","يحتوي عُضيات متخصصة","مثل حقيقية النواة"], a:1},
      {q:"التركيب الداخلي للخلايا حقيقية النواة:", c:["بسيط","معقد مع عُضيات متخصصة","بدون تنظيم","مثل بدائية النواة"], a:1},
      {q:"الكروموسومات في الخلايا بدائية النواة:", c:["محاطة بغشاء","عبارة عن جزيء DNA دائري حر","متعددة","في النواة"], a:1},
      {q:"الكروموسومات في الخلايا حقيقية النواة:", c:["حرة في السيتوبلازم","محاطة بغشاء نووي ومنظمة","دائرية فقط","غائبة"], a:1},
      {q:"عملية التنفس الخلوي في الخلايا حقيقية النواة تحدث في:", c:["السيتوبلازم فقط","الميتوكندريا أساساً","النواة","الجدار الخلوي"], a:1},
      {q:"عملية التنفس في الخلايا بدائية النواة تحدث في:", c:["الميتوكندريا","السيتوبلازم والغشاء الخلوي","النواة","البلاستيدات"], a:1},
      {q:"أقدم أشكال الحياة على الأرض:", c:["النباتات","الحيوانات","الكائنات بدائية النواة","الفطريات"], a:2}
    ];

    const el = {
      start: document.getElementById('btnStart'),
      quiz: document.getElementById('quiz'),
      list: document.getElementById('quizList'),
      submit: document.getElementById('btnSubmit'),
      reset: document.getElementById('btnReset'),
      meta: document.getElementById('studentMeta'),
      bar: document.getElementById('barFill'),
      done: document.getElementById('countDone'),
      total: document.getElementById('countTotal')
    };

    const storageKey = "watyn_bio_student";

    function getStudent(){ try{ return JSON.parse(localStorage.getItem(storageKey)) || null }catch{ return null } }
    function setStudent(obj){ localStorage.setItem(storageKey, JSON.stringify(obj)); }

    function renderQuestions(){
      el.total.textContent = bank.length;
      el.list.innerHTML = "";
      bank.forEach((item, idx)=>{
        const art = document.createElement('article');
        art.className = "q"; art.setAttribute('data-qid', 'q'+(idx+1));
        art.innerHTML = `
          <div><strong>${idx+1}) ${item.q}</strong></div>
          <div class="choices">
            ${item.c.map((txt,i)=>`<div class="choice" data-correct="${i===item.a}">${txt}</div>`).join('')}
          </div>
        `;
        el.list.appendChild(art);
      });
    }

    function updateProgress(){
      const total = document.querySelectorAll('.q[data-qid]').length;
      const answered = Array.from(document.querySelectorAll('.q')).filter(q => 
        q.querySelector('.choice.correct, .choice.wrong')
      ).length;
      
      if (el.total) el.total.textContent = total;
      if (el.done) el.done.textContent = answered;
      if (el.bar) el.bar.style.width = Math.round((answered/total)*100) + '%';
    }

    async function askStudent(){
      SoundSystem.play('start');
      
      const { value: formValues } = await Swal.fire({
        title: '🎓 مرحباً بك!',
        html:
          `<div style="text-align:right">
            <div style="margin-bottom:12px;font-weight:700;color:#d97706">أدخل بياناتك لتبدأ رحلتك العلمية:</div>
            <input id="swal-name" class="swal2-input" placeholder="اسم الطالب/ـة" style="text-align:right">
            <input id="swal-class" class="swal2-input" placeholder="الصف (مثال: التاسع/1)" style="text-align:right">
          </div>`,
        focusConfirm: false,
        confirmButtonText: '🚀 لنبدأ التعلم!',
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
        
        const welcomeMessages = [
          `🧬 أهلاً ${formValues.name}! مرحبًا بك في عالم أنواع الخلايا!`,
          `🔬 مرحبًا ${formValues.name}! ستكتشف اليوم الفرق بين الخلايا بدائية وحقيقية النواة`,
          `✨ أهلاً ${formValues.name}! رحلة مثيرة في تنوع الخلايا تنتظرك`
        ];
        const randomWelcome = welcomeMessages[Math.floor(Math.random() * welcomeMessages.length)];
        
        Swal.fire({
          title: '🎓 أهلاً وسهلاً!',
          text: randomWelcome,
          icon: 'success',
          confirmButtonText: '🧬 لننطلق!',
          timer: 4000,
          timerProgressBar: true
        }).then(() => {
          SoundSystem.play('welcome');
        });
        
        el.quiz.style.display = "block";
        gsap.from("#quiz .q", {opacity:0, y:20, stagger:.08, duration:.6});
      }
    }

    function updateMeta(){
      const s = getStudent();
      el.meta.textContent = s ? (`${s.name} — الصف: ${s.klass}`) : "مرحبًا! لنبدأ…";
    }

    document.addEventListener('click', (e)=>{
      const choice = e.target.closest('.choice');
      if(!choice) return;
      
      const container = choice.closest('.choices');
      const wasAnswered = container.querySelector('.choice.correct, .choice.wrong');
      if (wasAnswered) return;

      SoundSystem.play('click');
      
      container.querySelectorAll('.choice').forEach(c=> c.classList.remove('correct','wrong'));
      
      if(choice.dataset.correct === "true"){
        choice.classList.add('correct'); 
        SoundSystem.play('correct');
        gsap.fromTo(choice, {scale:1}, {scale:1.05, duration:.3, yoyo:true, repeat:1});
      }else{
        choice.classList.add('wrong'); 
        SoundSystem.play('wrong');
        gsap.fromTo(choice, {x:0}, {x:-10, duration:.1, yoyo:true, repeat:3});
      }
      updateProgress();
    });

    function computeScore(){
      const blocks = Array.from(document.querySelectorAll('.q[data-qid]'));
      let correct = 0;
      blocks.forEach(b=>{ const sel = b.querySelector('.choice.correct'); if(sel) correct++; });
      return { correct, total: blocks.length, percent: Math.round((correct/blocks.length)*100) };
    }

    function celebrate(){
      const duration = 2000; const end = Date.now() + duration;
      (function frame(){
        confetti({ particleCount: 5, angle: 60, spread: 70, origin: { x: 0 } });
        confetti({ particleCount: 5, angle: 120, spread: 70, origin: { x: 1 } });
        if (Date.now() < end) requestAnimationFrame(frame);
      })();
      SoundSystem.play('celebration');
    }

    el.start.addEventListener('click', askStudent);

    el.submit.addEventListener('click', ()=>{
      const s = getStudent();
      const { correct, total, percent } = computeScore();
      
      celebrate();
      
      let message, icon, soundType;
      if (percent >= 90) {
        message = `🏆 ممتاز ${s?.name}! أداء رائع - ${percent}%`;
        icon = 'success';
        soundType = 'celebration';
      } else if (percent >= 70) {
        message = `👏 أحسنت ${s?.name}! أداء جيد - ${percent}%`;
        icon = 'success';
        soundType = 'correct';
      } else {
        message = `📚 ${s?.name}، يمكنك المحاولة مرة أخرى - ${percent}%`;
        icon = 'info';
        soundType = 'progress';
      }
      
      SoundSystem.play(soundType);
      
      Swal.fire({
        title: 'نتيجة النشاط',
        text: message,
        icon: icon,
        confirmButtonText: '👍 حسناً',
        footer: `الدرجة: ${correct}/${total} • النسبة: ${percent}%`
      });
    });

    el.reset.addEventListener('click', ()=>{
      Swal.fire({
        title: 'إعادة تعيين',
        text: 'هل تريد حقاً إعادة تعيين جميع الإجابات؟',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'نعم، أعد التعيين',
        cancelButtonText: 'إلغاء'
      }).then((result) => {
        if (result.isConfirmed) {
          document.querySelectorAll('.choice').forEach(c => c.classList.remove('correct', 'wrong'));
          updateProgress();
          SoundSystem.play('click');
        }
      });
    });

    // تهيئة النشاط
    document.addEventListener('DOMContentLoaded', ()=>{
      renderQuestions();
      updateMeta();
      updateProgress();
    });
  </script>
</body>
</html>'''

# كتابة الملف
import os
lesson_path = "unit-1-cells/lesson-1-2/index.html"

# حذف الملف القديم إن وجد
if os.path.exists(lesson_path):
    os.remove(lesson_path)

# كتابة المحتوى الجديد
with open(lesson_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ تم إنشاء نسخة نظيفة من درس 1-2 بنجاح!")
print("📋 المحتوى: 20 سؤال حول أنواع الخلايا (بدائية وحقيقية النواة)")
print("🎵 النظام الصوتي: متكامل ومفعل")
print("🎨 التصميم: نظيف وبسيط مثل الدرس المثالي 1-1")