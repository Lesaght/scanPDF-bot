import os
import random
import string
import tempfile
import img2pdf
from PIL import Image

from telegram import Update
from telegram.ext import ContextTypes

from config import logger
from database.db import db
from utils.translations import get_translation
from utils.image_processing import process_image, scan_qr_codes
from utils.text_to_doc import generate_document
from bot.keyboards import (
    get_language_keyboard,
    get_menu_keyboard,
    get_settings_keyboard,
    get_filters_keyboard,
    get_quality_keyboard,
    get_pdf_format_keyboard,
    get_notifications_keyboard,
    get_text_format_keyboard,
    get_main_reply_keyboard
)

async def show_menu(message, user_id: int):
    """
    Helper function to send the main reply keyboard (bottom of screen).
    """
    keyboard = get_main_reply_keyboard(user_id)
    await message.reply_text(
        get_translation(user_id, 'menu'),
        reply_markup=keyboard
    )


async def _delete_query_message(query):
    """
    Delete the message that triggered a callback query.
    Safe no-op if the message is too old to delete or already removed.
    Never touches document messages — only the inline-button message itself.
    """
    try:
        await query.message.delete()
    except Exception as e:
        logger.debug(f"Could not delete callback message: {e}")

async def settings_menu(target, user_id: int):
    """
    Helper to send the settings menu. `target` may be a Message or Chat.
    """
    keyboard = get_settings_keyboard(user_id)
    text = get_translation(user_id, 'settings_menu')
    if hasattr(target, 'send_message'):
        await target.send_message(text, reply_markup=keyboard)
    else:
        await target.reply_text(text, reply_markup=keyboard)


async def send_help(target, user_id: int):
    """
    Helper to send the help message. `target` may be a Message or Chat.
    """
    text = get_translation(user_id, 'help')
    if hasattr(target, 'send_message'):
        await target.send_message(text, parse_mode='HTML')
    else:
        await target.reply_text(text, parse_mode='HTML')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    CommandHandler for /start.
    """
    user = update.effective_user
    user_id = user.id

    user_data = db.get_user(user_id)
    if not user_data:
        code = ''.join(random.choices(string.digits, k=6))
        lang = 'en'
        db.create_user(user_id, code, lang)

        await update.message.reply_text(
            get_translation(user_id, 'code_message', code=code, attempts=3),
            parse_mode='HTML'
        )
    else:
        if user_data['verified']:
            await update.message.reply_text(get_translation(user_id, 'verified'))
            await show_menu(update.message, user_id)
        else:
            await update.message.reply_text(get_translation(user_id, 'need_verification'))

async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    CommandHandler for /language.
    """
    user_id = update.effective_user.id
    keyboard = get_language_keyboard()
    text = get_translation(user_id, 'lang_choose')
    await update.message.reply_text(text, reply_markup=keyboard)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    CommandHandler for /help.
    """
    user_id = update.effective_user.id
    await send_help(update.message, user_id)

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    CallbackQueryHandler for language selection.
    """
    query = update.callback_query
    user_id = query.from_user.id
    lang = query.data

    db.update_user(user_id, lang=lang)
    await query.answer()
    await _delete_query_message(query)
    await query.message.chat.send_message(get_translation(user_id, 'language_set'))

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    CallbackQueryHandler for main menu selections.
    """
    query = update.callback_query
    user_id = query.from_user.id
    action = query.data

    user_data = db.get_user(user_id)
    if not user_data or not user_data['verified']:
        await query.message.reply_text(get_translation(user_id, 'need_verification'))
        await query.answer()
        return

    await query.answer()
    await _delete_query_message(query)
    chat = query.message.chat

    if action == 'convert':
        reply_markup = get_filters_keyboard(user_id)
        await chat.send_message(get_translation(user_id, 'choose_filter'), reply_markup=reply_markup)
    elif action == 'settings':
        await settings_menu(chat, user_id)
    elif action == 'help_menu':
        await send_help(chat, user_id)

async def filter_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    CallbackQueryHandler for filter selection.
    """
    query = update.callback_query
    user_id = query.from_user.id
    filter_type = query.data

    db.update_user(user_id, filter=filter_type)
    await query.answer()
    await _delete_query_message(query)
    await query.message.chat.send_message(get_translation(user_id, 'filter_applied'))

async def settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    CallbackQueryHandler for settings modifications.
    """
    query = update.callback_query
    user_id = query.from_user.id
    action = query.data

    await query.answer()
    chat = query.message.chat
    await _delete_query_message(query)

    if action == 'language_settings':
        keyboard = get_language_keyboard()
        text = get_translation(user_id, 'lang_choose')
        await chat.send_message(text, reply_markup=keyboard)
    elif action == 'quality_settings':
        keyboard = get_quality_keyboard(user_id)
        await chat.send_message(get_translation(user_id, 'quality_settings'), reply_markup=keyboard)
    elif action == 'pdf_format':
        keyboard = get_pdf_format_keyboard(user_id)
        await chat.send_message(get_translation(user_id, 'pdf_format'), reply_markup=keyboard)
    elif action == 'notifications':
        keyboard = get_notifications_keyboard(user_id)
        await chat.send_message(get_translation(user_id, 'notifications'), reply_markup=keyboard)
    elif action == 'text_format_settings':
        keyboard = get_text_format_keyboard(user_id)
        await chat.send_message(get_translation(user_id, 'text_format_choose'), reply_markup=keyboard)
    elif action == 'reset_settings':
        db.update_user(user_id, quality=95, pdf_format='standard', notifications=1, text_format='pdf')
        await chat.send_message(get_translation(user_id, 'settings_reset'))
    elif action in ['quality_low', 'quality_medium', 'quality_high']:
        quality_map = {'quality_low': 75, 'quality_medium': 85, 'quality_high': 95}
        db.update_user(user_id, quality=quality_map.get(action, 95))
        await chat.send_message(get_translation(user_id, 'settings_menu'), reply_markup=get_settings_keyboard(user_id))
    elif action in ['pdf_standard', 'pdf_compressed']:
        pdf_format_map = {'pdf_standard': 'standard', 'pdf_compressed': 'compressed'}
        db.update_user(user_id, pdf_format=pdf_format_map.get(action, 'standard'))
        await chat.send_message(get_translation(user_id, 'settings_menu'), reply_markup=get_settings_keyboard(user_id))
    elif action in ['notifications_on', 'notifications_off']:
        notif_value = 1 if action == 'notifications_on' else 0
        db.update_user(user_id, notifications=notif_value)
        await chat.send_message(get_translation(user_id, 'settings_menu'), reply_markup=get_settings_keyboard(user_id))
    elif action in ['text_fmt_pdf', 'text_fmt_docx', 'text_fmt_txt']:
        fmt = action.replace('text_fmt_', '')
        db.update_user(user_id, text_format=fmt)
        await chat.send_message(get_translation(user_id, 'text_format_set', fmt=fmt.upper()))

async def _purge_tracked_messages(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    """Delete previously tracked bot messages for this user."""
    ids = context.user_data.get('tracked_msg_ids', [])
    for mid in ids:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=mid)
        except Exception as e:
            logger.debug(f"Could not delete tracked message {mid}: {e}")
    context.user_data['tracked_msg_ids'] = []


def _track(context: ContextTypes.DEFAULT_TYPE, message):
    """Remember a bot message so it can be deleted on the next menu press."""
    if message is None:
        return
    ids = context.user_data.setdefault('tracked_msg_ids', [])
    ids.append(message.message_id)


async def verify_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    MessageHandler for textual inputs.
    - Unverified users: treat text as verification code.
    - Verified users: convert text into a document in the user's chosen format.
    """
    user = update.effective_user
    user_id = user.id
    text = update.message.text.strip()

    user_data = db.get_user(user_id)
    if not user_data:
        await update.message.reply_text(get_translation(user_id, 'need_verification'))
        return

    if user_data['verified']:
        # Reply-keyboard buttons arrive as plain text — intercept them first.
        menu_labels = {
            get_translation(user_id, 'convert'): 'convert',
            get_translation(user_id, 'settings'): 'settings',
            get_translation(user_id, 'help_button'): 'help',
        }
        if text in menu_labels:
            try:
                await update.message.delete()
            except Exception as e:
                logger.debug(f"Could not delete user message: {e}")
            await _purge_tracked_messages(context, update.message.chat_id)
            action = menu_labels[text]
            if action == 'convert':
                msg = await update.message.chat.send_message(
                    get_translation(user_id, 'choose_filter'),
                    reply_markup=get_filters_keyboard(user_id)
                )
                _track(context, msg)
            elif action == 'settings':
                msg = await update.message.chat.send_message(
                    get_translation(user_id, 'settings_menu'),
                    reply_markup=get_settings_keyboard(user_id)
                )
                _track(context, msg)
            elif action == 'help':
                msg = await update.message.chat.send_message(
                    get_translation(user_id, 'help'),
                    parse_mode='HTML'
                )
                _track(context, msg)
            return
        await handle_text_to_document(update, user_id, text, user_data)
        try:
            await update.message.delete()
        except Exception as e:
            logger.debug(f"Could not delete user message: {e}")
        return

    if text == user_data['code']:
        db.update_user(user_id, verified=1)
        await update.message.reply_text(
            get_translation(user_id, 'verification_passed'),
            parse_mode='HTML'
        )
        await show_menu(update.message, user_id)
    else:
        attempts = user_data['attempts'] - 1
        db.update_user(user_id, attempts=attempts)

        if attempts > 0:
            await update.message.reply_text(
                get_translation(user_id, 'invalid_code', attempts=attempts)
            )
        else:
            db.update_user(user_id, attempts=3, code='')
            await update.message.reply_text(get_translation(user_id, 'attempts_exceeded'))


async def handle_text_to_document(update: Update, user_id: int, text: str, user_data):
    """
    Convert an incoming text message into a document file (pdf/docx/txt)
    according to the user's `text_format` setting and send it back.
    """
    try:
        fmt = user_data['text_format'] if 'text_format' in user_data.keys() else 'pdf'
    except Exception:
        fmt = 'pdf'
    fmt = fmt or 'pdf'

    await update.message.reply_text(get_translation(user_id, 'text_processing'))

    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            path, filename = generate_document(text, fmt, tmp_dir)
            with open(path, 'rb') as f:
                await update.message.reply_document(
                    document=f,
                    caption=get_translation(user_id, 'text_doc_caption', fmt=fmt.upper()),
                    filename=filename
                )
        except Exception as e:
            logger.error(f"Text-to-document error: {e}")
            await update.message.reply_text(get_translation(user_id, 'text_error'))

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    MessageHandler to process incoming image files or photos, apply filters, and convert to PDF.
    """
    user = update.effective_user
    user_id = user.id

    user_data = db.get_user(user_id)
    if not user_data or not user_data['verified']:
        await update.message.reply_text(get_translation(user_id, 'need_verification'))
        return

    await update.message.reply_text(get_translation(user_id, 'processing_start'))

    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            if update.message.photo:
                # Use the highest resolution photo available
                file = await update.message.photo[-1].get_file()
            else:
                file = await update.message.document.get_file()

            input_path = os.path.join(tmp_dir, 'input_image')
            await file.download_to_drive(input_path)

            filter_type = user_data['filter'] if user_data else 'filter_bw'
            processed_image = process_image(input_path, filter_type, auto_crop=True)
            processed_path = os.path.join(tmp_dir, 'processed.jpg')

            quality = user_data['quality'] if user_data else 95
            if processed_image.mode != 'RGB':
                processed_image = processed_image.convert('RGB')
            processed_image.save(processed_path, 'JPEG', quality=quality)

            qr_payloads = []
            try:
                with Image.open(input_path) as orig:
                    qr_payloads = scan_qr_codes(orig)
            except Exception as e:
                logger.debug(f"QR scan failed: {e}")

            pdf_path = os.path.join(tmp_dir, 'document.pdf')
            with open(pdf_path, 'wb') as f:
                f.write(img2pdf.convert(processed_path))

            # Open and read file within context to prevent issues with closed files
            with open(pdf_path, 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    caption=get_translation(user_id, 'document_caption'),
                    filename='document.pdf'
                )

            if qr_payloads:
                joined = "\n".join(f"• <code>{p}</code>" for p in qr_payloads[:10])
                await update.message.chat.send_message(
                    f"📷 QR/штрих-коды:\n{joined}",
                    parse_mode='HTML'
                )

            try:
                await update.message.delete()
            except Exception as e:
                logger.debug(f"Could not delete user message: {e}")

        except Exception as e:
            logger.error(f"Image processing error: {e}")
            await update.message.reply_text(get_translation(user_id, 'processing_error'))
