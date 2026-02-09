import logging
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 1. LOGLARNI SOZLASH (Xatolarni ko'rish uchun)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# 2. RENDER PORT XATOSINI TUZATISH (Oddiy Web Server qismi)
# Render botdan port kutgani uchun, unga "ishlayapman" degan javobni qaytaramiz
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is live!")

def run_web_server():
    # Render beradigan portni olamiz yoki 8080 ni ishlatamiz
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"Web server {port}-portda ishga tushdi...")
    server.serve_forever()

# 3. BOT KOMANDALARI
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['Lotin', 'Kirill']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "Assalomu alaykum! Tilni tanlang / Тилni танланг:", 
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in ['Lotin', 'Kirill']:
        keyboard = [['Yo‘lovchi', 'Haydovchi']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Kim bo'lib davom etasiz?", reply_markup=reply_markup)
    
    elif text == 'Yo‘lovchi':
        await update.message.reply_text("Siz Yo'lovchi rejimini tanladingiz. Tez orada yangi funksiyalar qo'shiladi!")
    
    elif text == 'Haydovchi':
        await update.message.reply_text("Siz Haydovchi rejimini tanladingiz. Hujjatlaringizni tayyorlab turing!")

# 4. ASOSIY ISHGA TUSHIRISH QISMI
if __name__ == '__main__':
    # Tokeningiz
    token = "8197151133:AAHi601lQ-ZooDescxMne2dxVKzTWPiudWI"
    
    # Port xatosini chetlab o'tish uchun serverni alohida oqimda (thread) boshlaymiz
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # Bot ilovasini qurish
    application = ApplicationBuilder().token(token).build()
    
    # Buyruqlarni ulash
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot polling rejimida ishga tushdi...")
    # Render'da bot to'xtab qolmasligi uchun polling'ni boshlaymiz
    application.run_polling(drop_pending_updates=True)
