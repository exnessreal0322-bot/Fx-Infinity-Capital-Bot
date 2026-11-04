import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest


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
        "XAUUSD Analysis\n\n"
        "Market data is not connected yet."
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


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30
    )

    updates_request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=40,
        write_timeout=30,
        pool_timeout=30
    )

    app = (
        Application.builder()
        .token(token)
        .request(request)
        .get_updates_request(updates_request)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("analysis", analysis))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("weekly", weekly))
    app.add_handler(CommandHandler("risk", risk))

    app.run_polling(bootstrap_retries=-1)


if __name__ == "__main__":
    main()
