from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from config import BOT_TOKEN, logger
from bot.handlers import (
    start,
    help_command,
    language,
    language_callback,
    menu_callback,
    filter_callback,
    settings_callback,
    verify_code,
    handle_image
)

def main():
    if BOT_TOKEN == "your_bot_token" or not BOT_TOKEN:
        logger.warning("⚠️ BOT_TOKEN is not configured! Please set your actual bot token in the .env file.")
        
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("language", language))

    # Register callback query handlers
    application.add_handler(CallbackQueryHandler(language_callback, pattern='^(ru|en)$'))
    application.add_handler(CallbackQueryHandler(menu_callback, pattern='^(convert|settings|help_menu)$'))
    
    application.add_handler(CallbackQueryHandler(
        filter_callback,
        pattern='^(filter_bw|filter_sepia|filter_contrast|filter_sharpen|filter_blur|filter_grayscale|filter_invert|filter_contour|filter_emboss|filter_detail|filter_brightness|filter_warm|filter_cool|filter_scan_bw|filter_scan_color)$'
    ))
    
    application.add_handler(CallbackQueryHandler(
        settings_callback,
        pattern='^(language_settings|quality_settings|pdf_format|notifications|text_format_settings|reset_settings|quality_low|quality_medium|quality_high|pdf_standard|pdf_compressed|notifications_on|notifications_off|text_fmt_pdf|text_fmt_docx|text_fmt_txt)$'
    ))

    # Register message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verify_code))
    application.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_image))

    logger.info("🚀 Starting Telegram Bot Polling...")
    application.run_polling()

if __name__ == '__main__':
    main()
