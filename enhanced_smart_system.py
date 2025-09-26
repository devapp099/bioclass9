#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 نظام الرسائل التفاعلية الذكية المحسّن
=======================================
نظام متطور للرسائل المخصصة والتفاعل الذكي مع الطلاب
يشمل رسائل ترحيب موجهة، تشجيع ذكي، وتغذية راجعة مخصصة
"""

import os
import json
from pathlib import Path

class EnhancedSmartSystem:
    def __init__(self):
        self.workspace_path = Path.cwd()
        self.lessons_data = self.load_lessons_data()
        
    def load_lessons_data(self):
        """تحميل بيانات الدروس وتصنيفها حسب الموضوع"""
        return {
            "unit-1-cells": {
                "lesson-1-1": {
                    "title": "مدخل إلى الخلايا",
                    "topic": "cells",
                    "description": "تعرف على الوحدة الأساسية للحياة - الخلية",
                    "key_concepts": ["الخلية", "الغشاء الخلوي", "النواة", "العضيات"]
                },
                "lesson-1-2": {
                    "title": "أنواع الخلايا", 
                    "topic": "cells",
                    "description": "اكتشف الفروق بين الخلايا البدائية والحقيقية النوى",
                    "key_concepts": ["بدائية النوى", "حقيقية النوى", "البكتيريا", "الخلايا النباتية"]
                },
                "lesson-1-3": {
                    "title": "العضيات الخلوية",
                    "topic": "cells", 
                    "description": "تعلم عن المكونات الداخلية للخلية ووظائفها",
                    "key_concepts": ["الميتوكوندريا", "الشبكة الإندوبلازمية", "جهاز جولجي", "الريبوسومات"]
                }
            },
            "unit-2-transport": {
                "lesson-2-1": {
                    "title": "النقل السلبي",
                    "topic": "transport",
                    "description": "فهم كيفية انتقال المواد عبر الأغشية دون طاقة",
                    "key_concepts": ["الانتشار", "الانتشار المُيسَّر", "الخاصية الأسموزية"]
                },
                "lesson-2-2": {
                    "title": "النقل النشط",
                    "topic": "transport",
                    "description": "تعلم عن انتقال المواد باستخدام الطاقة",
                    "key_concepts": ["النقل النشط", "مضخة الصوديوم-البوتاسيوم", "البلعمة"]
                },
                "lesson-2-3": {
                    "title": "تنظيم النقل",
                    "topic": "transport",
                    "description": "اكتشف كيف تتحكم الخلايا في نقل المواد",
                    "key_concepts": ["التحكم في النفاذية", "القنوات الأيونية", "البروتينات الناقلة"]
                }
            },
            "unit-3-biomolecules": {
                "lesson-3-1": {
                    "title": "الكربوهيدرات",
                    "topic": "biomolecules",
                    "description": "تعرف على جزيئات الطاقة في الكائنات الحية",
                    "key_concepts": ["السكريات البسيطة", "السكريات المعقدة", "الجلوكوز", "النشا"]
                },
                "lesson-3-2": {
                    "title": "البروتينات",
                    "topic": "biomolecules", 
                    "description": "اكتشف جزيئات البناء والوظائف الحيوية",
                    "key_concepts": ["الأحماض الأمينية", "الإنزيمات", "الهرمونات", "البنية البروتينية"]
                },
                "lesson-3-3": {
                    "title": "الدهون والأحماض النووية",
                    "topic": "biomolecules",
                    "description": "تعلم عن جزيئات التخزين والوراثة",
                    "key_concepts": ["الدهون", "الفوسفوليبيدات", "DNA", "RNA"]
                }
            },
            "unit-4-nutrition": {
                "lesson-4-1": {
                    "title": "التمثيل الضوئي",
                    "topic": "nutrition",
                    "description": "فهم كيف تصنع النباتات غذاءها من الضوء",
                    "key_concepts": ["الكلوروفيل", "التفاعلات الضوئية", "دورة كالفن", "الأكسجين"]
                },
                "lesson-4-2": {
                    "title": "العوامل المؤثرة على التمثيل الضوئي",
                    "topic": "nutrition",
                    "description": "اكتشف ما يؤثر على كفاءة صنع الغذاء",
                    "key_concepts": ["شدة الضوء", "تركيز CO2", "درجة الحرارة", "المياه"]
                }
            },
            "unit-5-respiration": {
                "lesson-5-1": {
                    "title": "التنفس الخلوي",
                    "topic": "respiration",
                    "description": "تعلم كيف تحرر الخلايا الطاقة من الغذاء",
                    "key_concepts": ["الجلايكوليسيس", "دورة كريبس", "سلسلة نقل الإلكترون", "ATP"]
                }
            },
            "unit-6-homeostasis": {
                "lesson-6-1": {
                    "title": "مفهوم التوازن الداخلي",
                    "topic": "homeostasis",
                    "description": "فهم كيف تحافظ الكائنات على الاستقرار الداخلي",
                    "key_concepts": ["التوازن الداخلي", "التغذية الراجعة", "المستقبلات", "المنظمات"]
                },
                "lesson-6-2": {
                    "title": "تنظيم درجة الحرارة",
                    "topic": "homeostasis",
                    "description": "اكتشف كيف تتحكم الكائنات في حرارة أجسامها",
                    "key_concepts": ["التنظيم الحراري", "التعرق", "الارتعاش", "الأوعية الدموية"]
                },
                "lesson-6-3": {
                    "title": "تنظيم مستوى السكر",
                    "topic": "homeostasis",
                    "description": "تعلم عن تنظيم الجلوكوز في الدم",
                    "key_concepts": ["الإنسولين", "الجلوكاجون", "البنكرياس", "مرض السكري"]
                },
                "lesson-6-4": {
                    "title": "تنظيم الماء والأملاح",
                    "topic": "homeostasis", 
                    "description": "فهم كيفية تنظيم توازن الماء في الجسم",
                    "key_concepts": ["الكلى", "الهرمون المضاد لإدرار البول", "الأسموزية", "الترشيح"]
                }
            }
        }

    def get_enhanced_smart_system(self, unit_path, lesson_path):
        """إنشاء النظام الذكي المحسّن للدرس"""
        
        # استخراج معلومات الدرس
        unit_name = unit_path.name
        lesson_name = lesson_path.name
        
        lesson_info = self.lessons_data.get(unit_name, {}).get(lesson_name, {
            "title": "درس الأحياء",
            "topic": "general",
            "description": "تعلم مفاهيم مهمة في علم الأحياء",
            "key_concepts": ["العلوم", "الأحياء", "التعلم"]
        })
        
        return f'''
    // 🔊 النظام الصوتي المتقدم مع تحليل ذكي
    const SoundSystem = {{
      enabled: true,
      currentVolume: 0.7,
      sounds: {{}},
      
      // تهيئة جميع الأصوات
      init() {{
        const soundTypes = ['correct', 'wrong', 'click', 'select', 'milestone', 'celebration', 'complete', 'start', 'welcome'];
        soundTypes.forEach(type => {{
          this.sounds[type] = new Howl({{
            src: [`../../assets/audio/${{type === 'correct' ? 'win' : type === 'wrong' ? 'wrong_answer' : type === 'click' ? 'Click' : type === 'select' ? 'select' : type === 'milestone' ? 'g' : type === 'celebration' ? 'win-Blockbusters' : type === 'complete' ? 'end-timer' : type === 'start' ? 'start-timer' : 'name-start'}}.mp3`],
            volume: this.currentVolume,
            preload: true
          }});
        }});
      }},
      
      // تشغيل صوت مع تحليل السياق
      play(soundType) {{
        if (!this.enabled || !this.sounds[soundType]) return;
        
        // تحليل ذكي للصوت المناسب
        const contextualVolume = this.getContextualVolume(soundType);
        this.sounds[soundType].volume(contextualVolume);
        this.sounds[soundType].play();
        
        // تتبع استخدام الأصوات للتحليل
        this.trackSoundUsage(soundType);
      }},
      
      // تحديد مستوى الصوت حسب السياق
      getContextualVolume(soundType) {{
        const contextMap = {{
          'celebration': 0.9,
          'milestone': 0.8,
          'correct': 0.7,
          'welcome': 0.6,
          'wrong': 0.5,
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
      
      // تشغيل متسلسل مع تأثيرات ذكية
      sequence(sounds, delay = 500) {{
        sounds.forEach((sound, index) => {{
          setTimeout(() => {{
            this.play(sound);
            // إضافة تأثير بصري مع كل صوت
            if (sound === 'celebration') {{
              this.triggerVisualEffect();
            }}
          }}, index * delay);
        }});
      }},
      
      // تأثيرات بصرية مرافقة للأصوات
      triggerVisualEffect() {{
        if (typeof confetti !== 'undefined') {{
          confetti({{
            particleCount: 50,
            spread: 60,
            origin: {{ y: 0.8 }}
          }});
        }}
      }}
    }};

    // 🤖 نظام الرسائل التفاعلية الذكية المحسّن
    const EnhancedNotificationSystem = {{
      student: null,
      lessonInfo: {{
        title: "{lesson_info['title']}",
        description: "{lesson_info['description']}",
        keyConcepts: {json.dumps(lesson_info['key_concepts'], ensure_ascii=False)},
        topic: "{lesson_info['topic']}"
      }},
      interactionStats: {{
        clicks: 0,
        correctAnswers: 0,
        wrongAnswers: 0,
        hintsUsed: 0,
        timeSpent: 0
      }},
      
      // رسائل ذكية مخصصة حسب الموضوع والسياق
      smartMessages: {{
        welcome: {{
          general: [
            "🌟 أهلاً وسهلاً {{name}}! مرحبًا بك في {{lessonTitle}}",
            "👋 مرحبًا {{name}}! أنت على وشك خوض رحلة علمية مثيرة في {{lessonTitle}}",
            "✨ أهلاً {{name}}! دعنا نستكشف {{lessonTitle}} معًا"
          ],
          specific: {self.get_topic_specific_messages(lesson_info['topic'])}
        }},
        
        encouragement: {{
          consecutive: [
            "🚀 ممتاز {{name}}! {{consecutiveCount}} إجابات صحيحة متتالية!",
            "⭐ رائع {{name}}! أداءك يتحسن مع كل إجابة!",
            "🏆 مذهل {{name}}! أنت في حالة تدفق علمي رائعة!"
          ],
          improvement: [
            "📈 أحسنت {{name}}! أرى تحسناً واضحاً في فهمك",
            "💪 عظيم {{name}}! كل محاولة تجعلك أقوى",
            "🎯 ممتاز {{name}}! تركيزك يتطور بشكل رائع"
          ]
        }},
        
        motivation: {{
          gentle: [
            "💚 لا بأس {{name}}، التعلم رحلة جميلة من الاستكشاف",
            "🤗 المحاولة الجيدة {{name}}! كل خطأ فرصة للتعلم",
            "🌱 استمر {{name}}، أنت تنمو كعالم/ة صغير/ة"
          ],
          motivational: [
            "💡 فكر مرة أخرى {{name}}، لديك المعرفة بداخلك!",
            "🔍 راجع المفاهيم {{name}}، أنت أقرب للحل!",
            "⚡ تحدى نفسك {{name}}، العلماء لا يستسلمون!"
          ]
        }},
        
        contextual: {{
          timeSpent: [
            "⏰ {{name}}، لقد قضيت {{minutes}} دقائق في التعلم - استمر!",
            "📚 جهد رائع {{name}}! {{minutes}} دقائق من التركيز المثمر"
          ],
          performance: [
            "📊 {{name}}، نسبة نجاحك {{percentage}}% - أداء {{level}}!",
            "🎯 تحليل الأداء: {{name}} حقق {{percentage}}% - {{feedback}}"
          ]
        }},
        
        milestone: {{
          progress: [
            "🎉 ممتاز {{name}}! أكملت {{percentage}}% من الأسئلة",
            "🚀 رائع {{name}}! وصلت لمعلم {{milestone}} - استمر!",
            "⭐ تهانينا {{name}}! إنجاز جديد في رحلتك العلمية"
          ],
          mastery: [
            "🏆 {{name}} أتقن {{concept}} بنسبة {{mastery}}%!",
            "💎 إتقان ممتاز {{name}}! أنت خبير/ة في {{topic}}"
          ]
        }},
        
        finalResults: {{
          excellent: [
            "🏆 مبروك {{name}}! أداء استثنائي {{percentage}}% - أنت عالم/ة حقيقي/ة!",
            "⭐ رائع جداً {{name}}! إتقان كامل للموضوع - فخور بك!",
            "🌟 مذهل {{name}}! {{percentage}}% نتيجة تستحق التقدير والاحترام!"
          ],
          good: [
            "👏 أحسنت {{name}}! {{percentage}}% أداء جيد جداً - على الطريق الصحيح!",
            "💪 عمل ممتاز {{name}}! تحسن واضح وأداء مميز!",
            "🎯 رائع {{name}}! {{percentage}}% يظهر فهماً جيداً للموضوع"
          ],
          average: [
            "📚 أداء جيد {{name}}! {{percentage}}% - مراجعة بسيطة وستكون في القمة!",
            "🎯 استمر {{name}}! {{percentage}}% بداية جيدة للإتقان",
            "💡 جيد {{name}}! مع قليل من المراجعة ستصل للتميز"
          ],
          needsWork: [
            "💚 لا بأس {{name}}! {{percentage}}% بداية التعلم - لا تستسلم!",
            "🌱 استمر في المحاولة {{name}}! كل عالم عظيم بدأ من هنا",
            "🤝 معاً سنصل للهدف {{name}}! المثابرة هي سر النجاح"
          ]
        }}
      }},
      
      // تحليل السياق الذكي للطالب
      analyzeStudentContext() {{
        const totalAnswers = this.interactionStats.correctAnswers + this.interactionStats.wrongAnswers;
        const accuracy = totalAnswers > 0 ? (this.interactionStats.correctAnswers / totalAnswers) * 100 : 0;
        const timePerQuestion = totalAnswers > 0 ? this.interactionStats.timeSpent / totalAnswers : 0;
        
        return {{
          totalAnswers,
          accuracy: Math.round(accuracy),
          timePerQuestion: Math.round(timePerQuestion),
          engagement: this.calculateEngagement(),
          learningStyle: this.detectLearningStyle()
        }};
      }},
      
      // حساب مستوى التفاعل
      calculateEngagement() {{
        const factors = {{
          clicks: Math.min(this.interactionStats.clicks / 50, 1),
          time: Math.min(this.interactionStats.timeSpent / 600, 1), // 10 minutes max
          attempts: Math.min((this.interactionStats.correctAnswers + this.interactionStats.wrongAnswers) / 20, 1)
        }};
        
        return Math.round(((factors.clicks + factors.time + factors.attempts) / 3) * 100);
      }},
      
      // اكتشاف نمط التعلم
      detectLearningStyle() {{
        const ratio = this.interactionStats.correctAnswers / (this.interactionStats.wrongAnswers || 1);
        if (ratio > 2) return 'fast_learner';
        if (ratio > 1) return 'steady_learner';
        if (ratio > 0.5) return 'careful_learner';
        return 'exploratory_learner';
      }},
      
      // تحديد مستوى الأداء مع تحليل السياق
      getEnhancedPerformanceLevel(percentage) {{
        const context = this.analyzeStudentContext();
        let level = 'needsWork';
        
        if (percentage >= 90) level = 'excellent';
        else if (percentage >= 75) level = 'good';
        else if (percentage >= 60) level = 'average';
        
        // تعديل المستوى بناءً على السياق
        if (context.engagement > 80 && level === 'average') level = 'good';
        if (context.learningStyle === 'fast_learner' && percentage >= 85) level = 'excellent';
        
        return level;
      }},
      
      // اختيار رسالة ذكية مخصصة
      getSmartMessage(category, context = {{}}) {{
        let messages = this.smartMessages[category]?.general || [];
        
        // اختيار الرسائل المناسبة للسياق
        if (category === 'welcome' && this.smartMessages[category].specific) {{
          messages = [...messages, ...this.smartMessages[category].specific];
        }}
        
        // اختيار رسالة حسب مستوى الأداء
        if (context.percentage !== undefined) {{
          const level = this.getEnhancedPerformanceLevel(context.percentage);
          if (this.smartMessages[category][level]) {{
            messages = this.smartMessages[category][level];
          }}
        }}
        
        const randomMsg = messages[Math.floor(Math.random() * messages.length)];
        return this.personalizeMessage(randomMsg, context);
      }},
      
      // تخصيص الرسالة بمعلومات الطالب والسياق
      personalizeMessage(message, context = {{}}) {{
        const studentContext = this.analyzeStudentContext();
        const replacements = {{
          '{{name}}': this.student?.name || 'البطل/ة',
          '{{lessonTitle}}': this.lessonInfo.title,
          '{{percentage}}': context.percentage || '',
          '{{consecutiveCount}}': context.consecutiveCount || '',
          '{{minutes}}': Math.round(this.interactionStats.timeSpent / 60),
          '{{level}}': this.getPerformanceLevelArabic(context.percentage),
          '{{milestone}}': context.milestone || '',
          '{{concept}}': context.concept || 'المفهوم',
          '{{topic}}': this.lessonInfo.topic,
          '{{mastery}}': context.mastery || '',
          '{{feedback}}': this.getContextualFeedback(studentContext)
        }};
        
        let personalizedMessage = message;
        Object.keys(replacements).forEach(key => {{
          personalizedMessage = personalizedMessage.replace(new RegExp(key, 'g'), replacements[key]);
        }});
        
        return personalizedMessage;
      }},
      
      // الحصول على تغذية راجعة سياقية
      getContextualFeedback(context) {{
        if (context.accuracy >= 90) return "أداء متميز ومتسق";
        if (context.accuracy >= 75) return "مستوى جيد مع إمكانية للتحسن";
        if (context.accuracy >= 60) return "أداء مقبول يحتاج مراجعة";
        return "يحتاج مزيد من التمرين والمراجعة";
      }},
      
      // ترجمة مستوى الأداء للعربية
      getPerformanceLevelArabic(percentage) {{
        const level = this.getEnhancedPerformanceLevel(percentage);
        const translations = {{
          'excellent': 'ممتاز',
          'good': 'جيد جداً', 
          'average': 'جيد',
          'needsWork': 'يحتاج تحسين'
        }};
        return translations[level] || 'جيد';
      }},
      
      // عرض رسالة ترحيب ذكية مع معلومات الدرس
      showWelcomeMessage() {{
        const welcomeMsg = this.getSmartMessage('welcome');
        const lessonIntro = `📚 ستتعلم اليوم: ${{this.lessonInfo.description}}\\n🔬 المفاهيم الرئيسية: ${{this.lessonInfo.keyConcepts.join('، ')}}`;
        
        Swal.fire({{
          title: '🎓 مرحباً بك في رحلة التعلم!',
          html: `
            <div style="text-align:right;line-height:1.8;font-size:16px">
              <div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:15px;border-radius:12px;margin-bottom:15px">
                ${{welcomeMsg}}
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
      
      // عرض إشعار ذكي محسّن
      showSmartNotification(category, options = {{}}) {{
        const message = this.getSmartMessage(category, options);
        
        // تحديد الأيقونة والألوان حسب السياق
        const contextStyles = this.getContextualStyles(category, options);
        
        Swal.fire({{
          title: contextStyles.title,
          html: `
            <div style="text-align:right;line-height:1.6;font-size:15px">
              <div style="background:${{contextStyles.bgGradient}};color:white;padding:12px;border-radius:10px;margin-bottom:10px">
                ${{message}}
              </div>
              ${{options.showStats ? this.getStatsDisplay() : ''}}
            </div>`,
          icon: contextStyles.icon,
          timer: options.timer || 4000,
          timerProgressBar: true,
          showConfirmButton: false,
          toast: true,
          position: 'top-end',
          customClass: {{
            popup: 'animate__animated animate__slideInRight'
          }}
        }});
        
        // تشغيل الصوت المناسب
        SoundSystem.play(contextStyles.sound);
      }},
      
      // الحصول على أنماط سياقية للإشعارات
      getContextualStyles(category, options) {{
        const styles = {{
          welcome: {{
            title: '🎊 مرحباً!',
            icon: 'success',
            bgGradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            sound: 'welcome'
          }},
          encouragement: {{
            title: '⭐ أحسنت!',
            icon: 'success', 
            bgGradient: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
            sound: 'correct'
          }},
          motivation: {{
            title: '💪 استمر!',
            icon: 'info',
            bgGradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            sound: 'select'
          }},
          milestone: {{
            title: '🏆 إنجاز!',
            icon: 'success',
            bgGradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            sound: 'milestone'
          }}
        }};
        
        return styles[category] || styles.encouragement;
      }},
      
      // عرض إحصائيات الأداء
      getStatsDisplay() {{
        const context = this.analyzeStudentContext();
        return `
          <div style="background:#f8f9ff;padding:10px;border-radius:8px;font-size:13px;margin-top:10px">
            📊 الإحصائيات: دقة ${{context.accuracy}}% | تفاعل ${{context.engagement}}% | نمط التعلم: ${{this.getLearningStyleArabic(context.learningStyle)}}
          </div>`;
      }},
      
      // ترجمة نمط التعلم
      getLearningStyleArabic(style) {{
        const translations = {{
          'fast_learner': 'متعلم سريع',
          'steady_learner': 'متعلم منتظم',
          'careful_learner': 'متعلم حذر',
          'exploratory_learner': 'متعلم استكشافي'
        }};
        return translations[style] || 'متعلم مميز';
      }},
      
      // تسجيل تفاعل المستخدم
      recordInteraction(type, details = {{}}) {{
        this.interactionStats.clicks++;
        
        if (type === 'correct') {{
          this.interactionStats.correctAnswers++;
        }} else if (type === 'wrong') {{
          this.interactionStats.wrongAnswers++;
        }}
        
        // إشعارات ذكية حسب الأداء
        this.checkForSmartNotifications();
      }},
      
      // فحص الحاجة لإشعارات ذكية
      checkForSmartNotifications() {{
        const totalAnswers = this.interactionStats.correctAnswers + this.interactionStats.wrongAnswers;
        
        // إشعار معلم التقدم
        if (totalAnswers > 0 && totalAnswers % 5 === 0) {{
          const percentage = Math.round((totalAnswers / 20) * 100); // افتراض 20 سؤال
          this.showSmartNotification('milestone', {{
            percentage,
            milestone: `${{totalAnswers}} أسئلة`,
            showStats: true
          }});
        }}
        
        // إشعار التشجيع للإجابات المتتالية
        if (this.interactionStats.correctAnswers > 0 && 
            this.interactionStats.correctAnswers % 3 === 0 && 
            this.interactionStats.wrongAnswers === 0) {{
          this.showSmartNotification('encouragement', {{
            consecutiveCount: this.interactionStats.correctAnswers
          }});
        }}
      }},
      
      // تهيئة النظام للطالب
      initForStudent(studentData) {{
        this.student = studentData;
        this.showWelcomeMessage();
        
        // تتبع بداية الجلسة
        this.sessionStartTime = Date.now();
        console.log(`🤖 تم تفعيل النظام الذكي للطالب: ${{studentData.name}}`);
      }}
    }};

    // تهيئة الأنظمة عند تحميل الصفحة
    document.addEventListener('DOMContentLoaded', function() {{
      SoundSystem.init();
      console.log('🎵 تم تهيئة النظام الصوتي المحسّن');
      console.log('🤖 تم تهيئة نظام الرسائل التفاعلية الذكية');
    }});'''

    def get_topic_specific_messages(self, topic):
        """الحصول على رسائل مخصصة حسب الموضوع"""
        topic_messages = {
            "cells": [
                "🔬 أهلاً {name}! مرحبًا بك في عالم الخلايا - اللبنات الأساسية للحياة!",
                "🧬 مرحبًا {name}! ستكتشف اليوم أسرار الخلية وعجائبها",
                "✨ أهلاً {name}! رحلة مثيرة في عالم الخلايا المجهرية تنتظرك"
            ],
            "transport": [
                "💧 أهلاً {name}! مرحبًا بك في عالم النقل الخلوي المدهش!",
                "🚀 مرحبًا {name}! ستتعلم كيف تتحرك المواد عبر الأغشية",
                "⚡ أهلاً {name}! عالم الانتشار والنقل النشط في انتظارك"
            ],
            "biomolecules": [
                "🧪 أهلاً {name}! مرحبًا بك في عالم الجزيئات الحيوية الرائع!",
                "⚗️ مرحبًا {name}! ستكتشف لبنات الحياة الكيميائية",
                "🔬 أهلاً {name}! رحلة في الكيمياء الحيوية تنتظرك"
            ],
            "nutrition": [
                "🌱 أهلاً {name}! مرحبًا بك في عالم التمثيل الضوئي المذهل!",
                "☀️ مرحبًا {name}! ستتعلم كيف تصنع النباتات غذاءها من الضوء",
                "🍃 أهلاً {name}! عالم صنع الغذاء في النباتات يدعوك"
            ],
            "respiration": [
                "💨 أهلاً {name}! مرحبًا بك في عالم التنفس الخلوي!",
                "⚡ مرحبًا {name}! ستكتشف كيف تنتج الخلايا الطاقة",
                "🔋 أهلاً {name}! رحلة في عالم إنتاج الطاقة الخلوية"
            ],
            "homeostasis": [
                "⚖️ أهلاً {name}! مرحبًا بك في عالم التوازن الداخلي!",
                "🎯 مرحبًا {name}! ستتعلم كيف تحافظ الكائنات على استقرارها",
                "🧠 أهلاً {name}! عالم التنظيم والتحكم الحيوي يرحب بك"
            ]
        }
        return topic_messages.get(topic, topic_messages["cells"])

    def apply_to_all_lessons(self):
        """تطبيق النظام المحسّن على جميع الدروس"""
        
        lessons_updated = 0
        units_found = []
        
        print("🚀 بدء تطبيق النظام الذكي المحسّن على جميع الدروس...")
        
        # البحث عن جميع مجلدات الوحدات
        for item in self.workspace_path.iterdir():
            if item.is_dir() and item.name.startswith('unit-'):
                units_found.append(item.name)
                
                # البحث عن الدروس داخل كل وحدة
                for lesson_dir in item.iterdir():
                    if lesson_dir.is_dir() and lesson_dir.name.startswith('lesson-'):
                        index_file = lesson_dir / 'index.html'
                        
                        if index_file.exists():
                            try:
                                # قراءة محتوى الملف
                                with open(index_file, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                
                                # البحث عن النظام القديم وإزالته
                                content = self.remove_old_systems(content)
                                
                                # إضافة النظام الجديد المحسّن
                                enhanced_system = self.get_enhanced_smart_system(item, lesson_dir)
                                
                                # إدراج النظام في المكان المناسب (بعد تحميل المكتبات)
                                if '</script>' in content and 'Howler' in content:
                                    # العثور على آخر script tag قبل إغلاق head
                                    script_end = content.rfind('</script>')
                                    if script_end != -1:
                                        insert_pos = content.find('</script>', script_end) + len('</script>')
                                        content = content[:insert_pos] + '\n    <script>\n' + enhanced_system + '\n    </script>' + content[insert_pos:]
                                
                                # حفظ الملف المحدث
                                with open(index_file, 'w', encoding='utf-8') as f:
                                    f.write(content)
                                
                                lessons_updated += 1
                                print(f"✅ تم تحديث: {item.name}/{lesson_dir.name}")
                                
                            except Exception as e:
                                print(f"❌ خطأ في تحديث {item.name}/{lesson_dir.name}: {str(e)}")
        
        # تقرير النتائج
        print(f"\n🎉 اكتمل التحديث!")
        print(f"📊 إحصائيات التحديث:")
        print(f"   - الوحدات الموجودة: {len(units_found)}")
        print(f"   - الدروس المحدثة: {lessons_updated}")
        print(f"   - الوحدات: {', '.join(units_found)}")
        
        return lessons_updated, units_found

    def remove_old_systems(self, content):
        """إزالة الأنظمة القديمة لتجنب التداخل"""
        
        # إزالة النظام الصوتي القديم
        start_markers = [
            '// 🔊 النظام الصوتي المتقدم',
            '// النظام الصوتي المتطور',
            'const SoundSystem = {',
            '// 🔔 نظام الإشعارات والرسائل التفاعلية الذكي',
            'const NotificationSystem = {',
            'const EnhancedNotificationSystem = {'
        ]
        
        end_markers = [
            '};',
            'console.log(',
            'document.addEventListener('
        ]
        
        for start_marker in start_markers:
            start_pos = content.find(start_marker)
            if start_pos != -1:
                # البحث عن نهاية النظام
                search_start = start_pos
                brace_count = 0
                in_system = False
                end_pos = start_pos
                
                for i, char in enumerate(content[start_pos:], start_pos):
                    if char == '{':
                        brace_count += 1
                        in_system = True
                    elif char == '}':
                        brace_count -= 1
                        if in_system and brace_count == 0:
                            end_pos = i + 1
                            break
                
                # إزالة النظام القديم
                if end_pos > start_pos:
                    content = content[:start_pos] + content[end_pos:]
        
        return content

def main():
    """التشغيل الرئيسي للسكريبت"""
    
    print("🤖 نظام الرسائل التفاعلية الذكية المحسّن")
    print("=" * 50)
    
    enhancer = EnhancedSmartSystem()
    
    try:
        lessons_count, units = enhancer.apply_to_all_lessons()
        
        print(f"\n✨ تم تطبيق النظام المحسّن بنجاح!")
        print(f"📈 الميزات الجديدة المضافة:")
        print("   🎯 رسائل ترحيب مخصصة لكل درس")
        print("   🤖 تحليل ذكي لسلوك الطالب")
        print("   📊 تتبع الأداء والتفاعل")
        print("   💬 رسائل سياقية حسب الموقف")
        print("   🔊 نظام صوتي محسّن مع تأثيرات")
        print("   ⚡ تغذية راجعة فورية وذكية")
        
        # إنشاء تقرير مفصل
        from datetime import datetime
        report_content = f"""# 🤖 تقرير النظام الذكي المحسّن

## 📊 إحصائيات التطبيق
- **الدروس المحدثة**: {lessons_count}
- **الوحدات المشمولة**: {len(units)}
- **تاريخ التحديث**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🚀 الميزات الجديدة

### 1. 🎯 رسائل ترحيب ذكية مخصصة
- رسائل ترحيب مخصصة لكل موضوع
- تعريف بالدرس والمفاهيم الأساسية
- تحفيز الطالب للبدء

### 2. 🤖 تحليل سلوك الطالب
- تتبع عدد النقرات والتفاعلات
- تحليل معدل الإجابات الصحيحة
- اكتشاف نمط التعلم (سريع، منتظم، حذر، استكشافي)

### 3. 📊 نظام التغذية الراجعة الذكي
- رسائل تتكيف مع مستوى الأداء
- تشجيع مخصص للإجابات المتتالية
- تحفيز ذكي عند الأخطاء

### 4. 🔊 النظام الصوتي المحسّن
- أصوات سياقية حسب الموقف
- تأثيرات بصرية مرافقة
- تحكم ذكي في مستوى الصوت

### 5. ⚡ إشعارات المعالم الذكية
- إشعارات تلقائية عند إكمال نسب معينة
- تحليل الأداء في الوقت الفعلي
- رسائل تحفيزية مخصصة

## 🎯 الوحدات المشمولة
{chr(10).join([f"- {unit}" for unit in units])}

## 🔧 التحسينات التقنية
- كود JavaScript محسّن وأكثر كفاءة
- معالجة أفضل للأخطاء
- تصميم متجاوب للرسائل
- تحليل سلوك المستخدم في الوقت الفعلي

تم تطبيق جميع التحسينات بنجاح! 🎉
"""
        
        with open('ENHANCED_SYSTEM_REPORT.md', 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\n📄 تم إنشاء تقرير مفصل: ENHANCED_SYSTEM_REPORT.md")
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء التطبيق: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main()