<div align="center">

# 📄 scandf

**Telegram-бот, превращающий фотографии в аккуратные PDF-сканы — с автообрезкой, выравниванием перспективы и распознаванием QR/штрих-кодов.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![python-telegram-bot](https://img.shields.io/badge/PTB-20+-2CA5E0?logo=telegram&logoColor=white)](https://python-telegram-bot.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## ✨ Возможности

| | |
|---|---|
| 📐 **Автообрезка и выравнивание** | Поиск контура листа (Canny + `findContours`) и perspective transform — как в CamScanner |
| 🖋️ **Скан Ч/Б** | Adaptive threshold + bilateral filter — чистый документ без теней и фона |
| 🌈 **Скан Цвет** | CLAHE-усиление локального контраста с сохранением оттенков |
| 🎨 **13 фильтров** | Сепия, контраст, резкость, инверсия, рельеф, тёплые/холодные тона и др. |
| 📑 **Текст → документ** | Любое сообщение конвертируется в PDF / DOCX / TXT (на выбор пользователя) |
| 📷 **QR / штрих-коды** | Автоматически расшифровываются и присылаются отдельным сообщением |
| 🌍 **Локализация** | Русский / English |
| ⚙️ **Настройки на пользователя** | Качество, формат PDF, формат текста, уведомления |
| 🔐 **Верификация кодом** | Защита от ботов на входе |
| 🧹 **Чистый чат** | Бот удаляет старые меню и обработанные сообщения автоматически |

---

## 🚀 Быстрый старт

### 1. Клонирование

```bash
git clone https://github.com/<your-user>/scandf.git
cd scandf
```

### 2. Зависимости

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> **macOS:** для распознавания QR установите системную библиотеку `zbar`:
> ```bash
> brew install zbar
> ```
> **Linux (Debian/Ubuntu):**
> ```bash
> sudo apt install libzbar0
> ```

### 3. Конфигурация

Создайте `.env` в корне проекта:

```env
BOT_TOKEN=123456:ABC-DEF...
DB_NAME=user_data.db
BACKUP_DIR=backups
BACKUP_INTERVAL=86400
```

Токен получите у [@BotFather](https://t.me/BotFather).

### 4. Запуск

```bash
python main.py
```

---

## 🗂️ Структура проекта

```
scandf/
├── bot/
│   ├── handlers.py        # Хендлеры команд, текста, фото
│   └── keyboards.py       # Inline- и Reply-клавиатуры
├── database/
│   └── db.py              # SQLite-обёртка
├── utils/
│   ├── image_processing.py  # OpenCV: автообрезка, threshold, QR, фильтры
│   ├── text_to_doc.py       # Генерация PDF/DOCX/TXT из текста
│   └── translations.py      # i18n (ru / en)
├── tests/
├── config.py              # Конфиг и логгер
├── main.py                # Точка входа
└── requirements.txt
```

---

## 🧪 Как это работает

```
   ┌────────────┐    ┌──────────────────┐    ┌──────────────────┐
   │   Фото     │───▶│  Автообрезка +   │───▶│   Выбранный      │
   │ из чата    │    │  perspective     │    │   фильтр         │
   └────────────┘    │  transform       │    └────────┬─────────┘
                     └──────────────────┘             │
                                                      ▼
                                           ┌────────────────────┐
                                           │  JPEG → img2pdf →  │
                                           │     PDF в чат      │
                                           └────────────────────┘
                                                      │
                              QR/штрих-коды ◀─────────┘
                              (если найдены)
```

---

## ⚙️ Настройки пользователя

| Настройка | Значения | По умолчанию |
|---|---|---|
| Язык | `ru` / `en` | `en` |
| Качество JPEG | 75 / 85 / 95 | 95 |
| Формат PDF | standard / compressed | standard |
| Формат текста | pdf / docx / txt | pdf |
| Уведомления | on / off | on |

Хранятся в SQLite (`user_data.db`).

---

## 🛠️ Технологический стек

- **[python-telegram-bot](https://python-telegram-bot.org/)** 20+ — async-обёртка Bot API
- **[OpenCV](https://opencv.org/)** — детекция контура, perspective transform, CLAHE
- **[Pillow](https://python-pillow.org/)** — фильтры и EXIF-нормализация
- **[pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar/)** — QR/штрих-коды
- **[img2pdf](https://gitlab.mister-muffin.de/josch/img2pdf)** — JPEG → PDF без перекодировки
- **[reportlab](https://www.reportlab.com/)** / **[python-docx](https://python-docx.readthedocs.io/)** — генерация документов

---

## 🗺️ Roadmap

- [ ] OCR (Tesseract) → searchable PDF
- [ ] Multi-page: сборка нескольких фото в один документ
- [ ] Сжатие готового PDF
- [ ] Шифрование PDF паролем
- [ ] Webhook-режим для прод-деплоя
- [ ] Метрики и Sentry

---

## 🤝 Контрибьютинг

PR и issues приветствуются. Перед коммитом:

```bash
pytest tests/
```

---

## 📜 Лицензия

MIT © scandf contributors
