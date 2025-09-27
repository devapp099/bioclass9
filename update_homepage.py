#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def update_homepage():
    """
    تحديث الصفحة الرئيسية لتعكس التحديثات الجديدة في الوحدة 6
    """
    try:
        file_path = "index.html"
        
        # قراءة المحتوى الحالي
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # تحديث عنوان الوحدة السادسة
        content = content.replace(
            '<h1>⚖️ الوحدة السادسة: التوازن الداخلي</h1>',
            '<h1>🧠 الوحدة السادسة: التنسيق في الإنسان</h1>\n      <p class="lead">دراسة أجهزة التحكم والتنسيق في جسم الإنسان والمحافظة على الاتزان الداخلي</p>'
        )
        
        # تحديث تخطيط الشبكة للـ 5 دروس
        content = content.replace(
            '<div class="grid grid-2">',
            '<div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 20px;">'
        )
        
        # تحديث الدرس 6-1
        content = content.replace(
            '<h2>🧬 درس 6-1 — التنظيم في الإنسان</h2>',
            '<h2>🎯 درس 6-1 — التنسيق في الإنسان</h2>'
        )
        content = content.replace(
            '<p class="lead">تكامل عمل الجهاز العصبي والهرموني للاتزان الداخلي.</p>',
            '<p class="lead">مقدمة عن أنظمة التحكم والتنسيق في الجسم وأهميتها في الاتزان الداخلي.</p>'
        )
        
        # تحديث الدرس 6-2
        content = content.replace(
            '<p class="lead">تركيب ووظائف الجهاز العصبي وآلية نقل السيالات العصبية.</p>',
            '<p class="lead">تركيب ووظائف الجهاز العصبي وآلية نقل السيالات العصبية والاستجابات الانعكاسية.</p>'
        )
        
        # تحديث الدرس 6-3 (إصلاح رمز العين)
        content = content.replace(
            '<h2>👁️ درس 6-3 — العين</h2>',
            '<h2>👁️ درس 6-3 — العين</h2>'
        )
        content = content.replace(
            '<p class="lead">تركيب العين وآلية الإبصار وعيوب الرؤية وتصحيحها.</p>',
            '<p class="lead">تركيب العين ووظائفها، آلية الرؤية، عيوب الإبصار وطرق تصحيحها.</p>'
        )
        
        # تحديث الدرس 6-4
        content = content.replace(
            '<h2>🧬 درس 6-4 — الهرمونات</h2>',
            '<h2>🧪 درس 6-4 — الهرمونات</h2>'
        )
        content = content.replace(
            '<p class="lead">دور الهرمونات في تنظيم وظائف الجسم والغدد الصماء.</p>',
            '<p class="lead">تعريف الهرمونات ووظائفها، الغدد الصماء وأهميتها في التحكم والاتزان الداخلي.</p>'
        )
        
        # تحديث الدرس 6-5
        content = content.replace(
            '<p class="lead">آليات الحفاظ على الاتزان الداخلي وتنظيم بيئة الجسم الداخلية.</p>',
            '<p class="lead">مفهوم الاتزان الداخلي وآلياته، دور الأجهزة الحيوية في المحافظة على ثبات البيئة الداخلية.</p>'
        )
        
        # حفظ الملف المحدث
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("🎉 تم تحديث الصفحة الرئيسية بنجاح!")
        print("📊 التحديثات المطبقة:")
        print("   ✅ عنوان الوحدة: 🧠 التنسيق في الإنسان")
        print("   ✅ وصف الوحدة: دراسة أجهزة التحكم والتنسيق")
        print("   ✅ تخطيط الشبكة: محسن للـ 5 دروس")
        print("   ✅ تحديث جميع عناوين وأوصاف الدروس")
        print("   ✅ إصلاح الرموز والتنسيق")
        
    except FileNotFoundError:
        print("❌ خطأ: لم يتم العثور على ملف index.html!")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")

if __name__ == "__main__":
    update_homepage()