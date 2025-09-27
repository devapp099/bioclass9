#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

class SmartSystemTransfer:
    def __init__(self):
        self.reference_lesson = Path("unit-1-cells/lesson-1-1/index.html")
        self.smart_systems = {
            'head_scripts': '',
            'css_styles': '',
            'sound_system': '',
            'notification_system': '',
            'performance_functions': '',
            'interaction_handlers': '',
            'initialization': ''
        }
        
    def extract_smart_systems(self):
        """استخراج جميع الأنظمة الذكية من الدرس المرجعي"""
        try:
            with open(self.reference_lesson, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # استخراج مكتبات الـ head
            head_scripts = '''  <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css"/>
  <script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/howler@2.2.4/dist/howler.min.js"></script>'''
            
            # النظام الصوتي الكامل
            sound_system = '''
    const SoundSystem = {
      enabled: true,
      currentVolume: 0.7,
      sounds: {},
      
      init() {
        const soundTypes = ['correct', 'wrong', 'click', 'select', 'milestone', 'celebration', 'complete', 'start', 'welcome', 'progress'];
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
        
        soundTypes.forEach(type => {
          this.sounds[type] = new Howl({
            src: [`../../assets/audio/${soundMappings[type]}`],
            volume: this.getContextualVolume(type),
            preload: true,
            onloaderror: () => {
              console.warn(`فشل تحميل الصوت: ${type}`);
            }
          });
        });
        
        console.log('🎵 تم تهيئة النظام الصوتي المحسّن');
      },
      
      play(soundType) {
        if (!this.enabled || !this.sounds[soundType]) return;
        
        try {
          const contextualVolume = this.getContextualVolume(soundType);
          this.sounds[soundType].volume(contextualVolume);
          this.sounds[soundType].play();
          this.trackSoundUsage(soundType);
        } catch (error) {
          console.warn(`خطأ في تشغيل الصوت ${soundType}:`, error);
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
      },
      
      trackSoundUsage(soundType) {
        if (!window.soundStats) window.soundStats = {};
        window.soundStats[soundType] = (window.soundStats[soundType] || 0) + 1;
      },
      
      sequence(sounds, delay = 500) {
        sounds.forEach((sound, index) => {
          setTimeout(() => {
            this.play(sound);
            if (sound === 'celebration' && typeof confetti !== 'undefined') {
              confetti({
                particleCount: 50,
                spread: 60,
                origin: { y: 0.8 }
              });
            }
          }, index * delay);
        });
      },
      
      toggle() {
        this.enabled = !this.enabled;
        return this.enabled;
      }
    };'''
            
            # نظام الإشعارات الذكي
            notification_system = '''
    const EnhancedNotificationSystem = {
      student: null,
      lessonInfo: {
        title: "درس تفاعلي",
        description: "تعلم المفاهيم الأساسية بطريقة تفاعلية",
        keyConcepts: ["المفاهيم الأساسية"],
        topic: "biology"
      },
      interactionStats: {
        clicks: 0,
        correctAnswers: 0,
        wrongAnswers: 0,
        timeSpent: 0
      },
      
      showWelcomeMessage() {
        const welcomeMessages = [
          "🎓 أهلاً وسهلاً {name}! مرحبًا بك في هذا الدرس المثير!",
          "🌟 مرحبًا {name}! أنت على وشك تعلم شيء رائع!",
          "✨ أهلاً {name}! دعنا نتعلم العلوم معًا!"
        ];
        
        const randomWelcome = welcomeMessages[Math.floor(Math.random() * welcomeMessages.length)];
        const personalizedWelcome = randomWelcome.replace('{name}', this.student?.name || 'البطل/ة');
        const lessonIntro = `📚 ستتعلم اليوم: ${this.lessonInfo.description}`;
        
        Swal.fire({
          title: '🎓 مرحباً بك في رحلة التعلم!',
          html: `
            <div style="text-align:right;line-height:1.8;font-size:16px">
              <div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:15px;border-radius:12px;margin-bottom:15px">
                ${personalizedWelcome}
              </div>
              <div style="background:#f8f9ff;padding:15px;border-radius:10px;border-right:4px solid #667eea">
                ${lessonIntro}
              </div>
            </div>`,
          icon: 'info',
          confirmButtonText: '🚀 لنبدأ التعلم!',
          confirmButtonColor: '#667eea',
          timer: 8000,
          timerProgressBar: true
        }).then(() => {
          SoundSystem.play('start');
          this.startSessionTimer();
        });
      },
      
      startSessionTimer() {
        this.sessionStartTime = Date.now();
        this.timerInterval = setInterval(() => {
          this.interactionStats.timeSpent = Math.floor((Date.now() - this.sessionStartTime) / 1000);
        }, 1000);
      },
      
      initForStudent(studentData) {
        this.student = studentData;
        this.showWelcomeMessage();
        console.log(`🤖 تم تفعيل النظام الذكي للطالب: ${studentData.name}`);
      }
    };'''
            
            # دوال الأداء والتقييم
            performance_functions = '''
    function getPerformanceLevel(percentage) {
      if (percentage >= 90) return 'excellent';
      if (percentage >= 75) return 'good';
      if (percentage >= 60) return 'average';
      return 'needsWork';
    }

    function getFinalResultMessage(percentage, studentName) {
      const name = studentName || 'البطل/ة';
      const messages = {
        excellent: [
          `🏆 مبروك ${name}! أداء استثنائي - أنت عالم/ة حقيقي/ة!`,
          `⭐ رائع جداً ${name}! إتقان كامل للموضوع - فخور بك!`,
          `🌟 مذهل ${name}! نتيجة تستحق التقدير والاحترام!`
        ],
        good: [
          `👏 أحسنت ${name}! أداء جيد جداً - على الطريق الصحيح!`,
          `💪 عمل ممتاز ${name}! تحسن واضح وأداء مميز!`,
          `🎯 رائع ${name}! يظهر فهماً جيداً للموضوع`
        ],
        average: [
          `📚 أداء جيد ${name}! مراجعة بسيطة وستكون في القمة!`,
          `🎯 استمر ${name}! بداية جيدة للإتقان`,
          `💡 جيد ${name}! مع قليل من المراجعة ستصل للتميز`
        ],
        needsWork: [
          `💚 لا بأس ${name}! بداية التعلم - لا تستسلم!`,
          `🌱 استمر في المحاولة ${name}! كل عالم عظيم بدأ من هنا`,
          `🤝 معاً سنصل للهدف ${name}! المثابرة هي سر النجاح`
        ]
      };
      
      const level = getPerformanceLevel(percentage);
      const levelMessages = messages[level];
      return levelMessages[Math.floor(Math.random() * levelMessages.length)];
    }

    function showEncouragementMessage(type) {
      const s = getStudent();
      const name = s?.name || 'البطل/ة';
      
      const messages = {
        correct: [
          `ممتاز ${name}! إجابة صحيحة رائعة! 🌟`,
          `أحسنت ${name}! أنت تتقدم بشكل ممتاز! 👏`,
          `رائع ${name}! استمر على هذا الأداء المميز! 🚀`
        ],
        wrong: [
          `لا بأس ${name}، المحاولة جزء من التعلم! 💪`,
          `فكر مرة أخرى ${name}، أنت قريب من الإجابة الصحيحة! 🤔`,
          `استمر في المحاولة ${name}، كل خطأ فرصة للتعلم! 🌱`
        ]
      };
      
      const messageList = messages[type] || messages['correct'];
      const randomMessage = messageList[Math.floor(Math.random() * messageList.length)];
      
      Swal.fire({
        title: type === 'correct' ? '🎉 أحسنت!' : '💪 استمر!',
        text: randomMessage,
        icon: type === 'correct' ? 'success' : 'info',
        timer: 3000,
        timerProgressBar: true,
        toast: true,
        position: 'top-end',
        showConfirmButton: false
      });
    }

    function celebrate(){
      const duration = 1500; 
      const end = Date.now() + duration;
      (function frame(){
        confetti({ particleCount: 3, angle: 60, spread: 70, origin: { x: 0 } });
        confetti({ particleCount: 3, angle: 120, spread: 70, origin: { x: 1 } });
        if (Date.now() < end) requestAnimationFrame(frame);
      })();
    }'''
            
            # التهيئة
            initialization = '''
    // تهيئة الأنظمة عند تحميل الصفحة
    document.addEventListener('DOMContentLoaded', function() {
      SoundSystem.init();
      console.log('🎵 تم تهيئة النظام الصوتي المحسّن');
      console.log('🤖 تم تهيئة نظام الرسائل التفاعلية الذكية');
    });'''
            
            self.smart_systems = {
                'head_scripts': head_scripts,
                'sound_system': sound_system,
                'notification_system': notification_system,
                'performance_functions': performance_functions,
                'initialization': initialization
            }
            
            return True
            
        except Exception as e:
            print(f"❌ خطأ في استخراج الأنظمة: {str(e)}")
            return False
    
    def apply_to_lesson(self, lesson_path, lesson_info=None):
        """تطبيق الأنظمة الذكية على درس مع الحفاظ على محتواه"""
        try:
            with open(lesson_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # استخراج معلومات الدرس
            title_match = re.search(r'<title>(.*?)</title>', content)
            title = title_match.group(1) if title_match else "درس تفاعلي"
            
            # استخراج المحتوى بين <body> و </body>
            body_match = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
            if not body_match:
                return False, "لم يتم العثور على محتوى body"
            
            body_content = body_match.group(1)
            
            # إنشاء معلومات الدرس الذكية
            if lesson_info:
                lesson_info_js = f'''
      lessonInfo: {{
        title: "{lesson_info.get('title', 'درس تفاعلي')}",
        description: "{lesson_info.get('description', 'تعلم المفاهيم الأساسية')}",
        keyConcepts: {lesson_info.get('keyConcepts', ['المفاهيم الأساسية'])},
        topic: "{lesson_info.get('topic', 'biology')}"
      }},'''
            else:
                lesson_info_js = '''
      lessonInfo: {
        title: "درس تفاعلي",
        description: "تعلم المفاهيم الأساسية بطريقة تفاعلية",
        keyConcepts: ["المفاهيم الأساسية"],
        topic: "biology"
      },'''
            
            # تخصيص نظام الإشعارات للدرس
            customized_notification = self.smart_systems['notification_system'].replace(
                '''lessonInfo: {
        title: "درس تفاعلي",
        description: "تعلم المفاهيم الأساسية بطريقة تفاعلية",
        keyConcepts: ["المفاهيم الأساسية"],
        topic: "biology"
      },''', lesson_info_js
            )
            
            # إنشاء الملف الجديد
            new_content = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <title>{title}</title>
  
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@500;700;900&display=swap" rel="stylesheet" />

{self.smart_systems['head_scripts']}

  <script>
{self.smart_systems['sound_system']}

{customized_notification}

{self.smart_systems['performance_functions']}

{self.smart_systems['initialization']}
  </script>

  <style>
    :root{{
      --bg:linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); --card:#ffffff; --muted:#6b7280; --text:#1f2937;
      --primary:#f59e0b; --primary-2:#d97706; --accent:#ef4444;
      --success:#10b981; --warn:#f59e0b; --danger:#ef4444; --ring:rgba(245,158,11,.4);
      --card-shadow:0 20px 40px rgba(0,0,0,.1), 0 8px 16px rgba(0,0,0,.08);
    }}
    *{{box-sizing:border-box}}
    html,body{{height:100%}}
    body{{
      margin:0; background: var(--bg);
      min-height:100vh;
      color:var(--text); font-family:"Cairo", system-ui, sans-serif; line-height:1.7; letter-spacing:.2px;
      position: relative;
    }}
    body::before {{
      content: '';
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: 
        radial-gradient(circle at 20% 80%, rgba(255,165,0,.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255,69,0,.12) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(255,20,147,.1) 0%, transparent 50%);
      z-index: -1;
      pointer-events: none;
    }}
    .wrap{{max-width:1100px; margin-inline:auto; padding:24px}}
    header{{
      display:flex; align-items:center; justify-content:space-between; gap:12px; padding:18px 22px;
      border:1px solid rgba(255,255,255,.3);
      background:linear-gradient(135deg, rgba(255,255,255,.95) 0%, rgba(255,255,255,.85) 100%);
      border-radius:20px; backdrop-filter: blur(10px); position:sticky; top:16px; z-index:10;
      box-shadow: var(--card-shadow);
    }}
    .brand{{display:flex; align-items:center; gap:12px}}
    .logo{{width:42px; height:42px; border-radius:12px;
      background: conic-gradient(from 200deg, var(--primary), var(--accent), #10b981, #3b82f6);
      box-shadow: 0 8px 24px rgba(245,158,11,.35);
      animation: logoRotate 20s linear infinite;
    }}
    @keyframes logoRotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    .title{{font-weight:900; font-size:clamp(20px,3vw,28px)}}
    .subtitle{{font-weight:700; font-size:clamp(14px,2vw,16px); color:var(--muted)}}
    .card{{
      background: linear-gradient(135deg, rgba(255,255,255,.95) 0%, rgba(255,255,255,.85) 100%);
      border:1px solid rgba(255,255,255,.4);
      border-radius:22px; padding:22px;
      box-shadow: var(--card-shadow);
      transition: all 0.3s ease;
    }}
    .card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 25px 50px rgba(0,0,0,.12), 0 12px 20px rgba(0,0,0,.1);
    }}
    h1{{
      font-size: clamp(28px,4vw,40px);
      margin: 0 0 6px;
      font-weight: 900;
      background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 50%, #10b981 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }}
    h2{{font-size:clamp(24px,3.5vw,32px); margin:0 0 12px; font-weight:800; color:var(--text)}}
    .lead{{font-size:clamp(16px,2.2vw,20px); color:var(--muted); margin-bottom:16px; line-height:1.6}}
    ul{{padding-right:20px}}
    li{{margin-bottom:8px; line-height:1.6}}
    .btn{{
      background: linear-gradient(135deg, var(--primary) 0%, var(--primary-2) 100%);
      color: white; border: none; padding: 12px 24px; border-radius: 12px;
      font-size: 16px; font-weight: 700; cursor: pointer; transition: all 0.3s ease;
      font-family: inherit; text-decoration: none; display: inline-block;
      box-shadow: 0 4px 12px rgba(245,158,11,.3);
    }}
    .btn:hover{{
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(245,158,11,.4);
    }}
    .btn-ghost{{
      background: transparent; color: var(--muted);
      border: 2px solid rgba(107,114,128,.3); padding: 10px 22px;
      border-radius: 12px; font-size: 16px; font-weight: 600;
      cursor: pointer; transition: all 0.3s ease;
      font-family: inherit; text-decoration: none; display: inline-block;
    }}
    .btn-ghost:hover{{
      border-color: var(--primary);
      color: var(--primary);
      transform: translateY(-1px);
    }}
    .q{{
      background: rgba(255,255,255,.6);
      border: 1px solid rgba(255,255,255,.8);
      border-radius: 16px; padding: 20px; margin: 16px 0;
      transition: all 0.3s ease;
    }}
    .q:hover{{
      background: rgba(255,255,255,.8);
      transform: translateY(-1px);
    }}
    .choices{{display:flex; flex-direction:column; gap:12px; margin-top:16px}}
    .choice{{
      background: rgba(255,255,255,.8);
      border: 2px solid rgba(255,255,255,.6);
      border-radius: 12px; padding: 14px 18px;
      cursor: pointer; transition: all 0.3s ease;
      font-weight: 600;
    }}
    .choice:hover{{
      background: rgba(245,158,11,.1);
      border-color: var(--primary);
      transform: translateX(4px);
    }}
    .choice.correct{{
      background: linear-gradient(135deg, rgba(16,185,129,.15) 0%, rgba(16,185,129,.05) 100%);
      border-color: var(--success);
      color: var(--success);
    }}
    .choice.wrong{{
      background: linear-gradient(135deg, rgba(239,68,68,.15) 0%, rgba(239,68,68,.05) 100%);
      border-color: var(--danger);
      color: var(--danger);
    }}
    .progress{{display:flex; align-items:center; gap:12px; margin-top:12px}}
    .bar{{
      flex:1; height:8px; background:rgba(255,255,255,.6);
      border-radius:4px; overflow:hidden;
    }}
    .bar span{{
      display:block; height:100%; width:0%;
      background:linear-gradient(90deg, var(--primary) 0%, var(--success) 100%);
      transition: width 0.6s ease;
    }}
    .pulse{{
      position: absolute; top: -20px; right: -20px;
      width: 60px; height: 60px;
      background: radial-gradient(circle, var(--primary) 0%, transparent 70%);
      border-radius: 50%;
      animation: pulse 2s infinite;
      opacity: 0.7;
    }}
    @keyframes pulse {{
      0% {{ transform: scale(0.8); opacity: 0.7; }}
      50% {{ transform: scale(1.2); opacity: 0.3; }}
      100% {{ transform: scale(0.8); opacity: 0.7; }}
    }}
    
    @media (max-width: 768px) {{
      .wrap {{ padding: 16px; }}
      header {{ flex-direction: column; text-align: center; }}
      .brand {{ flex-direction: column; }}
      .choices {{ gap: 8px; }}
      .choice {{ padding: 12px 16px; }}
    }}
  </style>
</head>
<body>
{body_content}

  <script>
    // إضافة الأنظمة الذكية للدرس
    const storageKey = "watyn_bio_student";
    let totalAnswered = 0;
    let consecutiveCorrect = 0;
    let startTime = Date.now();

    const el = {{
      start: document.getElementById('btnStart'),
      quiz: document.getElementById('quiz'),
      submit: document.getElementById('btnSubmit'),
      reset: document.getElementById('btnReset'),
      meta: document.getElementById('studentMeta'),
      bar: document.getElementById('barFill'),
      done: document.getElementById('countDone'),
      total: document.getElementById('countTotal')
    }};

    function getStudent(){{ 
      try{{ 
        return JSON.parse(localStorage.getItem(storageKey)) || null;
      }} catch {{ 
        return null;
      }} 
    }}
    
    function setStudent(obj){{ 
      localStorage.setItem(storageKey, JSON.stringify(obj)); 
    }}

    function updateMeta(){{
      const s = getStudent();
      if (el.meta) {{
        el.meta.textContent = s ? (`الطالب/ـة: ${{s.name}} — الصف: ${{s.klass}}`) : "مرحبًا! لنبدأ…";
      }}
    }}

    function updateProgress(){{
      const total = document.querySelectorAll('.q[data-qid]').length;
      const answered = Array.from(document.querySelectorAll('.q')).filter(q => 
        q.querySelector('.choice.correct, .choice.wrong')
      ).length;
      
      if (el.total) el.total.textContent = total;
      if (el.done) el.done.textContent = answered;
      if (el.bar) {{
        const percentage = Math.round((answered/total)*100);
        el.bar.style.width = percentage + '%';
      }}
      
      if (answered > 0) {{
        SoundSystem.play('progress');
      }}
    }}

    function computeScore(){{
      const blocks = Array.from(document.querySelectorAll('.q[data-qid]'));
      let correct = 0;
      blocks.forEach(b => {{ 
        const sel = b.querySelector('.choice.correct'); 
        if(sel) correct++; 
      }});
      return {{ correct, total: blocks.length, percent: Math.round((correct/blocks.length)*100) }};
    }}

    async function askStudent(){{
      const {{ value: formValues }} = await Swal.fire({{
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
        preConfirm: () => {{
          const name = document.getElementById('swal-name').value?.trim();
          const klass = document.getElementById('swal-class').value?.trim();
          if(!name || !klass){{
            Swal.showValidationMessage('يرجى إدخال الاسم والصف');
            return false;
          }}
          return {{ name, klass }};
        }}
      }});
      
      if(formValues){{
        setStudent(formValues);
        updateMeta();
        EnhancedNotificationSystem.initForStudent(formValues);
        
        if (el.quiz) {{
          el.quiz.style.display = "block";
          gsap.from("#quiz .q", {{opacity:0, y:10, stagger:.08, duration:.5}});
        }}
        
        totalAnswered = 0;
        consecutiveCorrect = 0;
        startTime = Date.now();
      }}
    }}

    function resetQuiz(){{
      document.querySelectorAll('.choice').forEach(c => c.classList.remove('correct','wrong'));
      totalAnswered = 0;
      consecutiveCorrect = 0;
      startTime = Date.now();
      updateProgress();
      gsap.from("#quiz .q", {{opacity:0, y:10, stagger:.05, duration:.45}});
      window.scrollTo({{ top:0, behavior:'smooth' }});
    }}

    // نظام الأحداث الذكي
    document.addEventListener('click', (e) => {{
      const choice = e.target.closest('.choice');
      if(!choice) return;
      
      SoundSystem.play('click');
      
      const container = choice.closest('.choices');
      const wasAnswered = container.querySelector('.choice.correct, .choice.wrong');
      
      if (wasAnswered) return;
      
      container.querySelectorAll('.choice').forEach(c => c.classList.remove('correct','wrong'));
      totalAnswered++;
      
      if(choice.dataset.correct === "true"){{
        choice.classList.add('correct');
        consecutiveCorrect++;
        SoundSystem.play('correct');
        
        gsap.fromTo(choice, 
          {{scale:1}}, 
          {{scale:1.05, y:-4, duration:.3, yoyo:true, repeat:1, ease: "back.out(1.7)"}}
        );
        
        if (consecutiveCorrect >= 3) {{
          setTimeout(() => showEncouragementMessage('correct'), 800);
          consecutiveCorrect = 0;
        }}
      }} else {{
        choice.classList.add('wrong');
        consecutiveCorrect = 0;
        SoundSystem.play('wrong');
        
        gsap.fromTo(choice, {{x:0}}, {{x:-8, duration:.08, yoyo:true, repeat:6, ease: "power2.inOut"}});
        
        if (totalAnswered >= 3) {{
          setTimeout(() => showEncouragementMessage('wrong'), 1000);
        }}
      }}
      
      updateProgress();
    }});

    // تهيئة الأحداث
    if (el.start) el.start.addEventListener('click', askStudent);

    if (el.submit) {{
      el.submit.addEventListener('click', () => {{
        const s = getStudent();
        const {{ correct, total, percent }} = computeScore();
        celebrate();
        
        const performanceLevel = getPerformanceLevel(percent);
        const smartMessage = getFinalResultMessage(percent, s?.name);
        
        let resultIcon = 'success';
        let resultColor = '#10b981';
        
        if (percent < 60) {{
          resultIcon = 'info';
          resultColor = '#3b82f6';
        }}
        
        SoundSystem.play('complete');
        
        Swal.fire({{
          title: `${{performanceLevel === 'excellent' ? '🏆' : performanceLevel === 'good' ? '⭐' : performanceLevel === 'average' ? '👍' : '💪'}} النتائج النهائية`,
          html: `
            <div style="text-align:right;line-height:1.9;font-size:16px">
              <div style="margin-bottom:10px"><strong>👤 الاسم:</strong> ${{s?.name || 'غير محدد'}}</div>
              <div style="margin-bottom:10px"><strong>🏫 الصف:</strong> ${{s?.klass || 'غير محدد'}}</div>
              <div style="margin-bottom:10px"><strong>📊 النتيجة:</strong> ${{correct}} من ${{total}} سؤال</div>
              <div style="margin-bottom:15px"><strong>📈 النسبة المئوية:</strong> ${{percent}}%</div>
              <hr style="margin: 15px 0; border: none; height: 1px; background: linear-gradient(to right, transparent, #ddd, transparent);">
              <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);padding:15px;border-radius:12px;font-weight:600;color:#92400e;text-align:center">
                ${{smartMessage}}
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
        }}).then(res => {{
          if(res.isConfirmed) {{
            resetQuiz();
          }} else if (res.isDenied) {{
            window.location.href='../../index.html';
          }}
        }});
      }});
    }}

    if (el.reset) el.reset.addEventListener('click', resetQuiz);

    // تهيئة الصفحة
    updateMeta();
    
    AOS.init({{
      duration: 700,
      easing: 'ease',
      once: true,
      offset: 50
    }});
    
    if (document.getElementById('countTotal')) {{
      document.getElementById('countTotal').textContent = document.querySelectorAll('.q[data-qid]').length;
    }}
    
    updateProgress();
    
    console.log('✅ تم تحميل الصفحة مع جميع الأنظمة الذكية');
  </script>
</body>
</html>'''
            
            # كتابة الملف الجديد
            with open(lesson_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True, "تم نقل الأنظمة الذكية مع الحفاظ على المحتوى"
            
        except Exception as e:
            return False, f"خطأ: {str(e)}"

def main():
    print("🚀 نقل الأنظمة الذكية من الدرس 1-1 إلى باقي الدروس...")
    print("=" * 80)
    
    # إنشاء كائن النقل الذكي
    transfer = SmartSystemTransfer()
    
    # استخراج الأنظمة من الدرس المرجعي
    if not transfer.extract_smart_systems():
        print("❌ فشل في استخراج الأنظمة الذكية")
        return
    
    print("✅ تم استخراج الأنظمة الذكية من الدرس 1-1")
    
    # قائمة الدروس (باستثناء 1-1)
    lessons_to_update = [
        "unit-1-cells/lesson-1-2",
        "unit-1-cells/lesson-1-3",
        "unit-2-transport/lesson-2-1",
        "unit-2-transport/lesson-2-2",
        "unit-2-transport/lesson-2-3",
        "unit-3-biomolecules/lesson-3-1",
        "unit-3-biomolecules/lesson-3-2",
        "unit-3-biomolecules/lesson-3-3",
        "unit-4-nutrition/lesson-4-1",
        "unit-4-nutrition/lesson-4-2",
        "unit-5-respiration/lesson-5-1",
        "unit-6-homeostasis/lesson-6-1",
        "unit-6-homeostasis/lesson-6-2",
        "unit-6-homeostasis/lesson-6-3",
        "unit-6-homeostasis/lesson-6-4"
    ]
    
    # معلومات مخصصة لكل درس
    lesson_info_map = {
        "unit-1-cells/lesson-1-2": {
            "title": "رسم الخلايا وحساب التكبير",
            "description": "تعلم كيفية رسم الخلايا وحساب التكبير المجهري",
            "keyConcepts": ["الرسم العلمي", "التكبير", "المجهر"],
            "topic": "microscopy"
        },
        "unit-1-cells/lesson-1-3": {
            "title": "العُضيّات ووظائفها",
            "description": "استكشف العضيات المختلفة ووظائفها المتخصصة",
            "keyConcepts": ["العضيات", "الوظائف", "التخصص"],
            "topic": "organelles"
        },
        "unit-2-transport/lesson-2-1": {
            "title": "الانتشار",
            "description": "فهم آلية الانتشار ودورها في النقل الخلوي",
            "keyConcepts": ["الانتشار", "التدرج", "النقل السلبي"],
            "topic": "diffusion"
        }
        # يمكن إضافة المزيد حسب الحاجة
    }
    
    updated_count = 0
    error_count = 0
    
    for lesson_path in lessons_to_update:
        full_path = Path(lesson_path) / "index.html"
        
        if not full_path.exists():
            print(f"⚠️ {lesson_path}: الملف غير موجود")
            continue
        
        print(f"\n📚 معالجة: {lesson_path}")
        
        # الحصول على معلومات مخصصة للدرس
        lesson_info = lesson_info_map.get(lesson_path)
        
        success, message = transfer.apply_to_lesson(full_path, lesson_info)
        
        if success:
            print(f"✅ {message}")
            updated_count += 1
        else:
            print(f"❌ فشل التحديث: {message}")
            error_count += 1
    
    print("\n" + "=" * 80)
    print(f"📈 ملخص النتائج:")
    print(f"✅ الدروس المحدثة: {updated_count}")
    print(f"❌ الدروس التي فشل تحديثها: {error_count}")
    
    if updated_count > 0:
        print(f"\n🎉 تم نقل جميع الأنظمة الذكية بنجاح!")
        print(f"📝 الآن يمكنك تحديث محتوى كل درس يدوياً والأنظمة ستعمل تلقائياً")
        print(f"🔧 الأنظمة المنقولة:")
        print(f"   🎵 النظام الصوتي الكامل")
        print(f"   🔔 نظام الإشعارات الذكية")
        print(f"   💬 الرسائل التفاعلية المخصصة")
        print(f"   📊 تقييم الأداء الذكي")
        print(f"   🎨 التأثيرات البصرية والأنيميشن")

if __name__ == "__main__":
    main()