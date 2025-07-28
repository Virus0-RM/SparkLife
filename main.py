import logging
import sqlite3
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from database import init_db, save_location, get_logs
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

logging.basicConfig(level=logging.INFO)

# Initialize the database
init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    kb = [[KeyboardButton("📍 Share Location", request_location=True)]]
    await update.message.reply_text(
        f"Hi {user.first_name}! Tap below to share your location.",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    )

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    loc = update.message.location
    if loc:
        save_location(user.id, user.first_name, loc.latitude, loc.longitude)
        await update.message.reply_text(
            f"✅ Location received!\n📍 https://maps.google.com/?q={loc.latitude},{loc.longitude}"
        )

async def log_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("🚫 You're not authorized to view logs.")
        return
    logs = get_logs()
    if logs:
        message = "\n".join([f"{row[1]} ({row[0]}): {row[2]}, {row[3]}" for row in logs])
        await update.message.reply_text(f"📋 Location Logs:\n{message}")
    else:
        await update.message.reply_text("📭 No logs yet.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, location_handler))
    app.add_handler(CommandHandler("log", log_handler))
    app.run_polling()