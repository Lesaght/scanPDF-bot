<div align="center">

# 📄 scanpdf-bot

**Telegram-бот, превращающий фотографии в аккуратные PDF-сканы** — с автообрезкой, выравниванием перспективы и расширенной обработкой

**Telegram bot that converts photos into neat PDF scans** — with auto-cropping, perspective alignment and advanced processing

![GitHub](https://img.shields.io/badge/GitHub-Lesaght-181717?logo=github)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![python-telegram-bot](https://img.shields.io/badge/PTB-20+-2CA5E0?logo=telegram&logoColor=white)](https://python-telegram-bot.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[🇷🇺 Русский](#-возможности) • [🇬🇧 English](#-features)**

</div>

---

## 🇷🇺 Русский

### ✨ Возможности

| Функция | Описание |
|---------|---------|
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

### 🚀 Быстрый старт

#### 1️⃣ Клонирование

```bash
git clone https://github.com/Lesaght/Bot-for-PDF-scan.git
cd Bot-for-PDF-scan
```

#### 2️⃣ Установка зависимостей

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> **macOS:** для распознавания QR установите системную библиотеку `zbar`:
> ```bash
> brew install zbar
> ```
> 
> **Linux (Debian/Ubuntu):**
> ```bash
> sudo apt install libzbar0
> ```

#### 3️⃣ Конфигурация

Создайте `.env` в корне проекта:

```env
BOT_TOKEN=123456:ABC-DEF...
DB_NAME=user_data.db
BACKUP_DIR=backups
BACKUP_INTERVAL=86400
```

Токен получите у [@BotFather](https://t.me/BotFather).

#### 4️⃣ Запуск

```bash
python main.py
```

### 🗂️ Структура проекта

```
Bot-for-PDF-scan/
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

### 🧪 Как это работает

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
                                    QR/штрих-коды ◀──┘
                                    (если найдены)
```

### ⚙️ Настройки пользователя

| Настройка | Значения | По умолчанию |
|-----------|----------|--------------|
| Язык | `ru` / `en` | `en` |
| Качество JPEG | 75 / 85 / 95 | 95 |
| Формат PDF | standard / compressed | standard |
| Формат текста | pdf / docx / txt | pdf |
| Уведомления | on / off | on |

Хранятся в SQLite (`user_data.db`).

### 🛠️ Технологический стек

- **[python-telegram-bot](https://python-telegram-bot.org/)** 20+ — async-обёртка Bot API
- **[OpenCV](https://opencv.org/)** — детекция контура, perspective transform, CLAHE
- **[Pillow](https://python-pillow.org/)** — фильтры и EXIF-нормализация
- **[pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar/)** — QR/штрих-коды
- **[img2pdf](https://gitlab.mister-muffin.de/josch/img2pdf)** — JPEG → PDF без перекодировки
- **[reportlab](https://www.reportlab.com/)** / **[python-docx](https://python-docx.readthedocs.io/)** — генерация документов

### 📜 Лицензия

MIT © scandf contributors

---

## 🇬🇧 English

### ✨ Features

| Feature | Description |
|---------|-------------|
| 📐 **Auto-crop & Perspective** | Document edge detection (Canny + `findContours`) and perspective transform — like in CamScanner |
| 🖋️ **B&W Scan** | Adaptive threshold + bilateral filter — clean document without shadows and background |
| 🌈 **Color Scan** | CLAHE local contrast enhancement with color preservation |
| 🎨 **13 Filters** | Sepia, contrast, sharpness, inversion, emboss, warm/cool tones and more |
| 📑 **Text → Document** | Convert any message to PDF / DOCX / TXT (user's choice) |
| 📷 **QR / Barcodes** | Automatically decoded and sent as a separate message |
| 🌍 **Localization** | Russian / English |
| ⚙️ **User Settings** | Quality, PDF format, text format, notifications |
| 🔐 **Code Verification** | Bot protection from spam |
| 🧹 **Clean Chat** | Bot automatically removes old menus and processed messages |

### 🚀 Quick Start

#### 1️⃣ Clone Repository

```bash
git clone https://github.com/Lesaght/Bot-for-PDF-scan.git
cd Bot-for-PDF-scan
```

#### 2️⃣ Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> **macOS:** Install `zbar` for QR recognition:
> ```bash
> brew install zbar
> ```
> 
> **Linux (Debian/Ubuntu):**
> ```bash
> sudo apt install libzbar0
> ```

#### 3️⃣ Configuration

Create `.env` in the project root:

```env
BOT_TOKEN=123456:ABC-DEF...
DB_NAME=user_data.db
BACKUP_DIR=backups
BACKUP_INTERVAL=86400
```

Get your token from [@BotFather](https://t.me/BotFather).

#### 4️⃣ Run

```bash
python main.py
```

### 🗂️ Project Structure

```
Bot-for-PDF-scan/
├── bot/
│   ├── handlers.py        # Command, text, and photo handlers
│   └── keyboards.py       # Inline and reply keyboards
├── database/
│   └── db.py              # SQLite wrapper
├── utils/
│   ├── image_processing.py  # OpenCV: cropping, threshold, QR, filters
│   ├── text_to_doc.py       # PDF/DOCX/TXT generation from text
│   └── translations.py      # i18n (ru / en)
├── tests/
├── config.py              # Config and logger
├── main.py                # Entry point
└── requirements.txt
```

### 🧪 How It Works

```
   ┌────────────┐    ┌──────────────────┐    ┌──────────────────┐
   │   Photo    │───▶│  Auto-crop +     │───▶│   Selected       │
   │ from chat  │    │  perspective     │    │   filter         │
   └────────────┘    │  transform       │    └────────┬─────────┘
                     └──────────────────┘             │
                                                      ▼
                                         ┌────────────────────┐
                                         │  JPEG → img2pdf →  │
                                         │     PDF to chat    │
                                         └────────────────────┘
                                                      │
                                    QR/Barcodes ◀────┘
                                    (if found)
```

### ⚙️ User Settings

| Setting | Values | Default |
|---------|--------|---------|
| Language | `ru` / `en` | `en` |
| JPEG Quality | 75 / 85 / 95 | 95 |
| PDF Format | standard / compressed | standard |
| Text Format | pdf / docx / txt | pdf |
| Notifications | on / off | on |

Stored in SQLite (`user_data.db`).

### 🛠️ Technology Stack

- **[python-telegram-bot](https://python-telegram-bot.org/)** 20+ — async Bot API wrapper
- **[OpenCV](https://opencv.org/)** — edge detection, perspective transform, CLAHE
- **[Pillow](https://python-pillow.org/)** — filters and EXIF normalization
- **[pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar/)** — QR/barcode recognition
- **[img2pdf](https://gitlab.mister-muffin.de/josch/img2pdf)** — JPEG → PDF without re-encoding
- **[reportlab](https://www.reportlab.com/)** / **[python-docx](https://python-docx.readthedocs.io/)** — document generation

### 📜 License

MIT © scandf contributors

---

<div align="center">

**Made with ❤️ by Lesaght**

</div>
