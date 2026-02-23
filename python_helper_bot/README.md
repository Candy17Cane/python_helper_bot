![Tests](https://img.shields.io/github/actions/workflow/status/Candy17Cane/REPO/tests.yml?branch=main)
![Tests](https://img.shields.io/github/actions/workflow/status/Candy17Cane/python-helper-bot/tests.yml)
![Coverage](https://img.shields.io/badge/coverage-70%25-yellow)
![Repo Size](https://img.shields.io/github/repo-size/Candy17Cane/python-helper-bot)
![Last Commit](https://img.shields.io/github/last-commit/Candy17Cane/python-helper-bot)
![License](https://img.shields.io/badge/license-MIT-green)

## Setup

cp .env.example .env
BOT_TOKEN = 7156512157:AAHL3oShVdP_DA7wy3SmI98zuFtD9yOpEN4

# 🐍 Python Helper Telegram Bot

Интерактивный Telegram-бот-справочник по Python с поиском, структурированным контентом и архитектурой production-уровня.

---

## 🚀 Возможности

- 📚 Разделы по темам (ООП, синтаксис, библиотеки и др.)
- 🧠 Объяснение простыми словами
- 📌 Примеры кода
- ⭐ Избранное
- 🔎 Быстрый поиск по темам
- ⚡ Индексированный поиск (in-memory inverted index)
- 🧾 История просмотра (архитектура готова)
- 🛡 Обработка ошибок Telegram API
- 🪵 Полное логирование событий

---

## 🧱 Архитектура проекта

Проект построен по принципам backend-архитектуры с разделением ответственности:

```
handlers/      → входящие события (контроллеры)
services/      → бизнес-логика
storage/       → слой данных (SQLite / Memory)
middlewares/   → logging / rate-limit / DI
utils/         → вспомогательные функции
data/          → контент справочника
```

Архитектурные принципы:

- thin handlers
- service layer
- dependency injection
- config через env
- расширяемость storage слоя
- обратная совместимость callback_data

---

## ⚙️ Технологии

- Python 3.10+
- aiogram 3
- SQLite
- dotenv
- pytest
- logging middleware

---

## 📦 Установка

```bash
git clone https://github.com/yourname/python-helper-bot
cd python-helper-bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔑 Настройка окружения

```bash
cp .env.example .env
```

Заполни `.env`:

```
BOT_TOKEN=your_token
```

---

## ▶️ Запуск

```bash
python bot.py
```

---

## 🧪 Тесты

```bash
pytest -q
```

С покрытием:

```bash
pytest --cov
```

---

## 🪵 Логи

Логи пишутся:

```
logs/bot.log
```

С ротацией:

- 5 файлов
- по 5 MB

---

## 🔍 Поиск

Поиск реализован через inverted index:

```
token → topics
```

Преимущества:

- быстрый поиск
- масштабируемость
- ranking score

---

## 🗄 Storage слой

Поддерживаемые реализации:

- MemoryStorage
- SQLiteStorage

Можно добавить:

- PostgreSQL
- Redis

Без изменения handlers.

---

## 🧠 Callback versioning

Формат callback:

```
topic:v1:section:topic
```

Позволяет:

- обновлять формат
- не ломать старые кнопки

---

## 🛡 Надёжность

Бот устойчив к ошибкам:

- TelegramBadRequest перехватывается
- безопасное редактирование сообщений
- централизованный error middleware
- валидация callback_data

---

## 📈 Production-готовность

Проект поддерживает:

- масштабирование контента
- смену storage
- dev/prod режимы
- логирование
- тесты

---

## 🧑‍💻 Автор

Danil — backend developer

---

## ⭐ Почему этот проект сильный для портфолио

В отличие от типичных учебных ботов:

✔ архитектура сервиса
✔ слой бизнес-логики
✔ индекс поиска
✔ middleware
✔ тесты
✔ конфигурация окружения

---

## 📌 Roadmap

- Redis cache
- Webhook режим
- Web-панель управления
- Admin dashboard
- Multilanguage support

---

## 📜 License

MIT
