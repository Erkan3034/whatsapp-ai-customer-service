# 🤖 Yapay Zeka Destekli Chatbot Demo Sistemi

WhatsApp benzeri profesyonel chat arayüzü ile Together AI destekli müşteri hizmetleri chatbotu.

## 🎯 Özellikler

- **🧠 Yapay Zeka Entegrasyonu**: Together AI ile gerçekçi konuşmalar
- **💬 WhatsApp Benzeri Arayüz**: Tanıdık ve kullanıcı dostu tasarım
- **📱 Responsive Tasarım**: Mobil ve masaüstü uyumlu
- **⚡ Gerçek Zamanlı Chat**: Anında mesajlaşma deneyimi
- **🎨 Modern UI**: Bootstrap 5 ile şık tasarım
- **⚙️ Yapılandırılabilir**: config.json ile firma bilgileri
- **🔒 Güvenli**: CORS koruması ve input validasyonu

## 📋 Gereksinimler

- Python 3.8+
- Together AI API Anahtarı
- Modern web tarayıcısı

## 🚀 Kurulum

### 1. Projeyi İndirin
```bash
git clone <repo-url>
cd whatsapp_demo_ai
```

### 2. Python Bağımlılıklarını Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Environment Dosyasını Oluşturun
`.env` dosyası oluşturun ve Together AI API anahtarınızı ekleyin:
```bash
# .env dosyası
TOGETHER_API_KEY=sk-your-together-ai-api-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

### 4. Firma Bilgilerini Düzenleyin (İsteğe Bağlı)
`config.json` dosyasını kendi firma bilgilerinize göre düzenleyin:
```json
{
  "company_name": "Sizin Firma Adınız",
  "products": ["ürün1", "ürün2", "ürün3"],
  "price_range": "fiyat aralığı",
  "delivery_time": "teslimat süresi",
  "tone": "konuşma tarzı"
}
```

### 5. Uygulamayı Başlatın
```bash
python app.py
```

## 🌐 Kullanım

1. Tarayıcınızda `http://localhost:5000` adresine gidin
2. Chat arayüzünde istediğiniz mesajı yazın
3. Yapay zeka firma adına size yanıt verecektir

## 📁 Dosya Yapısı

```
whatsapp_demo_ai/
│
├── app.py                   # Flask backend sunucusu
├── config.json              # Firma bilgileri
├── requirements.txt         # Python bağımlılıkları
├── .env.example            # Environment şablonu
├── README.md               # Bu dosya
│
├── templates/
│   └── index.html          # Ana chat arayüzü
│
└── static/
    ├── css/
    │   └── style.css       # Ek CSS stilleri
    └── js/
        └── chat.js         # Chat JavaScript'i
```

## ⚙️ Yapılandırma

### Together AI Ayarları
`app.py` dosyasında Following ayarları değiştirebilirsiniz:
- `DEFAULT_MODEL`: AI modeli (varsayılan: Mixtral-8x7B)
- `max_tokens`: Maksimum yanıt uzunluğu
- `temperature`: Yaratıcılık seviyesi (0.1-1.0)

### Firma Bilgileri
`config.json` dosyasında şu bilgileri güncelleyebilirsiniz:
- `company_name`: Firma adı
- `products`: Ürün listesi
- `price_range`: Fiyat aralığı
- `delivery_time`: Teslimat süresi
- `tone`: Konuşma tarzı
- `working_hours`: Çalışma saatleri
- `contact`: İletişim bilgileri

## 🎨 Özelleştirme

### Renk Teması
`static/css/style.css` ve `templates/index.html` dosyalarından renkleri değiştirebilirsiniz.

### Mesaj Şablonları
`app.py` dosyasındaki `create_system_prompt()` fonksiyonunu düzenleyerek AI'ın davranışını özelleştirebilirsiniz.

## 🔧 API Endpoints

- `GET /` - Ana chat sayfası
- `POST /chat` - Mesaj gönderme
- `GET /health` - Sistem durumu
- `GET /company-info` - Firma bilgileri

## 📱 Mobil Uyumluluk

- Responsive tasarım
- Touch-friendly butonlar
- iOS ve Android uyumlu
- PWA hazır (service worker eklenebilir)

## 🛡️ Güvenlik

- CORS koruması aktif
- Input validasyonu
- XSS koruması
- Rate limiting (gelecekte eklenebilir)

## 🐛 Sorun Giderme

### API Anahtarı Hatası
```
API Error: 401 - Unauthorized
```
➡️ `.env` dosyasında `TOGETHER_API_KEY` doğru şekilde ayarlandığından emin olun.

### Bağlantı Hatası
```
Bağlantı sorunu yaşıyoruz
```
➡️ İnternet bağlantınızı ve Together AI servis durumunu kontrol edin.

### Modül Bulunamadı
```
ModuleNotFoundError: No module named 'flask'
```
➡️ `pip install -r requirements.txt` komutunu çalıştırın.

## 🚀 Geliştirme Fikirleri

- [ ] **Mesaj Geçmişi**: Database entegrasyonu
- [ ] **Çoklu Dil**: Dil seçeneği ekleme
- [ ] **Ses Mesajları**: Audio chat desteği
- [ ] **Dosya Paylaşımı**: Görsel ve dosya gönderme
- [ ] **Admin Panel**: Chatbot yönetim arayüzü
- [ ] **Analytics**: Chat istatistikleri
- [ ] **Push Notification**: Gerçek zamanlı bildirimler
- [ ] **Widget**: Web sitelerine gömülebilir chat widget'ı

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında dağıtılmaktadır. Detaylar için `LICENSE` dosyasına bakın.

## 🔗 Yararlı Bağlantılar

- [Together AI Dokümantasyonu](https://docs.together.ai/)
- [Flask Dokümantasyonu](https://flask.palletsprojects.com/)
- [Bootstrap 5 Dokümantasyonu](https://getbootstrap.com/docs/5.3/)

## 📞 Destek

Herhangi bir sorunuz varsa:
- Issue açın: [GitHub Issues](https://github.com/user/repo/issues)
- Email: support@example.com

---

**Made with ❤️ by AI & Human Collaboration** 