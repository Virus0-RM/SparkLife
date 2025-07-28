import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔐 Token এবং Admin ID
BOT_TOKEN = "8441489387:AAFGNRXC7D7iQij_pYAZ6IKqHM1ZaybiiIY"
ADMIN_IDS = [5820996662]

# 📋 Logging
logging.basicConfig(level=logging.INFO)

# 🚀 Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location_button = KeyboardButton(
        text="📍 Share Live Location",
        request_location=True
    )
    reply_markup = ReplyKeyboardMarkup([[location_button]], resize_keyboard=True)

    await update.message.reply_text(
        "👋 হ্যালো Boss! SparkLife বট-এ স্বাগতম!\n\n🛰️ নিচের বাটনে ক্লিক করে **লাইভ লোকেশন** শেয়ার করুন:",
        reply_markup=reply_markup
    )

# 🛰️ Handle Location
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    location = update.message.location

    msg = (
        f"📡 লাইভ লোকেশন আপডেট:\n"
        f"👤 {user.full_name} (ID: {user.id})\n"
        f"🌍 Lat: {location.latitude}\n"
        f"🌍 Lon: {location.longitude}"
    )

    # সকল অ্যাডমিনকে লোকেশন পাঠাও
    for admin_id in ADMIN_IDS:
        await context.bot.send_message(chat_id=admin_id, text=msg)

    await update.message.reply_text("✅ লাইভ লোকেশন পাওয়া গেছে!")

# ▶️ Main
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))

    print("✅ SparkLife Bot is Running with Live Tracking...")
    app.run_polling()