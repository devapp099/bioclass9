#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق النظام الصوتي الذكي ونظام الإشعارات على جميع الدروس
"""

import os
import re
import glob

def get_sound_system_code():
    """إرجاع كود النظام الصوتي الذكي"""
    return '''
    // 🎵 النظام الصوتي الذكي المتقدم
    const SoundSystem = {
      sounds: {
        // أصوات الإجابات
        correct: new Howl({ src: ['../../assets/audio/clap.mp3'], volume: 0.6 }),
        wrong: new Howl({ src: ['../../assets/audio/wrong_answer.mp3'], volume: 0.5 }),
        
        // أصوات التفاعل
        click: new Howl({ src: ['../../assets/audio/Click.mp3'], volume: 0.4 }),
        select: new Howl({ src: ['../../assets/audio/select.mp3'], volume: 0.4 }),
        
        // أصوات التقدم والإنجاز
        progress: new Howl({ src: ['../../assets/audio/notification.mp3'], volume: 0.5 }),
        milestone: new Howl({ src: ['../../assets/audio/win.mp3'], volume: 0.6 }),
        complete: new Howl({ src: ['../../assets/audio/win-Blockbusters.mp3'], volume: 0.7 }),
        
        // أصوات خاصة
        start: new Howl({ src: ['../../assets/audio/startapp.mp3'], volume: 0.5 }),
        welcome: new Howl({ src: ['../../assets/audio/name-start.mp3'], volume: 0.5 })
      },
      
      // حالة النظام
      enabled: true,
      
      // تشغيل صوت معين
      play(soundName) {
        if (!this.enabled || !this.sounds[soundName]) return;
        
        try {
          this.sounds[soundName].play();
        } catch (error) {
          console.log('تعذر تشغيل الصوت:', soundName);
        }
      },
      
      // تفعيل/إلغاء تفعيل النظام
      toggle() {
        this.enabled = !this.enabled;
        return this.enabled;
      },
      
      // تشغيل أصوات متتابعة
      sequence(sounds, delay = 500) {
        sounds.forEach((sound, index) => {
          setTimeout(() => this.play(sound), index * delay);
        });
      }
    };'''

def get_notification_system_code(lesson_topic):
    """إرجاع كود نظام الإشعارات حسب موضوع الدرس"""
    base_messages = {
        "cells": {
            "welcome": [
                "أهلاً وسهلاً {name}! مرحبًا بك في عالم الخلايا المثير! 🧬",
                "مرحبًا {name}! أنت على وشك اكتشاف أسرار الخلية! 🔬",
                "أهلاً {name}! دعنا نتعلم عن اللبنات الأساسية للحياة! ✨"
            ],
            "encouragement": [
                "رائع {name}! أنت تفهم الخلايا بشكل ممتاز! 🌟",
                "ممتاز {name}! معرفتك بالعضيات مذهلة! 💪",
                "أحسنت {name}! أنت عالم/ة خلايا حقيقي/ة! 🧠"
            ]
        },
        "transport": {
            "welcome": [
                "أهلاً وسهلاً {name}! مرحبًا بك في درس النقل والانتشار! 💧",
                "مرحبًا {name}! دعنا نتعلم كيف تتحرك المواد! 🚀",
                "أهلاً {name}! عالم النقل الخلوي في انتظارك! ⚡"
            ],
            "encouragement": [
                "رائع {name}! فهمك للانتشار والنقل ممتاز! 🌊",
                "ممتاز {name}! أنت تتقن مفاهيم النقل! 🎯",
                "أحسنت {name}! معرفتك بحركة المواد رائعة! 💫"
            ]
        },
        "biomolecules": {
            "welcome": [
                "أهلاً وسهلاً {name}! مرحبًا بك في عالم الجزيئات الحيوية! 🧪",
                "مرحبًا {name}! دعنا نكتشف لبنات الحياة الكيميائية! ⚗️",
                "أهلاً {name}! رحلة مثيرة في الكيمياء الحيوية تنتظرك! 🔬"
            ],
            "encouragement": [
                "رائع {name}! فهمك للبروتينات والكربوهيدرات ممتاز! 🧬",
                "ممتاز {name}! أنت كيميائي/ة حيوي/ة موهوب/ة! 🏆",
                "أحسنت {name}! معرفتك بالإنزيمات مدهشة! ⚡"
            ]
        },
        "nutrition": {
            "welcome": [
                "أهلاً وسهلاً {name}! مرحبًا بك في درس التغذية والتمثيل الضوئي! 🌱",
                "مرحبًا {name}! دعنا نتعلم كيف تصنع النباتات غذاءها! ☀️",
                "أهلاً {name}! عالم التمثيل الضوئي في انتظارك! 🍃"
            ],
            "encouragement": [
                "رائع {name}! فهمك للتمثيل الضوئي رائع! 🌟",
                "ممتاز {name}! أنت عالم/ة نبات ممتاز/ة! 🌿",
                "أحسنت {name}! معرفتك بالتغذية النباتية مميزة! 🌺"
            ]
        },
        "respiration": {
            "welcome": [
                "أهلاً وسهلاً {name}! مرحبًا بك في درس التنفس الخلوي! 💨",
                "مرحبًا {name}! دعنا نتعلم كيف تنتج الخلايا الطاقة! ⚡",
                "أهلاً {name}! رحلة في عالم إنتاج الطاقة تنتظرك! 🔋"
            ],
            "encouragement": [
                "رائع {name}! فهمك للتنفس والطاقة ممتاز! 🚀",
                "ممتاز {name}! أنت خبير/ة في الطاقة الخلوية! 💪",
                "أحسنت {name}! معرفتك بالتنفس مدهشة! ⭐"
            ]
        },
        "homeostasis": {
            "welcome": [
                "أهلاً وسهلاً {name}! مرحبًا بك في درس التوازن الداخلي! ⚖️",
                "مرحبًا {name}! دعنا نتعلم كيف يحافظ الجسم على توازنه! 🎯",
                "أهلاً {name}! عالم التنظيم والتوازن في انتظارك! 🧠"
            ],
            "encouragement": [
                "رائع {name}! فهمك للتوازن الداخلي ممتاز! 🌟",
                "ممتاز {name}! أنت خبير/ة في فيسيولوجيا الجسم! 🏆",
                "أحسنت {name}! معرفتك بالتنظيم الحيوي رائعة! ⚡"
            ]
        }
    }
    
    # رسائل عامة تصلح لجميع الدروس
    general_messages = '''
    // 🔔 نظام الإشعارات والرسائل التفاعلية الذكي
    const NotificationSystem = {
      student: null,
      
      // رسائل متنوعة حسب الأداء
      messages: {
        welcome: [
          "أهلاً وسهلاً {name}! مرحبًا بك في هذا الدرس المثير! 🧬",
          "مرحبًا {name}! أنت على وشك تعلم شيء رائع! 🔬",
          "أهلاً {name}! دعنا نتعلم العلوم معًا! ✨"
        ],
        
        encouragement: [
          "ممتاز {name}! أنت تتقدم بشكل رائع! 🌟",
          "أحسنت {name}! استمر على هذا الأداء المميز! 💪",
          "رائع {name}! أنت تبهرني بذكائك! 🧠",
          "عظيم {name}! كل إجابة تقربك من النجاح! 🎯"
        ],
        
        motivation: [
          "لا تستسلم {name}! المحاولة جزء من التعلم! 💚",
          "فكر مرة أخرى {name}، أنت أقرب للإجابة الصحيحة! 🤔",
          "المحاولة الجيدة {name}! التعلم من الأخطاء يجعلنا أقوى! 💎",
          "تركيزك يتحسن {name}! المحاولة القادمة ستكون أفضل! ⚡"
        ],
        
        milestone: [
          "🎉 ممتاز {name}! لقد أكملت 25% من الأسئلة!",
          "🚀 رائع {name}! وصلت لمنتصف الطريق - 50%!",
          "⭐ مذهل {name}! 75% مكتملة - أنت بطل/ة!",
          "🏆 تهانينا {name}! أكملت جميع الأسئلة بنجاح!"
        ],
        
        finalResults: {
          excellent: [
            "🏆 مذهل {name}! أداء استثنائي - أنت عالم/ة حقيقي/ة!",
            "⭐ رائع جداً {name}! إتقان كامل للموضوع!"
          ],
          good: [
            "👏 أحسنت {name}! أداء جيد جداً - استمر في التفوق!",
            "💪 عمل ممتاز {name}! أنت على الطريق الصحيح!"
          ],
          average: [
            "📚 أداء جيد {name}! مراجعة بسيطة وستكون في القمة!",
            "🎯 استمر {name}! أنت تتحسن مع كل محاولة!"
          ],
          needsWork: [
            "💚 لا بأس {name}! التعلم رحلة - استمر في المحاولة!",
            "🌱 كل خطأ فرصة للتعلم {name}! أنت في الطريق الصحيح!"
          ]
        }
      },
      
      // تحديد مستوى الأداء
      getPerformanceLevel(percentage) {
        if (percentage >= 90) return 'excellent';
        if (percentage >= 75) return 'good';
        if (percentage >= 60) return 'average';
        return 'needsWork';
      },
      
      // اختيار رسالة عشوائية
      getRandomMessage(category, percentage = null) {
        let messages = this.messages[category];
        if (percentage !== null && this.messages[category][this.getPerformanceLevel(percentage)]) {
          messages = this.messages[category][this.getPerformanceLevel(percentage)];
        }
        
        const randomMsg = messages[Math.floor(Math.random() * messages.length)];
        return randomMsg.replace('{name}', this.student?.name || 'البطل/ة');
      },
      
      // عرض إشعار ذكي
      showSmart(category, options = {}) {
        const message = this.getRandomMessage(category, options.percentage);
        
        Swal.fire({
          title: options.title || 'رسالة ذكية 🤖',
          text: message,
          icon: options.icon || 'info',
          timer: options.timer || 3000,
          timerProgressBar: true,
          showConfirmButton: false,
          toast: options.toast || true,
          position: options.position || 'top-end',
          customClass: {
            popup: 'animated-notification'
          }
        });
        
        // تشغيل صوت مناسب
        if (options.sound) {
          SoundSystem.play(options.sound);
        }
      }
    };'''
    
    return general_messages

def get_performance_variables():
    """إرجاع متغيرات تتبع الأداء"""
    return '''
    // متغيرات الأداء والتفاعل الذكي
    let totalAnswered = 0;
    let consecutiveCorrect = 0;
    let startTime = Date.now();'''

def get_enhanced_askstudent():
    """إرجاع دالة askStudent محسنة"""
    return '''      if(formValues){
        setStudent(formValues);
        NotificationSystem.student = formValues;
        updateMeta();
        
        // تشغيل صوت البداية والترحيب
        SoundSystem.play('start');
        
        setTimeout(() => {
          NotificationSystem.showSmart('welcome', {
            title: 'مرحباً بك! 👋',
            icon: 'success',
            timer: 4000,
            sound: 'welcome'
          });
        }, 1000);
        
        el.quiz.style.display = "block";
        gsap.from("#quiz .q", {opacity:0, y:10, stagger:.08, duration:.5});
        
        // إعادة تعيين متغيرات الأداء
        totalAnswered = 0;
        consecutiveCorrect = 0;
        startTime = Date.now();
      }'''

def get_enhanced_click_handler():
    """إرجاع معالج النقر المحسن"""
    return '''    // نظام الإجابة المحسن مع الذكاء الاصطناعي
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
        if (consecutiveCorrect >= 3) {
          setTimeout(() => {
            NotificationSystem.showSmart('encouragement', {
              title: 'أداء رائع! 🔥',
              icon: 'success',
              timer: 2500
            });
          }, 800);
          consecutiveCorrect = 0; // إعادة تعيين العداد
        }
        
      } else {
        choice.classList.add('wrong');
        consecutiveCorrect = 0;
        SoundSystem.play('wrong');
        
        // تأثير بصري للإجابة الخاطئة
        gsap.fromTo(choice, {x:0}, {x:-8, duration:.08, yoyo:true, repeat:6, ease: "power2.inOut"});
        
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
    });'''

def get_milestone_function():
    """إرجاع دالة فحص المعالم"""
    return '''    
    // فحص النقاط المهمة في التقدم
    function checkMilestones(percentage, questionCount, totalQuestions) {
      const milestones = [25, 50, 75, 100];
      const reached = milestones.find(m => percentage >= m && 
        questionCount === Math.ceil(totalQuestions * m / 100));
      
      if (reached && questionCount === Math.ceil(totalQuestions * reached / 100)) {
        setTimeout(() => {
          NotificationSystem.showSmart('milestone', {
            title: reached === 100 ? '🏆 مكتمل!' : `🎯 ${reached}% مكتمل!`,
            icon: 'success',
            timer: 3000,
            sound: reached === 100 ? 'complete' : 'milestone'
          });
        }, 500);
      }
    }'''

def get_enhanced_updateprogress():
    """إرجاع دالة updateProgress محسنة"""
    return '''    // تحديث شريط التقدّم مع تتبع المعالم المهمة
    function updateProgress(){
      const total = document.querySelectorAll('.q[data-qid]').length;
      const answered = Array.from(document.querySelectorAll('.q')).filter(q => 
        q.querySelector('.choice.correct, .choice.wrong')
      ).length;
      
      const oldProgress = parseInt(el.done.textContent) || 0;
      
      el.total.textContent = total;
      el.done.textContent = answered;
      const percentage = Math.round((answered/total)*100);
      el.bar.style.width = percentage + '%';
      
      // تشغيل صوت التقدم عند الإجابة
      if (answered > oldProgress && answered > 0) {
        SoundSystem.play('progress');
        
        // فحص المعالم المهمة
        checkMilestones(percentage, answered, total);
      }
    }'''

def get_mouse_sounds():
    """إرجاع كود أصوات الفأرة"""
    return '''    // إضافة أصوات للأزرار وتأثيرات تفاعلية
    document.addEventListener('DOMContentLoaded', () => {
      document.querySelectorAll('.choice').forEach(choice => {
        choice.addEventListener('mouseenter', () => {
          SoundSystem.play('select');
        });
      });
    });'''

def enhance_lesson(file_path):
    """تحسين ملف درس واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # التحقق من وجود النظام مسبقاً
        if 'SoundSystem' in content and 'NotificationSystem' in content:
            print(f"✅ {file_path} - الأنظمة موجودة مسبقاً")
            return False
            
        # إنشاء نسخة احتياطية
        backup_path = file_path + '.backup_smart_system'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 1. إضافة مكتبة Howler.js إذا لم تكن موجودة
        if 'howler' not in content:
            content = content.replace(
                '<script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>',
                '<script src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js"></script>\n  <script src="https://cdn.jsdelivr.net/npm/howler@2.2.4/dist/howler.min.js"></script>'
            )
        
        # 2. إضافة النظام الصوتي بعد AOS.init
        aos_pattern = r'AOS\.init\(\s*{\s*duration:\s*700,\s*once:\s*true\s*}\s*\);'
        if re.search(aos_pattern, content):
            content = re.sub(
                aos_pattern,
                f'AOS.init({{ duration: 700, once: true }});{get_sound_system_code()}',
                content
            )
        
        # 3. إضافة نظام الإشعارات
        lesson_topic = "general"  # يمكن تحسينه لاحقاً حسب الدرس
        sound_system_end = content.find('};', content.find('SoundSystem'))
        if sound_system_end != -1:
            insert_pos = sound_system_end + 2
            content = content[:insert_pos] + get_notification_system_code(lesson_topic) + content[insert_pos:]
        
        # 4. إضافة متغيرات الأداء
        storage_key_pos = content.find('const storageKey')
        if storage_key_pos != -1:
            content = content.replace(
                'const storageKey = "watyn_bio_student";',
                f'const storageKey = "watyn_bio_student";{get_performance_variables()}'
            )
        
        # 5. تحسين دالة askStudent
        askstudent_pattern = r'if\(formValues\)\{\s*setStudent\(formValues\);\s*updateMeta\(\);\s*el\.quiz\.style\.display\s*=\s*"block";\s*gsap\.from\("#quiz \.q",\s*\{[^}]+\}\);\s*\}'
        if re.search(askstudent_pattern, content, re.DOTALL):
            content = re.sub(
                askstudent_pattern,
                get_enhanced_askstudent(),
                content,
                flags=re.DOTALL
            )
        
        # 6. تحسين معالج النقر
        click_pattern = r'document\.addEventListener\(\'click\',\s*\(e\)\s*=>\s*\{[^}]+choice\.dataset\.correct[^}]+updateProgress\(\);\s*\}\);'
        if re.search(click_pattern, content, re.DOTALL):
            content = re.sub(
                click_pattern,
                get_enhanced_click_handler(),
                content,
                flags=re.DOTALL
            )
        
        # 7. تحسين دالة updateProgress
        update_progress_pattern = r'function updateProgress\(\)\{[^}]+el\.bar\.style\.width[^}]+\}'
        if re.search(update_progress_pattern, content, re.DOTALL):
            content = re.sub(
                update_progress_pattern,
                get_enhanced_updateprogress(),
                content,
                flags=re.DOTALL
            )
        
        # 8. إضافة دالة المعالم
        computescore_pos = content.find('function computeScore(){')
        if computescore_pos != -1:
            content = content[:computescore_pos] + get_milestone_function() + '\n\n    ' + content[computescore_pos:]
        
        # 9. إضافة أصوات الفأرة
        start_listener_pos = content.find('el.start.addEventListener')
        if start_listener_pos != -1:
            content = content[:start_listener_pos] + get_mouse_sounds() + '\n\n    ' + content[start_listener_pos:]
        
        # 10. تحسين رسالة النتائج النهائية
        result_pattern = r'title:\s*\'أحسنت يا بطل/ة!\s*🎉\','
        if re.search(result_pattern, content):
            enhanced_result = '''// رسالة نتائج ذكية مخصصة
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
            <div style="text-align:right;line-height:1.9">
              <div><strong>👤 الاسم:</strong> ${s?.name || '-'}</div>
              <div><strong>🏫 الصف:</strong> ${s?.klass || '-'}</div>
              <div><strong>📊 النتيجة:</strong> ${correct} من ${total} سؤال</div>
              <div><strong>📈 النسبة المئوية:</strong> ${percent}%</div>
              <hr style="margin: 15px 0;">
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
            window.location.href='../../index.html';
          }
        });'''
            
            # البحث عن بداية Swal.fire وتبديله
            swal_start = content.find('Swal.fire({')
            if swal_start != -1:
                swal_end = content.find('});', swal_start) + 3
                content = content[:swal_start] + enhanced_result[enhanced_result.find('Swal.fire'):] + content[swal_end:]
        
        # حفظ الملف المحدث
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"🔧 {file_path} - تم تطبيق الأنظمة الذكية")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في معالجة {file_path}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء تطبيق النظام الصوتي الذكي ونظام الإشعارات...")
    print("=" * 70)
    
    # البحث عن جميع ملفات الدروس
    lesson_pattern = "unit-*/lesson-*/index.html"
    lesson_files = glob.glob(lesson_pattern)
    
    if not lesson_files:
        print("❌ لم يتم العثور على ملفات الدروس!")
        return
    
    print(f"📁 تم العثور على {len(lesson_files)} ملف درس")
    print()
    
    enhanced_count = 0
    
    # معالجة كل ملف
    for file_path in sorted(lesson_files):
        if enhance_lesson(file_path):
            enhanced_count += 1
    
    print()
    print("=" * 70)
    print(f"✅ تم الانتهاء! تم تطبيق الأنظمة الذكية على {enhanced_count} درس")
    
    if enhanced_count > 0:
        print()
        print("🎯 المميزات المضافة:")
        print("   🎵 النظام الصوتي الذكي (8 أصوات مختلفة)")
        print("   🔔 نظام الإشعارات والرسائل التفاعلية")
        print("   🧠 الذكاء الاصطناعي للتحفيز والتشجيع")
        print("   📊 تتبع الأداء والمعالم المهمة")
        print("   ✨ تأثيرات بصرية محسنة")
        print("   🎯 رسائل نتائج ذكية مخصصة")
        print()
        print("🚀 الخطوات التالية:")
        print("   1. اختبر الدروس في المتصفح")
        print("   2. ارفع التغييرات على GitHub")
        print("   3. النسخ الاحتياطية محفوظة بامتداد .backup_smart_system")

if __name__ == "__main__":
    main()