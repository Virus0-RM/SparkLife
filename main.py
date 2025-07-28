import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_IDS = [5820996662]

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location_button = KeyboardButton("📍 Send Live Location", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[location_button]], resize_keyboard=True)

    await update.message.reply_text(
        "👋 হ্যালো Boss! SparkLife বট-এ স্বাগতম!\n\n🛰️ নিচের বাটনে ক্লিক করে লাইভ লোকেশন শেয়ার করুন:",
        reply_markup=reply_markup
    )

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    location = update.message.location

    msg = (
        f"📡 New Live Location:\n"
        f"👤 User: {user.full_name} ({user.id})\n"
        f"🌐 Lat: {location.latitude}, Lon: {location.longitude}"
    )

    for admin_id in ADMIN_IDS:
        await context.bot.send_message(chat_id=admin_id, text=msg)

    await update.message.reply_text("✅ আপনার লাইভ লোকেশন সফলভাবে গ্রহণ করা হয়েছে।")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))

    app.run_polling()