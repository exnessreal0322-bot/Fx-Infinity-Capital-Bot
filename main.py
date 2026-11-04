import os
import secrets
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

# ==============================
# FX INFINITY CAPITAL
# Configuration
# ==============================

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
PUBLIC_URL = os.getenv("RENDER_EXTERNAL_URL")

if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

if not WEBHOOK_SECRET:
    raise RuntimeError("WEBHOOK_SECRET is missing")

if not PUBLIC_URL:
    raise RuntimeError("RENDER_EXTERNAL_URL is missing")


# ==============================
# TELEGRAM COMMANDS
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "Welcome to Fx Infinity Capital!\n\n"
        "Institutional XAUUSD Gold Analysis Bot.\n\n"
        "Use /help to see available commands."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "FX INFINITY CAPITAL\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "AVAILABLE COMMANDS\n\n"
        "/start - Start Bot\n"
        "/help - Help Menu\n"
        "/analysis - Gold Analysis\n"
        "/signal - Trading Signal\n"
        "/price - Gold Price\n"
        "/daily - Daily Analysis\n"
        "/weekly - Weekly Analysis\n"
        "/risk - Risk Management\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "Professional XAUUSD Analysis\n"
        "Powered by Fx_Infinity_Capital"
    )


async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "XAUUSD MARKET ANALYSIS\n\n"
        "Market analysis feature is being configured.\n"
        "Please wait for live market integration."
    )


async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "GOLD TRADING SIGNAL\n\n"
        "Live signal engine is being configured.\n"
        "No unverified BUY/SELL signal will be provided."
    )


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "XAUUSD LIVE PRICE\n\n"
        "Live price API integration is in progress."
    )


async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "DAILY GOLD ANALYSIS\n\n"
        "Daily market report is being configured."
    )


async def weekly(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "WEEKLY GOLD ANALYSIS\n\n"
        "Weekly market report is being configured."
    )


async def risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "RISK MANAGEMENT\n\n"
        "1. Always use Stop Loss.\n"
        "2. Avoid overtrading.\n"
        "3. Risk only a small part of capital.\n"
        "4. Maintain proper Risk/Reward.\n"
        "5. Never trade without confirmation."
    )


# ==============================
# TELEGRAM APPLICATION
# ==============================

telegram_app = (
    Application.builder()
    .token(BOT_TOKEN)
    .build()
)

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_command))
telegram_app.add_handler(CommandHandler("analysis", analysis))
telegram_app.add_handler(CommandHandler("signal", signal))
telegram_app.add_handler(CommandHandler("price", price))
telegram_app.add_handler(CommandHandler("daily", daily))
telegram_app.add_handler(CommandHandler("weekly", weekly))
telegram_app.add_handler(CommandHandler("risk", risk))


# ==============================
# FASTAPI WEBHOOK
# ==============================

@asynccontextmanager
async def lifespan(app: FastAPI):

    await telegram_app.initialize()
    await telegram_app.start()

    webhook_url = f"{PUBLIC_URL.rstrip('/')}/webhook"

    await telegram_app.bot.set_webhook(
        url=webhook_url,
        secret_token=WEBHOOK_SECRET,
        allowed_updates=Update.ALL_TYPES
    )

    print("FX INFINITY CAPITAL BOT STARTED")
    print("WEBHOOK CONNECTED")

    yield

    await telegram_app.stop()
    await telegram_app.shutdown()


app = FastAPI(
    title="Fx Infinity Capital",
    lifespan=lifespan
)


@app.get("/")
async def home():
    return {
        "status": "Fx Infinity Capital Bot is running",
        "bot": "Online",
        "webhook": "Enabled"
    }


@app.post("/webhook")
async def webhook(request: Request):

    received_secret = request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token", ""
    )

    if not secrets.compare_digest(
        received_secret, WEBHOOK_SECRET
    ):
        raise HTTPException(
            status_code=403,
            detail="Invalid webhook secret"
        )

    try:
        data = await request.json()
        update = Update.de_json(data, telegram_app.bot)

        await telegram_app.process_update(update)

        return {"status": "ok"}

    except Exception as error:
        print("Webhook Error:", error)

        raise HTTPException(
            status_code=500,
            detail="Webhook processing failed"
        )
