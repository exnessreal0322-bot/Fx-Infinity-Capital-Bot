import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")
PUBLIC_URL = os.environ.get(
    "RENDER_EXTERNAL_URL",
    "https://fx-infinity-capital-bot.onrender.com"
)

telegram_app = Application.builder().token(BOT_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Fx_Infinity_Capital!\n\n"
        "Institutional XAUUSD Gold Analysis Bot.\n\n"
        "Use /help to see available commands."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/analysis - Gold market analysis\n"
        "/signal - XAUUSD signal\n"
        "/price - Gold price\n"
        "/daily - Daily projection\n"
        "/weekly - Weekly projection\n"
        "/risk - Risk management"
    )


async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "XAUUSD Analysis\n\nMarket data is not connected yet."
    )


async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "No verified trading signal available yet."
    )


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Live Gold price is not connected yet."
    )


async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Daily XAUUSD projection is not connected yet."
    )


async def weekly(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Weekly XAUUSD projection is not connected yet."
    )


async def risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Risk Management:\n"
        "Always use Stop Loss.\n"
        "Risk only a small part of your account.\n"
        "Never trade without confirmation."
    )


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(CommandHandler("analysis", analysis))
telegram_app.add_handler(CommandHandler("signal", signal))
telegram_app.add_handler(CommandHandler("price", price))
telegram_app.add_handler(CommandHandler("daily", daily))
telegram_app.add_handler(CommandHandler("weekly", weekly))
telegram_app.add_handler(CommandHandler("risk", risk))


@asynccontextmanager
async def lifespan(api: FastAPI):
    if not BOT_TOKEN or not WEBHOOK_SECRET:
        raise RuntimeError("Bot environment variables are missing")

    await telegram_app.initialize()
    await telegram_app.start()

    await telegram_app.bot.set_webhook(
        url=f"{PUBLIC_URL}/telegram-webhook",
        secret_token=WEBHOOK_SECRET
    )

    yield

    await telegram_app.bot.delete_webhook()
    await telegram_app.stop()
    await telegram_app.shutdown()


api = FastAPI(lifespan=lifespan)


@api.get("/")
async def home():
    return {"status": "Fx Infinity Capital Bot is running"}


@api.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    if request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token"
    ) != WEBHOOK_SECRET:
        raise HTTPException(status_code=403)

    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)

    return {"ok": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        api,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
