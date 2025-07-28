import logging
import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = os.getenv("ADMIN_IDS", "").split(",")

from database import log_user

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    log_user(user.id, user.username, update.effective_chat.id)
    await update.message.reply_text(f"👋 হ্যালো {user.first_name}! SparkLife বট-এ স্বাগতম।")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    info_msg = (
        f"🧾 User Info:\n"
        f"🆔 ID: {user.id}\n"
        f"👤 Username: @{user.username}\n"
        f"🕓 Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
    )
    await update.message.reply_text(info_msg)

async def admin_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ তোমার এই কমান্ড চালানোর অনুমতি নেই।")
        return

    if not os.path.exists("logs.db"):
        await update.message.reply_text("⚠️ কোনো লগ ডাটা পাওয়া যায়নি।")
        return

    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    msg = "📋 সর্বশেষ ইউজার লগ:\n"
    for row in rows:
        msg += f"🆔 {row[0]} | @{row[1]} | Chat ID: {row[2]} | ⏰ {row[3]}\n"

    await update.message.reply_text(msg)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("adminlogs", admin_logs))
    print("✅ Bot running...")
    app.run_polling()