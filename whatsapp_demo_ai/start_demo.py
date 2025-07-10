#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo Başlatma Script'i
Chatbot sistemini hızlı bir şekilde başlatmak için
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Python versiyonunu kontrol et"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 veya üzeri gereklidir!")
        print(f"   Mevcut versiyon: {sys.version}")
        return False
    print(f"✅ Python versiyonu uygun: {sys.version}")
    return True

def check_dependencies():
    """Gerekli modülleri kontrol et ve yükle"""
    required_packages = ['flask', 'flask-cors', 'requests', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} yüklü")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} eksik")
    
    if missing_packages:
        print(f"\n📦 Eksik paketler yükleniyor: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Tüm paketler başarıyla yüklendi!")
        except subprocess.CalledProcessError:
            print("❌ Paket yükleme başarısız! Manuel olarak yüklemeyi deneyin:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False
    
    return True

def create_env_file():
    """Environment dosyası oluştur"""
    env_file = '.env'
    if os.path.exists(env_file):
        print("✅ .env dosyası mevcut")
        return True
    
    print("📝 .env dosyası oluşturuluyor...")
    env_content = """# Together AI API Anahtarı
TOGETHER_API_KEY=sk-yourkey

# Flask ayarları
FLASK_ENV=development
FLASK_DEBUG=True
"""
    
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ .env dosyası oluşturuldu!")
        print("⚠️  Lütfen .env dosyasındaki TOGETHER_API_KEY değerini gerçek API anahtarınızla değiştirin!")
        return True
    except Exception as e:
        print(f"❌ .env dosyası oluşturulamadı: {e}")
        return False

def check_config_file():
    """Config dosyasını kontrol et"""
    if os.path.exists('config.json'):
        print("✅ config.json dosyası mevcut")
        return True
    else:
        print("❌ config.json dosyası bulunamadı!")
        print("   Bu dosya firma bilgilerinizi içerir.")
        return False

def show_instructions():
    """Kullanım talimatlarını göster"""
    print("\n" + "="*60)
    print("🚀 CHATBOT SİSTEMİ HAZIR!")
    print("="*60)
    print("\n📋 ÖNEMLİ ADIMLAR:")
    print("1. .env dosyasını açın")
    print("2. TOGETHER_API_KEY=sk-yourkey kısmını gerçek API anahtarınızla değiştirin")
    print("3. config.json dosyasını firma bilgilerinize göre düzenleyin (isteğe bağlı)")
    print("\n🌐 BAŞLATMA:")
    print("   python app.py")
    print("\n🔗 TARAYICI:")
    print("   http://localhost:5000")
    print("\n💡 API ANAHTARI ALMA:")
    print("   https://api.together.xyz/settings/api-keys")
    print("\n" + "="*60)

def main():
    """Ana demo script'i"""
    print("🤖 Yapay Zeka Chatbot Demo Sistemi")
    print("📅 Hazırlanan Tarih:", "2025")
    print("-" * 50)
    
    # Python versiyonu kontrol et
    if not check_python_version():
        return False
    
    # Bağımlılıkları kontrol et
    if not check_dependencies():
        return False
    
    # Environment dosyası oluştur
    if not create_env_file():
        return False
    
    # Config dosyasını kontrol et
    check_config_file()
    
    # Talimatları göster
    show_instructions()
    
    # Kullanıcıdan onay al
    user_input = input("\n❓ Sistemi şimdi başlatmak ister misiniz? (y/n): ").lower().strip()
    
    if user_input in ['y', 'yes', 'evet', 'e']:
        print("\n🚀 Sistem başlatılıyor...")
        try:
            # app.py'yi çalıştır
            subprocess.run([sys.executable, 'app.py'])
        except KeyboardInterrupt:
            print("\n\n👋 Sistem kapatıldı. Görüşmek üzere!")
        except Exception as e:
            print(f"\n❌ Başlatma hatası: {e}")
            print("   Manual olarak başlatmayı deneyin: python app.py")
    else:
        print("\n✅ Hazırlık tamamlandı! İstediğiniz zaman 'python app.py' ile başlatabilirsiniz.")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 İşlem iptal edildi!")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        print("   Manuel kurulum için README.md dosyasına bakın.") 