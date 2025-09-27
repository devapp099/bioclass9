#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إضافة الأنظمة المفقودة - النظام الصوتي والإشعارات والرسائل الذكية
"""

import os
import re

def add_missing_systems(file_path):
    """إضافة الأنظمة المفقودة لدرس واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"🔧 إضافة الأنظمة المفقودة في {file_path}")
        updated = False
        
        # البحث عن نهاية النظام الصوتي وإضافة الكود المطلوب
        sound_system_end = 'SoundSystem.init();'
        if sound_system_end in content and 'askStudent()' not in content:
            
            # كود نظام الرسائل الذكية والإشعارات
            smart_systems_code = '''
    // نظام الرسائل التفاعلية الذكية
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
            Swal.showValidationMessage('يرجى ملء جميع البيانات');
            return false;
          }
          return { name, klass };
        }
      });
      
      if (formValues) {
        setStudent(formValues);
        SoundSystem.play('welcome');
        
        Swal.fire({
          title: `🌟 أهلاً ${formValues.name}!`,
          html: `
            <div style="text-align:center; font-size:18px">
              <p>🎯 استعد لرحلة تعليمية ممتعة!</p>
              <p style="color:#10b981">📚 ${bank.length} سؤال تفاعلي في انتظارك</p>
            </div>`,
          icon: 'success',
          confirmButtonText: 'ابدأ الآن! 🚀',
          confirmButtonColor: '#10b981',
          timer: 3000,
          timerProgressBar: true
        });
      }
    }

    // نظام عرض النتائج الذكي
    function showResults(){
      const answered = answeredCount();
      const total = bank.length;
      const score = computeScore();
      const percentage = Math.round((score/total)*100);
      
      let message = '';
      let icon = 'info';
      let color = '#3b82f6';
      
      if (percentage >= 90) {
        message = '🌟 ممتاز! أداء رائع!';
        icon = 'success';
        color = '#10b981';
        SoundSystem.play('celebration');
      } else if (percentage >= 80) {
        message = '👍 جيد جداً! واصل التقدم!';
        icon = 'success';  
        color = '#10b981';
        SoundSystem.play('correct');
      } else if (percentage >= 70) {
        message = '👌 جيد! يمكنك تحسين أدائك';
        icon = 'warning';
        color = '#f59e0b';
        SoundSystem.play('progress');
      } else {
        message = '💪 لا تستسلم! حاول مرة أخرى';
        icon = 'error';
        color = '#ef4444';
        SoundSystem.play('wrong');
      }
      
      const student = getStudent();
      const name = student ? student.name : 'عزيزي الطالب';
      
      Swal.fire({
        title: `📊 نتيجتك يا ${name}`,
        html: `
          <div style="text-align:center; font-size:18px">
            <p style="color:${color}; font-weight:bold; font-size:24px">${percentage}%</p>
            <p>${message}</p>
            <div style="background:#f8fafc; padding:16px; border-radius:12px; margin:16px 0">
              <p>✅ الإجابات الصحيحة: <strong style="color:#10b981">${score}</strong></p>
              <p>❌ الإجابات الخاطئة: <strong style="color:#ef4444">${total-score}</strong></p>
              <p>📝 إجمالي الأسئلة: <strong>${total}</strong></p>
            </div>
          </div>`,
        icon: icon,
        confirmButtonText: 'إعادة المحاولة 🔄',
        confirmButtonColor: color,
        showCancelButton: true,
        cancelButtonText: 'الانتهاء ✨'
      }).then((result) => {
        if (result.isConfirmed) {
          location.reload();
        }
      });
    }

    // دالة حساب النقاط
    function computeScore(){
      let score = 0;
      document.querySelectorAll('.q').forEach(q => {
        const correct = q.querySelector('.choice.correct');
        if (correct) score++;
      });
      return score;
    }

    // نظام الإشعارات الذكية
    const SmartNotifications = {
      progress: (answered, total) => {
        if (answered === Math.floor(total/2)) {
          Swal.fire({
            title: '⚡ نصف الطريق!',
            text: 'أنت تتقدم بشكل رائع! 🌟',
            icon: 'info',
            timer: 2000,
            toast: true,
            position: 'top-end',
            showConfirmButton: false
          });
          SoundSystem.play('milestone');
        }
      },
      
      completed: () => {
        SoundSystem.play('complete');
        setTimeout(() => {
          showResults();
        }, 1000);
      }
    };'''
            
            # إضافة الكود بعد SoundSystem.init()
            content = content.replace(
                'SoundSystem.init();',
                'SoundSystem.init();' + smart_systems_code
            )
            updated = True
            print(f"  ✅ تم إضافة نظام الرسائل الذكية والإشعارات")
        
        # تحديث نظام التفاعل مع الأسئلة ليدعم الإشعارات
        if "document.addEventListener('click', e =>" in content:
            old_click_handler = re.search(
                r"document\.addEventListener\('click', e => \{[^}]+\}\);",
                content, re.DOTALL
            )
            
            if old_click_handler:
                new_click_handler = '''document.addEventListener('click', e => {
      if (e.target.matches('.choice')) {
        const isCorrect = e.target.dataset.correct === 'true';
        
        // إزالة الحالات السابقة من هذا السؤال
        e.target.parentNode.querySelectorAll('.choice').forEach(ch => {
          ch.classList.remove('correct', 'wrong');
        });
        
        // إضافة الحالة الجديدة
        e.target.classList.add(isCorrect ? 'correct' : 'wrong');
        
        // تشغيل الصوت
        SoundSystem.play(isCorrect ? 'correct' : 'wrong');
        
        // تحديث التقدم
        updateProgress();
        
        // إشعارات ذكية
        const answered = answeredCount();
        const total = bank.length;
        SmartNotifications.progress(answered, total);
        
        // إذا تم الانتهاء من جميع الأسئلة
        if (answered === total) {
          SmartNotifications.completed();
        }
      }
    });'''
                
                content = content.replace(old_click_handler.group(0), new_click_handler)
                updated = True
                print(f"  ✅ تم تحديث نظام التفاعل مع الإشعارات الذكية")
        
        # إضافة استدعاء askStudent إذا لم يكن موجوداً
        if 'renderQuestions();' in content and 'askStudent();' not in content:
            content = content.replace(
                'renderQuestions();',
                'renderQuestions();\n    askStudent();'
            )
            updated = True
            print(f"  ✅ تم إضافة استدعاء askStudent")
        
        # حفظ الملف إذا تم التحديث
        if updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            print(f"  ℹ️  لا يحتاج تحديث: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في معالجة {file_path}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 إضافة الأنظمة المفقودة...")
    print("=" * 60)
    
    # قائمة جميع الدروس
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
            if add_missing_systems(lesson):
                fixed_count += 1
        else:
            print(f"❌ الملف غير موجود: {lesson}")
    
    print("\n" + "=" * 60)
    print(f"🎉 انتهاء العملية!")
    print(f"✅ تم تحديث {fixed_count} درس من أصل {len(lessons)}")
    print("🌟 الأنظمة المضافة:")
    print("   💬 نظام الرسائل التفاعلية الذكية")
    print("   📢 نظام الإشعارات المتقدم")
    print("   🎯 نظام عرض النتائج الذكي")
    print("   ⚡ إشعارات التقدم التلقائية")
    print("   🎮 تفاعل محسن مع الأسئلة")

if __name__ == "__main__":
    main()