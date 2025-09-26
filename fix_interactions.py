#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 إصلاح سريع للرسائل التفاعلية والنتائج النهائية
===================================================
إصلاح المشاكل في الدرس 1-1 و 1-2
"""

import re
from pathlib import Path

def fix_lesson_interactions(file_path):
    """إصلاح الرسائل التفاعلية والنتائج النهائية"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ خطأ في قراءة {file_path}: {str(e)}")
        return False
    
    modified = False
    
    # 1. إصلاح استدعاءات NotificationSystem إلى دوال محلية
    if 'NotificationSystem.getPerformanceLevel' in content:
        content = content.replace('NotificationSystem.getPerformanceLevel(percent)', 'getPerformanceLevel(percent)')
        modified = True
    
    if 'NotificationSystem.getRandomMessage' in content:
        content = content.replace('NotificationSystem.getRandomMessage(\'finalResults\', percent)', 'getFinalResultMessage(percent, s?.name)')
        modified = True
    
    # 2. إصلاح رسائل التشجيع
    content = re.sub(
        r'NotificationSystem\.showSmart\(\'encouragement\'[^}]+\}\);',
        'showEncouragementMessage(\'correct\');',
        content
    )
    
    content = re.sub(
        r'NotificationSystem\.showSmart\(\'motivation\'[^}]+\}\);',
        'showEncouragementMessage(\'wrong\');',
        content
    )
    
    # 3. إصلاح رسائل المعالم
    content = re.sub(
        r'NotificationSystem\.showSmart\(\'milestone\'[^}]+\}\);',
        'showMilestoneMessage(reached);',
        content
    )
    
    # 4. إضافة الدوال المفقودة إذا لم تكن موجودة
    if 'function getPerformanceLevel' not in content:
        helper_functions = '''
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
    
    // عرض رسائل المعالم
    function showMilestoneMessage(milestone) {
      const s = getStudent();
      const name = s?.name || 'البطل/ة';
      
      const messages = {
        25: `🎉 ممتاز ${name}! لقد أكملت 25% من الأسئلة!`,
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
        
        # البحث عن مكان مناسب لإدراج الدوال
        celebrate_pos = content.find('function celebrate()')
        if celebrate_pos > 0:
            content = content[:celebrate_pos] + helper_functions + '\n\n    ' + content[celebrate_pos:]
            modified = True
    
    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"❌ خطأ في كتابة {file_path}: {str(e)}")
            return False
    
    return False

def main():
    """إصلاح الدروس المحددة"""
    
    print("🔧 إصلاح سريع للرسائل التفاعلية والنتائج النهائية")
    print("=" * 55)
    
    lessons_to_fix = [
        Path('unit-1-cells/lesson-1-1/index.html'),
        Path('unit-1-cells/lesson-1-2/index.html')
    ]
    
    fixed_count = 0
    
    for lesson_path in lessons_to_fix:
        if lesson_path.exists():
            print(f"🔧 إصلاح: {lesson_path.parent.parent.name}/{lesson_path.parent.name}")
            
            if fix_lesson_interactions(lesson_path):
                fixed_count += 1
                print(f"✅ تم الإصلاح: {lesson_path.parent.parent.name}/{lesson_path.parent.name}")
            else:
                print(f"ℹ️ لا يحتاج إصلاح: {lesson_path.parent.parent.name}/{lesson_path.parent.name}")
        else:
            print(f"❌ الملف غير موجود: {lesson_path}")
    
    print(f"\n🎉 تم إصلاح {fixed_count} من أصل {len(lessons_to_fix)} دروس")
    
    if fixed_count > 0:
        print("\n🧪 للاختبار:")
        print("   - افتح الدرس 1-1 أو 1-2")
        print("   - أجب على الأسئلة وشاهد الرسائل التشجيعية")
        print("   - أكمل الكويز وشاهد النتائج النهائية المخصصة")
        print("   - لاحظ رسائل المعالم عند 25%, 50%, 75%, 100%")

if __name__ == "__main__":
    main()