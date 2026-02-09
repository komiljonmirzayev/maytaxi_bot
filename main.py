import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Xatolarni logda ko'rish
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [['Lotin', 'Kirill']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Tilni tanlang / Тилни танланг:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in ['Lotin', 'Kirill']:
        keyboard = [['Yo‘lovchi', 'Haydovchi']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Kim bo'lib davom etasiz?", reply_markup=reply_markup)

if __name__ == '__main__':
    # Botingiz tokini
    token = "8197151133:AAHi601lQ-ZooDescxMne2dxVKzTWPiudWI"
    
    # Botni qurish
    application = ApplicationBuilder().token(token).build()
    
    # Handlerlarni qo'shish
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot ishga tushdi...")
    application.run_polling()
