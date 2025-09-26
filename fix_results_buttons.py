#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def fix_submit_button_results(lesson_path):
    """إصلاح زر النتائج لعرض الشاشة الذكية"""
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # التحقق من وجود النص المطلوب
        if 'النتائج النهائية' in content:
            return False, "الدرس محدث بالفعل"
        
        # البحث عن زر النتائج والاستبدال
        # البحث عن النمط الحالي لزر النتائج
        old_pattern = r'(el\.submit\.addEventListener\([\'"]click[\'"],\s*\(\s*\)\s*=>\s*\{[^}]*const\s*\{\s*correct,\s*total,\s*percent\s*\}\s*=\s*computeScore\(\);[^}]*celebrate\(\);[^}]*)(Swal\.fire\([^}]*\}\);[^}]*\}\);)'
        
        new_submit_code = '''el.submit.addEventListener('click', ()=>{
      const s = getStudent();
      const { correct, total, percent } = computeScore();
      celebrate();
      
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
      });
    });'''
        
        # استبدال زر النتائج بالكامل
        submit_pattern = r'el\.submit\.addEventListener\([\'"]click[\'"],\s*\([^}]*\{[^}]*\{[^}]*\}[^}]*\}[^}]*\}\);'
        
        if re.search(submit_pattern, content, re.DOTALL):
            new_content = re.sub(submit_pattern, new_submit_code, content, flags=re.DOTALL)
        else:
            # محاولة أخرى بنمط أبسط
            simple_pattern = r'el\.submit\.addEventListener\([^;]*\);'
            if re.search(simple_pattern, content, re.DOTALL):
                new_content = re.sub(simple_pattern, new_submit_code, content, flags=re.DOTALL)
            else:
                return False, "لم يتم العثور على زر النتائج"
        
        # كتابة الملف المحدث
        with open(lesson_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "تم إصلاح زر النتائج بنجاح"
        
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
    
    print("🔧 إصلاح أزرار النتائج لعرض الشاشة الذكية...")
    print("=" * 80)
    
    total_lessons = len(lessons)
    fixed_count = 0
    skipped_count = 0
    error_count = 0
    
    for lesson in sorted(lessons, key=lambda x: x['full_name']):
        print(f"\n📚 معالجة الدرس: {lesson['full_name']}")
        
        success, message = fix_submit_button_results(lesson['path'])
        
        if success:
            print(f"✅ تم الإصلاح بنجاح")
            fixed_count += 1
        elif "محدث بالفعل" in message:
            print(f"⏭️ {message}")
            skipped_count += 1
        else:
            print(f"❌ فشل الإصلاح: {message}")
            error_count += 1
    
    print("\n" + "=" * 80)
    print(f"📈 ملخص النتائج:")
    print(f"📚 إجمالي الدروس: {total_lessons}")
    print(f"✅ الدروس المُصلحة: {fixed_count}")
    print(f"⏭️ الدروس المتخطاة (محدثة مسبقاً): {skipped_count}")
    print(f"❌ الدروس التي فشل إصلاحها: {error_count}")
    
    if fixed_count > 0:
        print(f"\n🎉 تم إصلاح {fixed_count} درس!")
        print(f"📝 يُنصح بعمل commit للتغييرات")
    else:
        print(f"\n💡 جميع الدروس محدثة بالفعل!")

if __name__ == "__main__":
    main()