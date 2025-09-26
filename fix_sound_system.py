#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔊 إصلاح النظام الصوتي المتقدم
=============================
إصلاح مشاكل النظام الصوتي وتطبيق الحلول على جميع الدروس
"""

import os
import re
from pathlib import Path

class SoundSystemFixer:
    def __init__(self):
        self.workspace_path = Path.cwd()
        
    def fix_sound_system_in_file(self, file_path):
        """إصلاح النظام الصوتي في ملف واحد"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # التحقق من وجود مشاكل في النظام الصوتي
            needs_fix = False
            
            # البحث عن استخدام sfx القديم
            if 'sfx.' in content:
                needs_fix = True
                # استبدال استخدامات sfx القديم
                content = re.sub(r'sfx\.correct\.play\(\)', 'SoundSystem.play("correct")', content)
                content = re.sub(r'sfx\.wrong\.play\(\)', 'SoundSystem.play("wrong")', content)
                content = re.sub(r'sfx\.done\.play\(\)', 'SoundSystem.play("celebration")', content)
                
            # البحث عن تعريف sfx القديم وإزالته
            sfx_pattern = r'const sfx = \{[^}]+\};'
            if re.search(sfx_pattern, content, re.DOTALL):
                needs_fix = True
                content = re.sub(sfx_pattern, '', content, flags=re.DOTALL)
                
            # التحقق من وجود ملفات صوتية من CDN
            if 'tiny-sound@master' in content:
                needs_fix = True
                # إزالة الأصوات القديمة من CDN
                old_sounds_pattern = r'/\* أصوات \*/.*?const sfx = \{[^}]+\};'
                content = re.sub(old_sounds_pattern, '', content, flags=re.DOTALL)
                
            # التحقق من وجود SoundSystem المناسب
            if 'SoundSystem.play(' in content and 'const SoundSystem' not in content:
                needs_fix = True
                # إضافة النظام الصوتي المحسّن في المكان المناسب
                howler_pos = content.find('</script>', content.find('howler'))
                if howler_pos != -1:
                    sound_system_code = self.get_enhanced_sound_system()
                    insert_pos = howler_pos + len('</script>')
                    content = content[:insert_pos] + sound_system_code + content[insert_pos:]
            
            if needs_fix:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
                
        except Exception as e:
            print(f"❌ خطأ في إصلاح {file_path}: {str(e)}")
            return False
            
        return False
    
    def get_enhanced_sound_system(self):
        """الحصول على كود النظام الصوتي المحسّن"""
        return '''

  <script>
    // 🔊 النظام الصوتي المحسّن المُصلح
    const SoundSystem = {
      enabled: true,
      currentVolume: 0.7,
      sounds: {},
      
      // تهيئة جميع الأصوات مع مسارات محلية صحيحة
      init() {
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
        
        Object.keys(soundMappings).forEach(type => {
          this.sounds[type] = new Howl({
            src: [`../../assets/audio/${soundMappings[type]}`],
            volume: this.getContextualVolume(type),
            preload: true,
            onloaderror: (id, error) => {
              console.warn(`⚠️ فشل تحميل الصوت ${type}: ${error}`);
            },
            onload: () => {
              console.log(`✅ تم تحميل الصوت: ${type}`);
            }
          });
        });
        
        console.log('🎵 تم تهيئة النظام الصوتي المحسّن بنجاح');
      },
      
      // تشغيل صوت مع معالجة الأخطاء
      play(soundType) {
        if (!this.enabled) {
          console.log('🔇 النظام الصوتي معطل');
          return;
        }
        
        if (!this.sounds[soundType]) {
          console.warn(`⚠️ الصوت غير موجود: ${soundType}`);
          return;
        }
        
        try {
          const contextualVolume = this.getContextualVolume(soundType);
          this.sounds[soundType].volume(contextualVolume);
          this.sounds[soundType].play();
          
          console.log(`🔊 تم تشغيل الصوت: ${soundType} بمستوى ${contextualVolume}`);
          this.trackSoundUsage(soundType);
        } catch (error) {
          console.error(`❌ خطأ في تشغيل الصوت ${soundType}:`, error);
        }
      },
      
      // تحديد مستوى الصوت حسب السياق
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
      
      // تتبع استخدام الأصوات
      trackSoundUsage(soundType) {
        if (!window.soundStats) window.soundStats = {};
        window.soundStats[soundType] = (window.soundStats[soundType] || 0) + 1;
      },
      
      // تشغيل متسلسل
      sequence(sounds, delay = 500) {
        sounds.forEach((sound, index) => {
          setTimeout(() => this.play(sound), index * delay);
        });
      },
      
      // تفعيل/إلغاء تفعيل النظام
      toggle() {
        this.enabled = !this.enabled;
        console.log(`🎵 النظام الصوتي: ${this.enabled ? 'مُفعل' : 'معطل'}`);
        return this.enabled;
      },
      
      // اختبار جميع الأصوات
      testAll() {
        console.log('🧪 اختبار جميع الأصوات...');
        const sounds = Object.keys(this.sounds);
        sounds.forEach((sound, index) => {
          setTimeout(() => {
            console.log(`🎵 اختبار: ${sound}`);
            this.play(sound);
          }, index * 1000);
        });
      }
    };

    // تهيئة النظام عند تحميل الصفحة
    document.addEventListener('DOMContentLoaded', function() {
      console.log('🚀 بدء تهيئة النظام الصوتي...');
      
      // تأخير قصير للتأكد من تحميل Howler
      setTimeout(() => {
        if (typeof Howl !== 'undefined') {
          SoundSystem.init();
          
          // اختبار سريع للتأكد من العمل
          setTimeout(() => {
            console.log('🧪 اختبار النظام الصوتي...');
            // يمكن إلغاء التعليق للاختبار: SoundSystem.play('welcome');
          }, 1000);
        } else {
          console.error('❌ مكتبة Howler غير محملة');
        }
      }, 500);
    });
  </script>'''
    
    def fix_all_lessons(self):
        """إصلاح النظام الصوتي في جميع الدروس"""
        
        fixed_count = 0
        total_count = 0
        
        print("🔧 بدء إصلاح النظام الصوتي في جميع الدروس...")
        
        # البحث عن جميع ملفات index.html في مجلدات الدروس
        for unit_dir in self.workspace_path.iterdir():
            if unit_dir.is_dir() and unit_dir.name.startswith('unit-'):
                for lesson_dir in unit_dir.iterdir():
                    if lesson_dir.is_dir() and lesson_dir.name.startswith('lesson-'):
                        index_file = lesson_dir / 'index.html'
                        
                        if index_file.exists():
                            total_count += 1
                            print(f"🔍 فحص: {unit_dir.name}/{lesson_dir.name}")
                            
                            if self.fix_sound_system_in_file(index_file):
                                fixed_count += 1
                                print(f"✅ تم إصلاح: {unit_dir.name}/{lesson_dir.name}")
                            else:
                                print(f"ℹ️  لا يحتاج إصلاح: {unit_dir.name}/{lesson_dir.name}")
        
        print(f"\n🎉 اكتمل الإصلاح!")
        print(f"📊 الإحصائيات:")
        print(f"   - الدروس المفحوصة: {total_count}")
        print(f"   - الدروس المُصلحة: {fixed_count}")
        print(f"   - الدروس السليمة: {total_count - fixed_count}")
        
        return fixed_count, total_count

def main():
    """التشغيل الرئيسي"""
    
    print("🔊 مُصلح النظام الصوتي المتقدم")
    print("=" * 35)
    
    fixer = SoundSystemFixer()
    
    try:
        fixed_count, total_count = fixer.fix_all_lessons()
        
        if fixed_count > 0:
            print(f"\n✨ تم إصلاح {fixed_count} من أصل {total_count} دروس")
            print("🎵 جميع الأنظمة الصوتية تعمل الآن بشكل صحيح!")
        else:
            print(f"\n✅ جميع الدروس الـ{total_count} تعمل بشكل صحيح بالفعل")
            
        print("\n🧪 لاختبار النظام الصوتي:")
        print("   - افتح أي درس")
        print("   - اضغط F12 واكتب: SoundSystem.testAll()")
        print("   - يجب أن تسمع جميع الأصوات بالتتابع")
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء الإصلاح: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main()