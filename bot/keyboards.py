from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from utils.translations import get_translation


def get_main_reply_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """
    Persistent bottom keyboard shown next to the chat input.
    """
    keyboard = [
        [KeyboardButton(get_translation(user_id, 'convert'))],
        [
            KeyboardButton(get_translation(user_id, 'settings')),
            KeyboardButton(get_translation(user_id, 'help_button'))
        ]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)

def get_language_keyboard() -> InlineKeyboardMarkup:
    """
    Returns inline keyboard markup for selecting language.
    """
    keyboard = [
        [InlineKeyboardButton("Русский 🇷🇺", callback_data='ru')],
        [InlineKeyboardButton("English 🇬🇧", callback_data='en')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Returns inline keyboard markup for the main menu.
    """
    keyboard = [
        [InlineKeyboardButton(get_translation(user_id, 'convert'), callback_data='convert')],
        [
            InlineKeyboardButton(get_translation(user_id, 'settings'), callback_data='settings'),
            InlineKeyboardButton(get_translation(user_id, 'help_button'), callback_data='help_menu')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Returns inline keyboard markup for settings menu options.
    """
    keyboard = [
        [InlineKeyboardButton(get_translation(user_id, 'language_set'), callback_data='language_settings')],
        [InlineKeyboardButton(get_translation(user_id, 'quality_settings'), callback_data='quality_settings')],
        [InlineKeyboardButton(get_translation(user_id, 'pdf_format'), callback_data='pdf_format')],
        [InlineKeyboardButton(get_translation(user_id, 'notifications'), callback_data='notifications')],
        [InlineKeyboardButton(get_translation(user_id, 'text_format'), callback_data='text_format_settings')],
        [InlineKeyboardButton(get_translation(user_id, 'reset_settings'), callback_data='reset_settings')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_filters_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Returns inline keyboard markup for choosing an image filter, organized in a sleek 2-column layout.
    """
    filter_pairs = [
        ('filter_scan_bw', 'filter_scan_color'),
        ('filter_bw', 'filter_sepia'),
        ('filter_contrast', 'filter_sharpen'),
        ('filter_blur', 'filter_grayscale'),
        ('filter_invert', 'filter_contour'),
        ('filter_emboss', 'filter_detail'),
        ('filter_brightness', 'filter_warm'),
        ('filter_cool', None)
    ]
    keyboard = []
    for f1, f2 in filter_pairs:
        row = [InlineKeyboardButton(get_translation(user_id, f1), callback_data=f1)]
        if f2:
            row.append(InlineKeyboardButton(get_translation(user_id, f2), callback_data=f2))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def get_quality_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Returns inline keyboard markup for choosing quality options.
    """
    keyboard = [
        [InlineKeyboardButton(get_translation(user_id, 'quality_low'), callback_data='quality_low')],
        [InlineKeyboardButton(get_translation(user_id, 'quality_medium'), callback_data='quality_medium')],
        [InlineKeyboardButton(get_translation(user_id, 'quality_high'), callback_data='quality_high')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_pdf_format_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Returns inline keyboard markup for choosing PDF format.
    """
    keyboard = [
        [InlineKeyboardButton(get_translation(user_id, 'pdf_standard'), callback_data='pdf_standard')],
        [InlineKeyboardButton(get_translation(user_id, 'pdf_compressed'), callback_data='pdf_compressed')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_notifications_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Returns inline keyboard markup for toggling notifications.
    """
    keyboard = [
        [InlineKeyboardButton(get_translation(user_id, 'notifications_on'), callback_data='notifications_on')],
        [InlineKeyboardButton(get_translation(user_id, 'notifications_off'), callback_data='notifications_off')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_text_format_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Returns inline keyboard markup for choosing the output format for text messages.
    """
    keyboard = [
        [InlineKeyboardButton(get_translation(user_id, 'text_format_pdf'), callback_data='text_fmt_pdf')],
        [InlineKeyboardButton(get_translation(user_id, 'text_format_docx'), callback_data='text_fmt_docx')],
        [InlineKeyboardButton(get_translation(user_id, 'text_format_txt'), callback_data='text_fmt_txt')]
    ]
    return InlineKeyboardMarkup(keyboard)
