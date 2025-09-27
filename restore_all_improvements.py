#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 مدير استعادة التحسينات الشاملة
==================================
يستعيد جميع التحسينات بعد استعادة النسخة الاحتياطية:
✅ الأسئلة المتخصصة من مجلد Q
✅ الأهداف التعليمية المتخصصة  
✅ شريط التقدم والإشعارات الذكية
✅ الأنظمة التفاعلية المحسنة
"""

import os
import json
import re
from pathlib import Path

class ComprehensiveRestorer:
    def __init__(self):
        self.base_dir = Path('.')
        self.q_dir = Path('./Q')
        self.stats = {
            'lessons_updated': 0,
            'questions_restored': 0,
            'objectives_restored': 0,
            'systems_updated': 0
        }
        
        # تعريفات الدروس المتقدمة
        self.lessons = {
            'unit-1-cells/lesson-1-1': '🔬 الخلية ومكوناتها',
            'unit-1-cells/lesson-1-2': '🧪 أنواع الخلايا',
            'unit-1-cells/lesson-1-3': '🔍 تقسيم الخلايا',
            'unit-2-transport/lesson-2-1': '🚛 النقل عبر الغشاء',
            'unit-2-transport/lesson-2-2': '💧 النقل المائي',
            'unit-2-transport/lesson-2-3': '⚡ النقل النشط',
            'unit-3-biomolecules/lesson-3-1': '🧬 الكربوهيدرات',
            'unit-3-biomolecules/lesson-3-2': '🧪 البروتينات',
            'unit-3-biomolecules/lesson-3-3': '⚗️ الدهون والأحماض النووية',
            'unit-4-nutrition/lesson-4-1': '🍎 التغذية والهضم',
            'unit-4-nutrition/lesson-4-2': '🔄 الامتصاص والأيض',
            'unit-5-respiration/lesson-5-1': '💨 التنفس الخلوي',
            'unit-6-homeostasis/lesson-6-1': '⚖️ الاتزان الداخلي',
            'unit-6-homeostasis/lesson-6-2': '🌡️ تنظيم درجة الحرارة',
            'unit-6-homeostasis/lesson-6-3': '🍬 تنظيم السكر',
            'unit-6-homeostasis/lesson-6-4': '🧠 الجهاز العصبي'
        }

    def extract_specialized_questions(self, q_file_path):
        """استخراج الأسئلة المتخصصة من مجلد Q"""
        if not q_file_path.exists():
            return []
            
        try:
            with open(q_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # البحث عن قائمة الأسئلة
            questions_match = re.search(r'const\s+questions\s*=\s*\[(.*?)\];', content, re.DOTALL)
            if not questions_match:
                return []
            
            questions_content = questions_match.group(1)
            questions = []
            
            # استخراج كل سؤال
            question_pattern = r'\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'
            for match in re.finditer(question_pattern, questions_content):
                question_text = match.group(1)
                
                # استخراج التفاصيل
                question_match = re.search(r'question:\s*["\']([^"\']*)["\']', question_text)
                answers_match = re.search(r'answers:\s*\[(.*?)\]', question_text, re.DOTALL)
                correct_match = re.search(r'correct:\s*(\d+)', question_text)
                
                if question_match and answers_match and correct_match:
                    # استخراج الإجابات
                    answers_text = answers_match.group(1)
                    answers = re.findall(r'["\']([^"\']*)["\']', answers_text)
                    
                    questions.append({
                        'question': question_match.group(1),
                        'answers': answers,
                        'correct': int(correct_match.group(1))
                    })
            
            return questions
        except Exception as e:
            print(f"⚠️ خطأ في استخراج الأسئلة من {q_file_path}: {e}")
            return []

    def extract_specialized_objectives(self, q_file_path):
        """استخراج الأهداف التعليمية المتخصصة من مجلد Q"""
        if not q_file_path.exists():
            return []
            
        try:
            with open(q_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # البحث عن قسم الأهداف
            objectives_pattern = r'<div[^>]*class="[^"]*objectives[^"]*"[^>]*>.*?<ul[^>]*>(.*?)</ul>'
            objectives_match = re.search(objectives_pattern, content, re.DOTALL | re.IGNORECASE)
            
            if not objectives_match:
                return []
            
            objectives_content = objectives_match.group(1)
            objectives = []
            
            # استخراج كل هدف
            objective_pattern = r'<li[^>]*>(.*?)</li>'
            for match in re.finditer(objective_pattern, objectives_content, re.DOTALL):
                objective_text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                if objective_text:
                    objectives.append(objective_text)
            
            return objectives
        except Exception as e:
            print(f"⚠️ خطأ في استخراج الأهداف من {q_file_path}: {e}")
            return []

    def update_lesson_questions(self, lesson_path, questions):
        """تحديث أسئلة الدرس"""
        if not questions:
            return False
            
        try:
            with open(lesson_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # تحويل الأسئلة إلى JavaScript
            js_questions = []
            for q in questions:
                answers_str = ', '.join([f'"{answer}"' for answer in q['answers']])
                js_questions.append(f'''        {{
            question: "{q['question']}",
            answers: [{answers_str}],
            correct: {q['correct']}
        }}''')
            
            questions_js = ',\n'.join(js_questions)
            new_questions_block = f"    const questions = [\n{questions_js}\n    ];"
            
            # البحث عن قائمة الأسئلة الحالية واستبدالها
            questions_pattern = r'const\s+questions\s*=\s*\[.*?\];'
            if re.search(questions_pattern, content, re.DOTALL):
                content = re.sub(questions_pattern, new_questions_block, content, flags=re.DOTALL)
            else:
                # إضافة الأسئلة قبل نهاية الـ script
                script_end = content.rfind('</script>')
                if script_end != -1:
                    content = content[:script_end] + f"\n    // الأسئلة المتخصصة\n{new_questions_block}\n\n" + content[script_end:]
            
            with open(lesson_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        except Exception as e:
            print(f"⚠️ خطأ في تحديث أسئلة {lesson_path}: {e}")
            return False

    def update_lesson_objectives(self, lesson_path, objectives):
        """تحديث أهداف الدرس"""
        if not objectives:
            return False
            
        try:
            with open(lesson_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # إنشاء HTML للأهداف
            objectives_html = '\n'.join([f'                <li class="objective-item">{obj}</li>' for obj in objectives])
            new_objectives_section = f'''            <div class="objectives-section">
                <h3><i class="fas fa-target"></i> 🎯 أهداف الدرس</h3>
                <ul class="objectives-list">
{objectives_html}
                </ul>
            </div>'''
            
            # البحث عن قسم الأهداف الحالي واستبدالها
            objectives_pattern = r'<div[^>]*class="[^"]*objectives[^"]*"[^>]*>.*?</div>'
            if re.search(objectives_pattern, content, re.DOTALL | re.IGNORECASE):
                content = re.sub(objectives_pattern, new_objectives_section, content, flags=re.DOTALL | re.IGNORECASE)
            else:
                # إضافة الأهداف بعد العنوان الرئيسي
                main_title_pattern = r'(<h1[^>]*>.*?</h1>)'
                if re.search(main_title_pattern, content, re.DOTALL):
                    content = re.sub(main_title_pattern, r'\1\n        ' + new_objectives_section, content, flags=re.DOTALL)
            
            with open(lesson_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        except Exception as e:
            print(f"⚠️ خطأ في تحديث أهداف {lesson_path}: {e}")
            return False

    def add_enhanced_systems(self, lesson_path):
        """إضافة الأنظمة المحسنة للدرس"""
        try:
            with open(lesson_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # التحقق من وجود الأنظمة المحسنة
            if 'EnhancedNotificationSystem' in content and 'SmartNotifications' in content:
                return False  # الأنظمة موجودة بالفعل
            
            # إضافة الأنظمة المحسنة
            enhanced_systems = '''
        // 🎵 نظام الصوت المحسن
        const SoundSystem = {
            sounds: {},
            
            preload() {
                const soundFiles = {
                    correct: '../../assets/audio/win.mp3',
                    wrong: '../../assets/audio/wrong_answer.mp3',
                    click: '../../assets/audio/Click.mp3',
                    start: '../../assets/audio/start-timer.mp3',
                    end: '../../assets/audio/end-timer.mp3',
                    notification: '../../assets/audio/Notification.mp3'
                };
                
                Object.keys(soundFiles).forEach(key => {
                    this.sounds[key] = new Audio(soundFiles[key]);
                    this.sounds[key].preload = 'auto';
                });
            },
            
            play(soundName) {
                if (this.sounds[soundName]) {
                    this.sounds[soundName].currentTime = 0;
                    return this.sounds[soundName].play().catch(e => console.log('تعذر تشغيل الصوت:', e));
                }
            }
        };

        // 🔔 نظام الإشعارات المحسن
        const EnhancedNotificationSystem = {
            show(message, type = 'info', duration = 3000) {
                const notification = document.createElement('div');
                notification.className = `enhanced-notification ${type}`;
                notification.innerHTML = `
                    <div class="notification-content">
                        <i class="fas fa-${this.getIcon(type)}"></i>
                        <span>${message}</span>
                    </div>
                `;
                
                document.body.appendChild(notification);
                
                setTimeout(() => notification.classList.add('show'), 100);
                setTimeout(() => {
                    notification.classList.remove('show');
                    setTimeout(() => document.body.removeChild(notification), 300);
                }, duration);
            },
            
            getIcon(type) {
                const icons = {
                    success: 'check-circle',
                    error: 'exclamation-circle',
                    warning: 'exclamation-triangle',
                    info: 'info-circle'
                };
                return icons[type] || 'info-circle';
            }
        };

        // 🧠 نظام الإشعارات الذكية
        const SmartNotifications = {
            show(message, options = {}) {
                const defaults = {
                    type: 'info',
                    duration: 3000,
                    position: 'top-right',
                    sound: true,
                    animation: 'slide'
                };
                
                const config = { ...defaults, ...options };
                
                if (config.sound) {
                    SoundSystem.play('notification');
                }
                
                EnhancedNotificationSystem.show(message, config.type, config.duration);
            }
        };

        // 📊 نظام تتبع التقدم المحسن
        function updateProgress() {
            const studentData = JSON.parse(localStorage.getItem('biology_progress') || '{}');
            const lessonKey = window.location.pathname;
            
            if (!studentData[lessonKey]) {
                studentData[lessonKey] = {
                    completed: false,
                    score: 0,
                    attempts: 0,
                    lastVisit: new Date().toISOString()
                };
            }
            
            studentData[lessonKey].attempts += 1;
            studentData[lessonKey].lastVisit = new Date().toISOString();
            
            localStorage.setItem('biology_progress', JSON.stringify(studentData));
            
            // تحديث شريط التقدم
            const progressBar = document.querySelector('.progress-bar');
            if (progressBar) {
                const completedLessons = Object.values(studentData).filter(lesson => lesson.completed).length;
                const totalLessons = 16;
                const progressPercent = (completedLessons / totalLessons) * 100;
                
                progressBar.style.width = `${progressPercent}%`;
                progressBar.setAttribute('data-progress', `${Math.round(progressPercent)}%`);
            }
        }

        // تهيئة الأنظمة عند تحميل الصفحة
        document.addEventListener('DOMContentLoaded', function() {
            SoundSystem.preload();
            updateProgress();
            
            // تحسين أداء الأزرار
            document.querySelectorAll('button').forEach(btn => {
                btn.addEventListener('click', () => SoundSystem.play('click'));
            });
        });
'''
            
            # إضافة الأنظمة المحسنة قبل نهاية الـ script
            script_end = content.rfind('</script>')
            if script_end != -1:
                content = content[:script_end] + enhanced_systems + '\n' + content[script_end:]
            
            # إضافة CSS للإشعارات المحسنة
            enhanced_css = '''
        <style>
        /* 🎨 أنماط الإشعارات المحسنة */
        .enhanced-notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transform: translateX(400px);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            z-index: 10000;
            max-width: 350px;
        }
        
        .enhanced-notification.show {
            transform: translateX(0);
            opacity: 1;
        }
        
        .enhanced-notification.success {
            background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        }
        
        .enhanced-notification.error {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        }
        
        .enhanced-notification.warning {
            background: linear-gradient(135deg, #ffa726 0%, #ffcc02 100%);
        }
        
        .notification-content {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .notification-content i {
            font-size: 1.2em;
        }
        
        /* 📊 تحسين شريط التقدم */
        .progress-container {
            background: rgba(255,255,255,0.1);
            border-radius: 25px;
            padding: 3px;
            margin: 20px 0;
            backdrop-filter: blur(10px);
        }
        
        .progress-bar {
            height: 25px;
            background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
            border-radius: 25px;
            transition: width 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
            overflow: hidden;
        }
        
        .progress-bar::before {
            content: attr(data-progress);
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: white;
            font-weight: bold;
            font-size: 12px;
        }
        
        .progress-bar::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        </style>
'''
            
            # إضافة CSS في الـ head
            head_end = content.find('</head>')
            if head_end != -1:
                content = content[:head_end] + enhanced_css + '\n' + content[head_end:]
            
            with open(lesson_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        except Exception as e:
            print(f"⚠️ خطأ في إضافة الأنظمة المحسنة لـ {lesson_path}: {e}")
            return False

    def process_lesson(self, lesson_key):
        """معالجة درس واحد بالكامل"""
        lesson_title = self.lessons[lesson_key]
        lesson_path = self.base_dir / lesson_key / 'index.html'
        q_lesson_path = self.q_dir / lesson_key / 'index.html'
        
        print(f"\n🔄 معالجة: {lesson_title}")
        print("-" * 50)
        
        if not lesson_path.exists():
            print(f"⚠️ ملف الدرس غير موجود: {lesson_path}")
            return False
        
        success = False
        
        # 1. استخراج وتحديث الأسئلة المتخصصة
        questions = self.extract_specialized_questions(q_lesson_path)
        if questions:
            if self.update_lesson_questions(lesson_path, questions):
                print(f"  ✅ تم تحديث {len(questions)} سؤال متخصص")
                self.stats['questions_restored'] += len(questions)
                success = True
            else:
                print(f"  ❌ فشل تحديث الأسئلة")
        else:
            print(f"  ℹ️ لا توجد أسئلة متخصصة في مجلد Q")
        
        # 2. استخراج وتحديث الأهداف التعليمية
        objectives = self.extract_specialized_objectives(q_lesson_path)
        if objectives:
            if self.update_lesson_objectives(lesson_path, objectives):
                print(f"  ✅ تم تحديث {len(objectives)} هدف تعليمي")
                self.stats['objectives_restored'] += len(objectives)
                success = True
            else:
                print(f"  ❌ فشل تحديث الأهداف")
        else:
            print(f"  ℹ️ لا توجد أهداف متخصصة في مجلد Q")
        
        # 3. إضافة الأنظمة المحسنة
        if self.add_enhanced_systems(lesson_path):
            print(f"  ✅ تم إضافة الأنظمة التفاعلية المحسنة")
            self.stats['systems_updated'] += 1
            success = True
        else:
            print(f"  ℹ️ الأنظمة المحسنة موجودة بالفعل")
        
        if success:
            self.stats['lessons_updated'] += 1
            print(f"✅ تم تحديث {lesson_title} بنجاح")
        
        return success

    def run(self):
        """تشغيل عملية الاستعادة الشاملة"""
        print("🚀 بدء عملية الاستعادة الشاملة للتحسينات...")
        print("=" * 70)
        
        # التحقق من وجود مجلد Q
        if not self.q_dir.exists():
            print("⚠️ مجلد Q غير موجود! تأكد من وجود المحتوى المتخصص.")
            return
        
        # معالجة جميع الدروس
        for lesson_key in self.lessons.keys():
            self.process_lesson(lesson_key)
        
        # عرض الإحصائيات النهائية
        print("\n" + "=" * 70)
        print("🎉 انتهاء عملية الاستعادة الشاملة!")
        print(f"✅ تم تحديث {self.stats['lessons_updated']} درس من أصل {len(self.lessons)}")
        print(f"📝 إجمالي الأسئلة المستعادة: {self.stats['questions_restored']}")
        print(f"🎯 إجمالي الأهداف المستعادة: {self.stats['objectives_restored']}")
        print(f"⚙️ إجمالي الأنظمة المحدثة: {self.stats['systems_updated']}")
        
        print(f"\n🎯 ما تم إنجازه:")
        print(f"   📚 استعادة المحتوى المتخصص من مجلد Q")
        print(f"   🎵 إضافة أنظمة الصوت والإشعارات المحسنة")
        print(f"   📊 تفعيل تتبع التقدم الذكي")
        print(f"   ✨ تحسين التفاعل والأداء")
        
        print(f"\n💡 المشروع جاهز الآن بجميع التحسينات!")

if __name__ == "__main__":
    restorer = ComprehensiveRestorer()
    restorer.run()