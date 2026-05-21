import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
TELEGRAM_BOT_TOKEN = "8831792304:AAH021MLBVksp7_-ndf8reuRo3tEOx6MQJg"
CMC_API_KEY = "bdb95ac1c7aa4d87ab6d91ea24e96eed"

CMC_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"


def fmt_money(x):
    if x >= 1_000_000_000:
        return f"${x / 1_000_000_000:.2f}B"

    if x >= 1_000_000:
        return f"${x / 1_000_000:.2f}M"

    return f"${x:,.2f}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введи тікер: BTC, ETH, SOL...")


async def get_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = update.message.text.strip().upper()

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": CMC_API_KEY
    }

    params = {
        "symbol": symbol,
        "convert": "USD"
    }

    response = requests.get(
        CMC_URL,
        headers=headers,
        params=params
    )

    data = response.json()

    if "data" not in data or symbol not in data["data"]:
        await update.message.reply_text("Монета не знайдена")
        return

    coin = data["data"][symbol]
    quote = coin["quote"]["USD"]
    text = (
        f"{coin['name']} ({symbol})\n\n"
        f"Price: ${quote['price']:,.6f}\n"
        f"Market Cap: {fmt_money(quote['market_cap'])}\n"
        f"Volume 24h: {fmt_money(quote['volume_24h'])}"
    )
    

    await update.message.reply_text(text)


app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_coin))

print("BOT STARTED")

app.run_polling()