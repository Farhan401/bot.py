from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread
import os

# -------- ১. ওয়েব সার্ভার অংশ (বট সচল রাখার জন্য) --------
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -------- ২. বটের মেইন অংশ --------

# আপনার টোকেন এখানে দিন
TOKEN = "8555039540:AAFtHKKpbQqlOBYAAhGJh4L0dar_hzTrAO0" 

pending_tasks = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "রিমাইন্ডার বট চালু হয়েছে!\nকাজ যুক্ত করতে: /add কাজ_লিখুন\nলিস্ট দেখতে: /list"
    )
    # রিমাইন্ডার সেট করা (১ ঘণ্টা = ৩৬০০ সেকেন্ড)
    context.job_queue.run_repeating(send_hourly_reminder, interval=3600, first=10, chat_id=update.message.chat_id)

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task = ' '.join(context.args)
    if task:
        pending_tasks.append(task)
        await update.message.reply_text(f"যুক্ত হয়েছে: {task}")
    else:
        await update.message.reply_text("কাজের নাম লিখুন। যেমন: /add পড়া")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if pending_tasks:
        tasks_text = "\n".join([f"{i+1}. {t}" for i, t in enumerate(pending_tasks)])
        await update.message.reply_text(f"আপনার কাজ:\n{tasks_text}")
    else:
        await update.message.reply_text("কোনো কাজ নেই।")

async def send_hourly_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    if pending_tasks:
        tasks_text = "\n".join([f"- {t}" for t in pending_tasks])
        await context.bot.send_message(job.chat_id, text=f"⏰ রিমাইন্ডার! আপনার কাজ:\n{tasks_text}")

def main():
    keep_alive() # সার্ভার চালু করা হচ্ছে
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_task))
    application.add_handler(CommandHandler("list", list_tasks))
    
    print("বট চলছে...")
    application.run_polling()

if __name__ == "__main__":
    main()
  
