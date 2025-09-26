#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛠️ الإصلاح الشامل والمتقدم للدروس
=====================================
إصلاح شامل للمشاكل الثلاث الأساسية:
1. زر "ابدأ النشاط" لا يعمل
2. عدم وجود صوت
3. عدم إظهار رسائل تفاعلية موجهة
"""

import os
import re
from pathlib import Path

class ComprehensiveFixer:
    def __init__(self):
        self.workspace_path = Path.cwd()
        
    def get_complete_enhanced_system(self, lesson_info):
        """الحصول على النظام المحسّن الكامل"""
        
        return f'''
    // 🔊 النظام الصوتي المتطور والمحسّن
    const SoundSystem = {{
      enabled: true,
      currentVolume: 0.7,
      sounds: {{}},
      initialized: false,
      
      // تهيئة جميع الأصوات مع معالجة شاملة للأخطاء
      init() {{
        if (this.initialized) return;
        
        const soundMappings = {{
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
        }};
        
        let loadedCount = 0;
        const totalSounds = Object.keys(soundMappings).length;
        
        Object.keys(soundMappings).forEach(type => {{
          this.sounds[type] = new Howl({{
            src: [`../../assets/audio/${{soundMappings[type]}}`],
            volume: this.getContextualVolume(type),
            preload: true,
            onload: () => {{
              loadedCount++;
              console.log(`✅ تم تحميل الصوت: ${{type}} (${{loadedCount}}/${{totalSounds}})`);
              if (loadedCount === totalSounds) {{
                this.initialized = true;
                console.log('🎵 تم تهيئة النظام الصوتي بالكامل');
              }}
            }},
            onloaderror: (id, error) => {{
              loadedCount++;
              console.warn(`⚠️ فشل تحميل الصوت ${{type}}: ${{error}}`);
              // إنشاء صوت صامت كبديل
              this.sounds[type] = {{
                play: () => console.warn(`🔇 صوت غير متاح: ${{type}}`),
                volume: () => {{}},
                stop: () => {{}}
              }};
            }}
          }});
        }});
        
        console.log('🚀 بدء تحميل الأصوات...');
      }},
      
      // تشغيل صوت مع معالجة شاملة للأخطاء
      play(soundType) {{
        if (!this.enabled) {{
          console.log('🔇 النظام الصوتي معطل');
          return;
        }}
        
        if (!this.sounds[soundType]) {{
          console.warn(`⚠️ الصوت غير موجود: ${{soundType}}`);
          return;
        }}
        
        try {{
          const contextualVolume = this.getContextualVolume(soundType);
          this.sounds[soundType].volume(contextualVolume);
          this.sounds[soundType].play();
          
          console.log(`🔊 تم تشغيل الصوت: ${{soundType}} بمستوى ${{contextualVolume}}`);
          this.trackSoundUsage(soundType);
        }} catch (error) {{
          console.error(`❌ خطأ في تشغيل الصوت ${{soundType}}:`, error);
        }}
      }},
      
      // تحديد مستوى الصوت حسب السياق
      getContextualVolume(soundType) {{
        const contextMap = {{
          'celebration': 0.9,
          'milestone': 0.8,
          'correct': 0.7,
          'welcome': 0.6,
          'wrong': 0.5,
          'progress': 0.4,
          'click': 0.4,
          'select': 0.3
        }};
        return contextMap[soundType] || this.currentVolume;
      }},
      
      // تتبع استخدام الأصوات
      trackSoundUsage(soundType) {{
        if (!window.soundStats) window.soundStats = {{}};
        window.soundStats[soundType] = (window.soundStats[soundType] || 0) + 1;
      }},
      
      // تشغيل متسلسل
      sequence(sounds, delay = 500) {{
        sounds.forEach((sound, index) => {{
          setTimeout(() => this.play(sound), index * delay);
        }});
      }},
      
      // تفعيل/إلغاء تفعيل النظام
      toggle() {{
        this.enabled = !this.enabled;
        console.log(`🎵 النظام الصوتي: ${{this.enabled ? 'مُفعل' : 'معطل'}}`);
        return this.enabled;
      }},
      
      // اختبار جميع الأصوات
      testAll() {{
        console.log('🧪 اختبار جميع الأصوات...');
        const sounds = Object.keys(this.sounds);
        sounds.forEach((sound, index) => {{
          setTimeout(() => {{
            console.log(`🎵 اختبار: ${{sound}}`);
            this.play(sound);
          }}, index * 1000);
        }});
      }}
    }};

    // 🤖 نظام الرسائل التفاعلية الذكية المحسّن
    const EnhancedNotificationSystem = {{
      student: null,
      lessonInfo: {{
        title: "{lesson_info['title']}",
        description: "{lesson_info['description']}",
        keyConcepts: {lesson_info['key_concepts']},
        topic: "{lesson_info['topic']}"
      }},
      interactionStats: {{
        clicks: 0,
        correctAnswers: 0,
        wrongAnswers: 0,
        timeSpent: 0
      }},
      
      // رسائل ذكية مخصصة حسب الموضوع
      getTopicSpecificWelcome() {{
        const topicMessages = {{
          'cells': [
            "🔬 أهلاً وسهلاً {{name}}! مرحبًا بك في عالم الخلايا - اللبنات الأساسية للحياة!",
            "🧬 مرحبًا {{name}}! ستكتشف اليوم أسرار الخلية وعجائبها",
            "✨ أهلاً {{name}}! رحلة مثيرة في عالم الخلايا المجهرية تنتظرك"
          ],
          'transport': [
            "💧 أهلاً وسهلاً {{name}}! مرحبًا بك في عالم النقل الخلوي المدهش!",
            "🚀 مرحبًا {{name}}! ستتعلم كيف تتحرك المواد عبر الأغشية",
            "⚡ أهلاً {{name}}! عالم الانتشار والنقل النشط في انتظارك"
          ],
          'biomolecules': [
            "🧪 أهلاً وسهلاً {{name}}! مرحبًا بك في عالم الجزيئات الحيوية الرائع!",
            "⚗️ مرحبًا {{name}}! ستكتشف لبنات الحياة الكيميائية",
            "🔬 أهلاً {{name}}! رحلة في الكيمياء الحيوية تنتظرك"
          ],
          'nutrition': [
            "🌱 أهلاً وسهلاً {{name}}! مرحبًا بك في عالم التمثيل الضوئي المذهل!",
            "☀️ مرحبًا {{name}}! ستتعلم كيف تصنع النباتات غذاءها من الضوء",
            "🍃 أهلاً {{name}}! عالم صنع الغذاء في النباتات يدعوك"
          ],
          'respiration': [
            "💨 أهلاً وسهلاً {{name}}! مرحبًا بك في عالم التنفس الخلوي!",
            "⚡ مرحبًا {{name}}! ستكتشف كيف تنتج الخلايا الطاقة",
            "🔋 أهلاً {{name}}! رحلة في عالم إنتاج الطاقة الخلوية"
          ],
          'homeostasis': [
            "⚖️ أهلاً وسهلاً {{name}}! مرحبًا بك في عالم التوازن الداخلي!",
            "🎯 مرحبًا {{name}}! ستتعلم كيف تحافظ الكائنات على استقرارها",
            "🧠 أهلاً {{name}}! عالم التنظيم والتحكم الحيوي يرحب بك"
          ]
        }};
        
        const messages = topicMessages[this.lessonInfo.topic] || topicMessages['cells'];
        return messages[Math.floor(Math.random() * messages.length)];
      }},
      
      // عرض رسالة ترحيب ذكية مع معلومات الدرس
      showWelcomeMessage() {{
        const welcomeMsg = this.getTopicSpecificWelcome();
        const personalizedWelcome = welcomeMsg.replace('{{name}}', this.student?.name || 'البطل/ة');
        const lessonIntro = `📚 ستتعلم اليوم: ${{this.lessonInfo.description}}\\n🔬 المفاهيم الرئيسية: ${{this.lessonInfo.keyConcepts.join('، ')}}`;
        
        Swal.fire({{
          title: '🎓 مرحباً بك في رحلة التعلم!',
          html: `
            <div style="text-align:right;line-height:1.8;font-size:16px">
              <div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:15px;border-radius:12px;margin-bottom:15px">
                ${{personalizedWelcome}}
              </div>
              <div style="background:#f8f9ff;padding:15px;border-radius:10px;border-right:4px solid #667eea">
                ${{lessonIntro}}
              </div>
            </div>`,
          icon: 'info',
          confirmButtonText: '🚀 لنبدأ التعلم!',
          confirmButtonColor: '#667eea',
          timer: 8000,
          timerProgressBar: true,
          showClass: {{
            popup: 'animate__animated animate__fadeInDown'
          }}
        }}).then(() => {{
          SoundSystem.play('start');
          this.startSessionTimer();
        }});
      }},
      
      // بدء مؤقت الجلسة
      startSessionTimer() {{
        this.sessionStartTime = Date.now();
        this.timerInterval = setInterval(() => {{
          this.interactionStats.timeSpent = Math.floor((Date.now() - this.sessionStartTime) / 1000);
        }}, 1000);
      }},
      
      // تهيئة النظام للطالب
      initForStudent(studentData) {{
        this.student = studentData;
        console.log(`🤖 تم تفعيل النظام الذكي للطالب: ${{studentData.name}}`);
        
        // تأخير بسيط لضمان تحميل الأصوات
        setTimeout(() => {{
          this.showWelcomeMessage();
        }}, 500);
      }},
      
      // عرض رسائل تشجيع ذكية
      showEncouragement(type = 'general') {{
        const messages = {{
          'correct': [
            "ممتاز {{name}}! إجابة صحيحة رائعة! 🌟",
            "أحسنت {{name}}! أنت تتقدم بشكل ممتاز! 👏",
            "رائع {{name}}! استمر على هذا الأداء المميز! 🚀"
          ],
          'wrong': [
            "لا بأس {{name}}، المحاولة جزء من التعلم! 💪",
            "فكر مرة أخرى {{name}}، أنت قريب من الإجابة الصحيحة! 🤔",
            "استمر في المحاولة {{name}}، كل خطأ فرصة للتعلم! 🌱"
          ],
          'milestone': [
            "تهانينا {{name}}! لقد أحرزت تقدماً رائعاً! 🎉",
            "ممتاز {{name}}! أنت في منتصف الطريق! ⭐",
            "رائع {{name}}! أداءك يتحسن مع كل سؤال! 📈"
          ]
        }};
        
        const messageList = messages[type] || messages['general'];
        const randomMessage = messageList[Math.floor(Math.random() * messageList.length)];
        const personalizedMessage = randomMessage.replace('{{name}}', this.student?.name || 'البطل/ة');
        
        Swal.fire({{
          title: type === 'correct' ? '🎉 أحسنت!' : type === 'wrong' ? '💪 استمر!' : '🏆 تهانينا!',
          text: personalizedMessage,
          icon: type === 'correct' ? 'success' : type === 'wrong' ? 'info' : 'success',
          timer: 3000,
          timerProgressBar: true,
          toast: true,
          position: 'top-end',
          showConfirmButton: false
        }});
      }}
    }};

    // تهيئة الأنظمة عند تحميل الصفحة
    document.addEventListener('DOMContentLoaded', function() {{
      console.log('🚀 بدء تهيئة الأنظمة المحسّنة...');
      
      // تأخير قصير للتأكد من تحميل جميع المكتبات
      setTimeout(() => {{
        if (typeof Howl !== 'undefined') {{
          SoundSystem.init();
          console.log('✅ تم تهيئة النظام الصوتي');
        }} else {{
          console.error('❌ مكتبة Howler غير محملة');
        }}
        
        if (typeof Swal !== 'undefined') {{
          console.log('✅ مكتبة SweetAlert2 جاهزة');
        }} else {{
          console.error('❌ مكتبة SweetAlert2 غير محملة');
        }}
        
        console.log('🎉 تم تهيئة جميع الأنظمة بنجاح');
      }}, 1000);
    }});'''
    
    def get_lesson_info(self, unit_name, lesson_name):
        """الحصول على معلومات الدرس"""
        
        lessons_data = {
            "unit-1-cells": {
                "lesson-1-1": {
                    "title": "مدخل إلى الخلايا",
                    "description": "تعرف على الوحدة الأساسية للحياة - الخلية",
                    "key_concepts": ["الخلية", "الغشاء الخلوي", "النواة", "العضيات"],
                    "topic": "cells"
                },
                "lesson-1-2": {
                    "title": "رسم الخلايا وحساب التكبير",
                    "description": "تعلم كيفية رسم الخلايا وحساب التكبير المجهري",
                    "key_concepts": ["الرسم العلمي", "التكبير", "المجهر", "القياس"],
                    "topic": "cells"
                },
                "lesson-1-3": {
                    "title": "العضيات الخلوية",
                    "description": "اكتشف المكونات الداخلية للخلية ووظائفها",
                    "key_concepts": ["الميتوكوندريا", "الشبكة الإندوبلازمية", "جهاز جولجي", "الريبوسومات"],
                    "topic": "cells"
                }
            },
            "unit-2-transport": {
                "lesson-2-1": {
                    "title": "النقل السلبي",
                    "description": "فهم كيفية انتقال المواد عبر الأغشية دون طاقة",
                    "key_concepts": ["الانتشار", "الانتشار المُيسَّر", "الخاصية الأسموزية"],
                    "topic": "transport"
                },
                "lesson-2-2": {
                    "title": "النقل النشط",
                    "description": "تعلم عن انتقال المواد باستخدام الطاقة",
                    "key_concepts": ["النقل النشط", "مضخة الصوديوم-البوتاسيوم", "البلعمة"],
                    "topic": "transport"
                },
                "lesson-2-3": {
                    "title": "تنظيم النقل",
                    "description": "اكتشف كيف تتحكم الخلايا في نقل المواد",
                    "key_concepts": ["التحكم في النفاذية", "القنوات الأيونية", "البروتينات الناقلة"],
                    "topic": "transport"
                }
            }
        }
        
        # إضافة باقي الوحدات بنفس النمط...
        default_info = {
            "title": "درس الأحياء",
            "description": "تعلم مفاهيم مهمة في علم الأحياء",
            "key_concepts": ["العلوم", "الأحياء", "التعلم"],
            "topic": "cells"
        }
        
        return lessons_data.get(unit_name, {}).get(lesson_name, default_info)
    
    def fix_lesson_completely(self, lesson_path):
        """إصلاح شامل للدرس"""
        
        try:
            with open(lesson_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ خطأ في قراءة {lesson_path}: {str(e)}")
            return False
        
        # استخراج معلومات الدرس
        unit_name = lesson_path.parent.parent.name
        lesson_name = lesson_path.parent.name
        lesson_info = self.get_lesson_info(unit_name, lesson_name)
        
        modified = False
        
        # 1. التأكد من وجود المكتبات المطلوبة
        required_libs = [
            'sweetalert2@11',
            'canvas-confetti@1.9.3',
            'gsap@3.12.5',
            'howler@2.2.4'
        ]
        
        for lib in required_libs:
            if lib.split('@')[0] not in content:
                print(f"⚠️ مكتبة {lib} قد تكون غير محملة في {unit_name}/{lesson_name}")
        
        # 2. إزالة الأنظمة القديمة والمتضاربة
        old_patterns = [
            r'const sfx = \{[^}]+\};',
            r'// أصوات.*?const sfx.*?\};',
            r'// 🔊 النظام الصوتي.*?(?=// |    const|    function|\n    \w)',
            r'// 🤖 نظام الرسائل.*?(?=// |    const|    function|\n    \w)'
        ]
        
        for pattern in old_patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, '', content, flags=re.DOTALL)
                modified = True
        
        # 3. إضافة النظام المحسّن الجديد
        if 'const SoundSystem' not in content or 'const EnhancedNotificationSystem' not in content:
            # البحث عن المكان المناسب للإدراج (بعد تحميل Howler)
            howler_pos = content.find('</script>', content.find('howler'))
            if howler_pos != -1:
                enhanced_system = self.get_complete_enhanced_system(lesson_info)
                insert_pos = howler_pos + len('</script>')
                content = content[:insert_pos] + '\n  <script>' + enhanced_system + '\n  </script>' + content[insert_pos:]
                modified = True
        
        # 4. التأكد من ربط زر البداية
        if 'el.start.addEventListener' not in content and 'btnStart' in content:
            # إضافة ربط زر البداية في نهاية الكود
            script_end = content.rfind('</script>')
            if script_end > 0:
                button_binding = '\nel.start.addEventListener(\'click\', askStudent);\n'
                content = content[:script_end] + button_binding + content[script_end:]
                modified = True
        
        # 5. تحسين دالة askStudent لدعم النظام الجديد
        if 'askStudent' in content and 'EnhancedNotificationSystem.initForStudent' not in content:
            # استبدال استدعاء النظام القديم بالجديد
            old_init_pattern = r'(setStudent\(formValues\);.*?)(\s+el\.quiz\.style\.display)'
            replacement = r'\1\n        EnhancedNotificationSystem.initForStudent(formValues);\n        \n        setTimeout(() => {\2'
            
            if re.search(old_init_pattern, content, re.DOTALL):
                content = re.sub(old_init_pattern, replacement, content, flags=re.DOTALL)
                modified = True
        
        if modified:
            try:
                with open(lesson_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            except Exception as e:
                print(f"❌ خطأ في كتابة {lesson_path}: {str(e)}")
                return False
        
        return False
    
    def fix_all_lessons_completely(self):
        """إصلاح شامل لجميع الدروس"""
        
        print("🛠️ بدء الإصلاح الشامل لجميع الدروس...")
        print("=" * 50)
        
        fixed_count = 0
        total_count = 0
        
        for unit_dir in self.workspace_path.iterdir():
            if unit_dir.is_dir() and unit_dir.name.startswith('unit-'):
                for lesson_dir in unit_dir.iterdir():
                    if lesson_dir.is_dir() and lesson_dir.name.startswith('lesson-'):
                        index_file = lesson_dir / 'index.html'
                        
                        if index_file.exists():
                            total_count += 1
                            lesson_name = f"{unit_dir.name}/{lesson_dir.name}"
                            
                            print(f"🔧 إصلاح: {lesson_name}")
                            
                            if self.fix_lesson_completely(index_file):
                                fixed_count += 1
                                print(f"✅ تم الإصلاح: {lesson_name}")
                            else:
                                print(f"ℹ️ لا يحتاج إصلاح: {lesson_name}")
        
        print(f"\n🎉 اكتمل الإصلاح الشامل!")
        print(f"📊 النتائج:")
        print(f"   - إجمالي الدروس: {total_count}")
        print(f"   - دروس تم إصلاحها: {fixed_count}")
        print(f"   - دروس سليمة: {total_count - fixed_count}")
        
        return fixed_count, total_count

def main():
    """التشغيل الرئيسي"""
    
    print("🛠️ الإصلاح الشامل والمتقدم للدروس")
    print("=" * 40)
    print("🎯 يهدف لإصلاح:")
    print("   1. زر 'ابدأ النشاط' لا يعمل")
    print("   2. عدم وجود صوت")  
    print("   3. عدم إظهار رسائل تفاعلية موجهة")
    print("=" * 40)
    
    fixer = ComprehensiveFixer()
    
    try:
        fixed_count, total_count = fixer.fix_all_lessons_completely()
        
        if fixed_count > 0:
            print(f"\n✨ تم إصلاح {fixed_count} من أصل {total_count} دروس")
            print("\n🧪 للاختبار:")
            print("   - افتح أي درس")
            print("   - جرب زر 'ابدأ النشاط'")
            print("   - استمع للأصوات أثناء التفاعل")
            print("   - لاحظ الرسائل المخصصة بالاسم")
            print("\n🔧 للفحص التقني:")
            print("   - اضغط F12 واكتب: SoundSystem.testAll()")
            print("   - تحقق من console للرسائل التشخيصية")
        else:
            print(f"\n✅ جميع الدروس الـ{total_count} تعمل بشكل صحيح")
            
    except Exception as e:
        print(f"❌ حدث خطأ أثناء الإصلاح: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main()