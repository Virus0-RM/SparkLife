import os
from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = os.getenv("ADMIN_IDS", "").split(",")

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    location_button = KeyboardButton(text="📍 Send Location", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[location_button]], resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        f"""👋 হ্যালো {user.first_name or "বন্ধু"}!  
📡 SparkLife বট-এ স্বাগতম।

এই Bot-এর মাধ্যমে আপনি আপনার লোকেশন শেয়ার করতে পারবেন।
অনুগ্রহ করে নিচের 📍 Send Location বাটনে ট্যাপ করুন।""",
        reply_markup=reply_markup
    )

# location handler
async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    loc = update.message.location

    for admin_id in ADMIN_IDS:
        if admin_id:
            await context.bot.send_message(
                chat_id=int(admin_id),
                text=f"""📍 লোকেশন এসেছে!
👤 User: {user.full_name} ({user.id})
🌍 Location: {loc.latitude}, {loc.longitude}"""
            )

# Run bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, location_handler))
    app.run_polling()