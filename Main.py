import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def get_price(symbol="BTC"):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        r = requests.get(url, timeout=10)
        return float(r.json()['price'])
    except:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات فعال شد ✅\nدستورات:\n/price - قیمت بیت کوین\n/start_auto - فعال سازی هر 10 دقیقه")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    p = get_price("BTC")
    if p:
        await update.message.reply_text(f"₿ BTC: ${p:,.2f}")
    else:
        await update.message.reply_text("خطا در گرفتن قیمت")

async def send_auto_price(context: ContextTypes.DEFAULT_TYPE):
    p = get_price("BTC")
    if p and context.job.chat_id:
        await context.bot.send_message(chat_id=context.job.chat_id, text=f"📊 آپدیت خودکار\n₿ BTC: ${p:,.2f}")

async def start_auto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    context.job_queue.run_repeating(send_auto_price, interval=600, first=10, chat_id=chat_id, name=str(chat_id))
    await update.message.reply_text("✅ آپدیت خودکار هر 10 دقیقه فعال شد")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("start_auto", start_auto))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
