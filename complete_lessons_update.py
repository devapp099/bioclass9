#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def update_lesson_with_enhanced_features(lesson_path):
    """تحديث الدرس بالميزات المحسنة الناقصة"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # التحقق من وجود الميزات المطلوبة
        needs_update = False
        
        if not re.search(r'getPerformanceLevel', content):
            needs_update = True
        if not re.search(r'getFinalResultMessage', content):
            needs_update = True
        if not re.search(r'showEncouragementMessage', content):
            needs_update = True
        if not re.search(r'النتائج النهائية', content):
            needs_update = True
            
        if not needs_update:
            return False, "الدرس محدث بالفعل"
        
        # البحث عن نقطة الإدراج (قبل نهاية البرنامج النصي)
        insert_point = content.rfind('el.submit.addEventListener')
        if insert_point == -1:
            insert_point = content.rfind('updateMeta()')
            if insert_point == -1:
                return False, "لم يتم العثور على نقطة الإدراج"
        
        # الكود المحسن للإضافة
        enhanced_code = '''
    
    // دوال مساعدة للنتائج النهائية
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

    // دالة عرض رسائل التشجيع
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

    // دالة عرض إشعارات المعالم المهمة
    function showMilestoneMessage(milestone) {
      const s = getStudent();
      const name = s?.name || 'البطل/ة';
      
      const messages = {
        25: `🌟 رائع ${name}! أكملت 25% من الأسئلة!`,
        50: `🚀 رائع ${name}! وصلت لمنتصف الطريق - 50%!`,
        75: `⭐ مذهل ${name}! 75% مكتملة - أنت بطل/ة!`,
        100: `🏆 تهانينا ${name}! أكملت جميع الأسئلة بنجاح!`
      };
      
      Swal.fire({
        title: milestone === 100 ? '🏆 مكتمل!' : `🎯 ${milestone}% مكتمل!`,
        text: messages[milestone],
        icon: 'success',
        timer: 4000,
        timerProgressBar: true,
        toast: true,
        position: 'top-end',
        showConfirmButton: false
      });
      
      SoundSystem.play(milestone === 100 ? 'complete' : 'milestone');
    }'''

        # إدراج الكود المحسن
        new_content = content[:insert_point] + enhanced_code + '\n\n    ' + content[insert_point:]
        
        # تحديث زر النتائج إذا لم يكن محدث
        if 'النتائج النهائية' not in content:
            # البحث عن el.submit.addEventListener والاستبدال
            submit_pattern = r'(el\.submit\.addEventListener\([\'"]click[\'"],\s*\(\s*\)\s*=>\s*{[^}]*)(celebrate\(\);?\s*)(.*?)(}\);)'
            
            replacement = r'''\1\2
      
      // رسالة نتائج ذكية مخصصة
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
      }).then(res=>{
        if(res.isConfirmed) {
          resetQuiz();
        } else if (res.isDenied) {
          window.location.href='../../index.html';
        }
      });\3\4'''
            
            new_content = re.sub(submit_pattern, replacement, new_content, flags=re.DOTALL)
        
        # إضافة رسائل التشجيع في نظام الإجابة
        if 'showEncouragementMessage' not in content:
            # إضافة رسائل التشجيع للإجابات الصحيحة
            correct_pattern = r'(choice\.classList\.add\([\'"]correct[\'"].*?SoundSystem\.play\([\'"]correct[\'"].*?)(gsap\.fromTo.*?}\);)'
            correct_replacement = r'''\1\2
        
        // رسائل تشجيع ذكية حسب الأداء
        if (consecutiveCorrect >= 3) {
          setTimeout(() => {
            showEncouragementMessage('correct');
          }, 800);
          consecutiveCorrect = 0; // إعادة تعيين العداد
        }'''
            
            new_content = re.sub(correct_pattern, correct_replacement, new_content, flags=re.DOTALL)
            
            # إضافة رسائل التشجيع للإجابات الخاطئة
            wrong_pattern = r'(choice\.classList\.add\([\'"]wrong[\'"].*?SoundSystem\.play\([\'"]wrong[\'"].*?)(gsap\.fromTo.*?}\);)'
            wrong_replacement = r'''\1\2
        
        // رسائل تحفيز ذكية
        if (totalAnswered >= 3) {
          setTimeout(() => {
            showEncouragementMessage('wrong');
          }, 1000);
        }'''
            
            new_content = re.sub(wrong_pattern, wrong_replacement, new_content, flags=re.DOTALL)
        
        # كتابة الملف المحدث
        with open(lesson_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "تم التحديث بنجاح"
        
    except Exception as e:
        return False, f"خطأ: {str(e)}"

def main():
    base_path = Path(".")
    lessons = []
    
    # البحث عن جميع دروس الوحدات
    for unit_dir in base_path.glob("unit-*"):
        if unit_dir.is_dir():
            for lesson_dir in unit_dir.glob("lesson-*"):
                if lesson_dir.is_dir():
                    index_file = lesson_dir / "index.html"
                    if index_file.exists():
                        lessons.append({
                            'path': str(index_file),
                            'unit': unit_dir.name,
                            'lesson': lesson_dir.name,
                            'full_name': f"{unit_dir.name}/{lesson_dir.name}"
                        })
    
    print("🔧 تحديث جميع الدروس بالميزات المحسنة...")
    print("=" * 80)
    
    total_lessons = len(lessons)
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for lesson in sorted(lessons, key=lambda x: x['full_name']):
        print(f"\n📚 معالجة الدرس: {lesson['full_name']}")
        
        success, message = update_lesson_with_enhanced_features(lesson['path'])
        
        if success:
            print(f"✅ تم التحديث بنجاح")
            updated_count += 1
        elif "محدث بالفعل" in message:
            print(f"⏭️ {message}")
            skipped_count += 1
        else:
            print(f"❌ فشل التحديث: {message}")
            error_count += 1
    
    print("\n" + "=" * 80)
    print(f"📈 ملخص النتائج:")
    print(f"📚 إجمالي الدروس: {total_lessons}")
    print(f"✅ الدروس المحدثة: {updated_count}")
    print(f"⏭️ الدروس المتخطاة (محدثة مسبقاً): {skipped_count}")
    print(f"❌ الدروس التي فشل تحديثها: {error_count}")
    
    if updated_count > 0:
        print(f"\n🎉 تم تحديث {updated_count} درس بالميزات المحسنة!")
        print(f"📝 يُنصح بعمل commit للتغييرات")
    else:
        print(f"\n💡 جميع الدروس محدثة بالفعل!")

if __name__ == "__main__":
    main()