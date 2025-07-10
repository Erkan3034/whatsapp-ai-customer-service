#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yapay Zeka Destekli Chatbot Demo Sistemi
Flask Backend - Together AI entegrasyonu ile
"""

import os
import json
import re
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "sk-your-default-key")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
DEFAULT_MODEL = "deepseek-ai/DeepSeek-V3"

def load_company_config():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Default config, istersen burayı genişletebilirsin
        return {
            "company_name": "Demo Perde Sistemleri",
            "products": ["stor perde", "zebra perde", "pilise perde"],
            "price_range": "500 - 1500 TL",
            "delivery_time": "3-5 iş günü",
            "contact": {
                "phone": "+90 212 123 45 67",
                "email": "info@demoperde.com",
                "address": "İstiklal Cad. No:123, İstanbul"
            },
            "tone": "samimi ve güven veren",
            "working_hours": "Pazartesi-Cumartesi 09:00-18:00",
            "services": ["ücretsiz ölçüm", "profesyonel montaj", "garantili hizmet"]
        }

def create_system_prompt(config: dict, user_message: str) -> str:
    """
    Sistemi tanımlar, config'ten tüm önemli bilgileri alır.
    user_message'a göre mağaza/iletişim/hizmet vs. özel ekleme yapar.
    """
    company_name = config.get("company_name", "Demo Perde Sistemleri")
    products = ", ".join(config.get("products", []))
    price_range = config.get("price_range", "500 - 1500 TL")
    delivery_time = config.get("delivery_time", "3-5 iş günü")
    tone = config.get("tone", "samimi ve güven veren")
    working_hours = config.get("working_hours", "Pazartesi-Cumartesi 09:00-18:00")
    contact = config.get("contact", {})
    contact_phone = contact.get("phone", "bilgi yok")
    contact_email = contact.get("email", "bilgi yok")
    contact_address = contact.get("address", "bilgi yok")
    services = config.get("services", [])

    base_prompt = f"""
Sen {company_name} firmasının müşteri temsilcisisin. 
Firma bilgilerin: 
- Ürünler: {products}
- Fiyat aralığı: {price_range}
- Teslimat süresi: {delivery_time}
- Çalışma saatleri: {working_hours}
- Hizmetlerimiz: {', '.join(services) if services else 'Bilgi yok'}
- İletişim bilgileri: Telefon: {contact_phone}, Email: {contact_email}, Adres: {contact_address}

Konuşma tarzın: {tone}

Görevlerin:
1. Müşterilere samimi, net ve kısa cevaplar ver.
2. Ürünler ve fiyatlar hakkında bilgi ver, kesin fiyat için ölçüm gerektiğini belirt.
3. Teslimat ve çalışma saatleri hakkında bilgi ver.
4. Hizmetlerimizi anlat.
5. İletişim bilgilerini paylaş.
6. Gerektiğinde kullanıcı sorusuna göre uygun bilgiyi öne çıkar.
7. Düşünme süreçlerini veya <think> gibi etiketleri kullanma, sadece doğrudan cevabı ver.

"""

    # Özel tetikleyiciler: mağaza, iletişim, hizmet sorularına ekstra vurgu yap
    triggers = {
        "store": ["mağaza", "adres", "nerede", "konum", "lokasyon"],
        "contact": ["telefon", "email", "e-posta", "iletişim", "bize nasıl ulaşırız"],
        "services": ["hizmet", "montaj", "ölçüm", "garanti"]
    }

    user_lower = user_message.lower()

    for key, keywords in triggers.items():
        if any(k in user_lower for k in keywords):
            if key == "store":
                base_prompt += f"\nMağaza adresimiz: {contact_address}\n"
            elif key == "contact":
                base_prompt += f"\nİletişim bilgilerimiz: Telefon: {contact_phone}, Email: {contact_email}\n"
            elif key == "services":
                base_prompt += f"\nSunulan hizmetler: {', '.join(services) if services else 'Bilgi yok'}\n"
            break  # Sadece ilk eşleşen tetikleyici eklenir

    return base_prompt.strip()

def clean_response(text: str) -> str:
    """Yanıttaki <think> gibi etiketleri temizler"""
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r"<thinking>.*?</thinking>", "", cleaned, flags=re.DOTALL | re.IGNORECASE)
    return cleaned.strip()

def get_ai_response(user_message: str, config: dict) -> str:
    system_prompt = create_system_prompt(config, user_message)
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 500,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            res_json = response.json()
            choices = res_json.get("choices", [])
            if choices:
                answer = choices[0]["message"]["content"]
                return clean_response(answer)
            else:
                return "Üzgünüm, şu anda yanıt veremiyorum. Lütfen tekrar deneyin."
        else:
            print(f"API Hatası: {response.status_code} - {response.text}")
            return "Teknik bir sorun var, lütfen daha sonra deneyin."
    except requests.exceptions.Timeout:
        return "Yanıt süresi aşıldı. Lütfen tekrar deneyin."
    except requests.exceptions.RequestException as e:
        print(f"İstek Hatası: {e}")
        return "Bağlantı sorunu var, internetini kontrol et."
    except Exception as e:
        print(f"Beklenmeyen Hata: {e}")
        return "Bir hata oluştu, lütfen tekrar dene."

@app.route("/")
def index():
    config = load_company_config()
    return render_template("index.html", company_name=config.get("company_name", "Demo Chat"))

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Mesaj bulunamadı", "response": "Lütfen bir mesaj gönderin."}), 400

    user_message = data["message"].strip()
    if not user_message:
        return jsonify({"error": "Boş mesaj", "response": "Lütfen bir mesaj yazın."}), 400

    config = load_company_config()
    ai_response = get_ai_response(user_message, config)
    return jsonify({"success": True, "response": ai_response, "user_message": user_message})

@app.route("/health")
def health_check():
    return jsonify({"status": "healthy", "message": "Chatbot sistemi çalışıyor"})

@app.route("/company-info")
def company_info():
    config = load_company_config()
    return jsonify(config)

if __name__ == "__main__":
    print("🤖 Yapay Zeka Chatbot Demo Sistemi Başlatılıyor...")
    print("🌐 Chat arayüzü: http://localhost:5000")
    print("🌍 Yerel ağ: http://192.168.172.46:5000")
    print("📝 API endpoint: http://localhost:5000/chat")
    print("💡 .env dosyasına TOGETHER_API_KEY=sk-yourkey ekleyin")
    
    # Flask uygulamasını başlat
    app.run(debug=True, host="0.0.0.0", port=5000)
