/**
 * Yapay Zeka Destekli Chatbot - Frontend JavaScript
 * Chat işlevselliği ve UI yönetimi
 */

// Global değişkenler
let isWaitingForResponse = false;
let messageHistory = [];

// DOM elementleri
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');
const typingIndicator = document.getElementById('typingIndicator');

// Event listener'ları ekle
document.addEventListener('DOMContentLoaded', function() {
    initializeChat();
});

/**
 * Chat sistemini başlat
 */
function initializeChat() {
    // Enter tuşu ile mesaj gönder (Shift+Enter ile yeni satır)
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Send butonu tıklama
    sendBtn.addEventListener('click', sendMessage);

    // Input değişikliklerini dinle
    messageInput.addEventListener('input', function() {
        const message = this.value.trim();
        sendBtn.disabled = message.length === 0 || isWaitingForResponse;
    });

    console.log('💬 Chat sistemi başlatıldı');
}

/**
 * Mesaj gönder
 */
async function sendMessage() {
    const message = messageInput.value.trim();

    // Boş mesaj kontrolü
    if (!message || isWaitingForResponse) {
        return;
    }

    // UI'yi güncelle
    addUserMessage(message);
    messageInput.value = '';
    setWaitingState(true);

    try {
        // Backend'e mesaj gönder
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            // AI yanıtını göster
            setTimeout(() => {
                addBotMessage(data.response);
                setWaitingState(false);
            }, 1000); // Gerçekçi yanıt süresi için gecikme
        } else {
            // Hata durumu
            setTimeout(() => {
                addBotMessage(data.response || 'Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.');
                setWaitingState(false);
            }, 1000);
        }

        // Mesaj geçmişine ekle
        messageHistory.push({
            user: message,
            bot: data.response,
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error('Chat Error:', error);
        setTimeout(() => {
            addBotMessage('Bağlantı sorunu yaşıyoruz. Lütfen internet bağlantınızı kontrol edin ve tekrar deneyin.');
            setWaitingState(false);
        }, 1000);
    }
}

/**
 * Kullanıcı mesajını ekle
 * @param {string} message - Kullanıcı mesajı
 */
function addUserMessage(message) {
    const messageElement = createMessageElement(message, 'user');
    appendMessage(messageElement);
    scrollToBottom();
}

/**
 * Bot mesajını ekle
 * @param {string} message - Bot mesajı
 */
function addBotMessage(message) {
    const messageElement = createMessageElement(message, 'bot');
    appendMessage(messageElement);
    scrollToBottom();
}

/**
 * WhatsApp tarzı mesaj elementi oluştur
 * @param {string} text - Mesaj metni
 * @param {string} type - Mesaj tipi ('user' veya 'bot')
 * @returns {HTMLElement} - Mesaj elementi
 */
function createMessageElement(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;

    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.textContent = text;

    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    const now = new Date();
    timeDiv.textContent = now.toLocaleTimeString('tr-TR', {
        hour: '2-digit',
        minute: '2-digit'
    });

    bubbleDiv.appendChild(timeDiv);
    messageDiv.appendChild(bubbleDiv);

    return messageDiv;
}

/**
 * Mesajı chat alanına ekle
 * @param {HTMLElement} messageElement - Mesaj elementi
 */
function appendMessage(messageElement) {
    // Welcome mesajını kaldır (varsa)
    const welcomeMessage = chatMessages.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }

    chatMessages.appendChild(messageElement);
}

/**
 * Chat alanını en alta kaydır
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Bekleme durumunu ayarla
 * @param {boolean} waiting - Bekleme durumu
 */
function setWaitingState(waiting) {
    isWaitingForResponse = waiting;

    // Send butonu durumu
    sendBtn.disabled = waiting || messageInput.value.trim().length === 0;

    // Input durumu
    messageInput.disabled = waiting;

    // Typing indicator
    if (waiting) {
        typingIndicator.style.display = 'block';
        scrollToBottom();
    } else {
        typingIndicator.style.display = 'none';
        messageInput.focus();
    }

    // Send butonu ikonu
    const icon = sendBtn.querySelector('i');
    if (waiting) {
        icon.className = 'fas fa-spinner fa-spin';
    } else {
        icon.className = 'fas fa-paper-plane';
    }
}

/**
 * Mesaj geçmişini temizle
 */
function clearChatHistory() {
    messageHistory = [];
    chatMessages.innerHTML = `
        <div class="welcome-message">
            <i class="fas fa-robot"></i>
            <h4>Hoş Geldiniz!</h4>
            <p>Size nasıl yardımcı olabilirim?</p>
        </div>
    `;
    console.log('💭 Chat geçmişi temizlendi');
}

/**
 * Hızlı yanıt butonları ekle (isteğe bağlı)
 */
function addQuickReplies() {
    const quickReplies = [
        'Ürünleriniz nelerdir?',
        'Fiyat bilgisi alabilir miyim?',
        'Teslimat süresi ne kadar?',
        'İletişim bilgileriniz'
    ];

    const quickReplyContainer = document.createElement('div');
    quickReplyContainer.className = 'quick-replies mt-2';

    quickReplies.forEach(reply => {
        const button = document.createElement('button');
        button.className = 'btn btn-outline-primary btn-sm me-2 mb-2';
        button.textContent = reply;
        button.onclick = () => {
            messageInput.value = reply;
            sendMessage();
        };
        quickReplyContainer.appendChild(button);
    });

    return quickReplyContainer;
}

/**
 * Sistem durumunu kontrol et
 */
async function checkSystemHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();

        if (data.status === 'healthy') {
            console.log('✅ Sistem durumu: Sağlıklı');
            return true;
        } else {
            console.warn('⚠️ Sistem durumu: Sorunlu');
            return false;
        }
    } catch (error) {
        console.error('❌ Sistem durumu kontrol edilemedi:', error);
        return false;
    }
}

/**
 * Hata mesajı göster
 * @param {string} message - Hata mesajı
 */
function showErrorMessage(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger alert-dismissible fade show';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.insertBefore(errorDiv, document.body.firstChild);

    // 5 saniye sonra otomatik kaldır
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.remove();
        }
    }, 5000);
}

/**
 * Başarı mesajı göster
 * @param {string} message - Başarı mesajı
 */
function showSuccessMessage(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success alert-dismissible fade show';
    successDiv.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.insertBefore(successDiv, document.body.firstChild);

    // 3 saniye sonra otomatik kaldır
    setTimeout(() => {
        if (successDiv.parentNode) {
            successDiv.remove();
        }
    }, 3000);
}

// Sayfa kapatılırken uyarı (isteğe bağlı)
window.addEventListener('beforeunload', function(e) {
    if (messageHistory.length > 0) {
        e.preventDefault();
        e.returnValue = 'Chat geçmişiniz kaybolacak. Sayfayı kapatmak istediğinizden emin misiniz?';
    }
});

// Debug fonksiyonları (development için)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    window.chatDebug = {
        getHistory: () => messageHistory,
        clearHistory: clearChatHistory,
        addTestMessage: (text) => addBotMessage(text),
        checkHealth: checkSystemHealth
    };

    console.log('🔧 Debug modu aktif. chatDebug objesi kullanılabilir.');
}