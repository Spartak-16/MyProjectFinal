# ======================================================================
# ТЕЛЕГРАМ БОТ - КАЛЬКУЛЯТОР
# ======================================================================
# Бот для выполнения математических операций:
# - Базовые: +, -, *, /, **, //, %
# - Тригонометрия: sin, cos, tan
# - Обратная тригонометрия: asin, acos, atan
# - Гиперболические: sinh, cosh, tanh, asinh, acosh, atanh
# - Логарифмы и корни: sqrt, ln, log10, log2, факториал
# - Целочисленные: НОД, НОК
# ======================================================================

# ======================================================================
# 1. ИМПОРТ НЕОБХОДИМЫХ БИБЛИОТЕК
# ======================================================================
import math  # Математические функции
import operator  # Базовые операции + - * /
from typing import Dict, Callable  # Для указания типов

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ======================================================================
# 2. КОНФИГУРАЦИЯ БОТА (ТОКЕН И ДАННЫЕ)
# ======================================================================
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
BOT_TOKEN = "8445380198:AAFPMj-5miqfBsJatNkW-FAH25f26vtsuV8"  # ВАШ ТОКЕН

# ======================================================================
# 3. ХРАНИЛИЩЕ СОСТОЯНИЙ ПОЛЬЗОВАТЕЛЕЙ
# ======================================================================
# Для каждого пользователя храним:
# - op: выбранную операцию (например "+")
# - arity: количество аргументов (1 или 2)
# - type: тип чисел ("int" или "float")
user_calc_state: Dict[int, dict] = {}


# ======================================================================
# 4. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ ОПЕРАЦИЙ
# ======================================================================
def _meta(func, arity, type_="float", domain=None):
    """Создаёт метаданные для операции"""
    return {"func": func, "arity": arity, "type": type_, "domain": domain}


def _check_domain(domain, *args):
    """Проверяет область определения функции"""
    if not domain:
        return None
    try:
        ok = domain(*args)
    except:
        return "Ошибка проверки"
    if not ok:
        return "Аргументы вне области определения"
    return None


# ======================================================================
# 5. СЛОВАРЬ ВСЕХ МАТЕМАТИЧЕСКИХ ОПЕРАЦИЙ
# ======================================================================
OPS = {
    # ----- БАЗОВЫЕ АРИФМЕТИЧЕСКИЕ (2 аргумента) -----
    "+": _meta(operator.add, 2, "float"),
    "-": _meta(operator.sub, 2, "float"),
    "*": _meta(operator.mul, 2, "float"),
    "/": _meta(operator.truediv, 2, "float", domain=lambda a, b: b != 0),  # проверка деления на 0
    "**": _meta(operator.pow, 2, "float"),
    "//": _meta(operator.floordiv, 2, "int", domain=lambda a, b: b != 0),
    "%": _meta(operator.mod, 2, "int", domain=lambda a, b: b != 0),

    # ----- ТРИГОНОМЕТРИЯ (1 аргумент) -----
    "sin": _meta(math.sin, 1, "float"),
    "cos": _meta(math.cos, 1, "float"),
    "tan": _meta(math.tan, 1, "float"),

    # ----- ОБРАТНАЯ ТРИГОНОМЕТРИЯ (1 аргумент) -----
    "asin": _meta(math.asin, 1, "float", domain=lambda x: -1.0 <= x <= 1.0),
    "acos": _meta(math.acos, 1, "float", domain=lambda x: -1.0 <= x <= 1.0),
    "atan": _meta(math.atan, 1, "float"),

    # ----- ГИПЕРБОЛИЧЕСКИЕ (1 аргумент) -----
    "sinh": _meta(math.sinh, 1, "float"),
    "cosh": _meta(math.cosh, 1, "float"),
    "tanh": _meta(math.tanh, 1, "float"),
    "asinh": _meta(math.asinh, 1, "float"),
    "acosh": _meta(math.acosh, 1, "float", domain=lambda x: x >= 1.0),
    "atanh": _meta(math.atanh, 1, "float", domain=lambda x: -1.0 < x < 1.0),

    # ----- ЛОГАРИФМЫ, КОРНИ, ФАКТОРИАЛ (1 аргумент) -----
    "sqrt": _meta(math.sqrt, 1, "float", domain=lambda x: x >= 0.0),
    "log": _meta(math.log, 1, "float", domain=lambda x: x > 0.0),
    "log10": _meta(math.log10, 1, "float", domain=lambda x: x > 0.0),
    "log2": _meta(math.log2, 1, "float", domain=lambda x: x > 0.0),
    "factorial": _meta(math.factorial, 1, "int", domain=lambda n: n >= 0),

    # ----- ЦЕЛОЧИСЛЕННЫЕ СПЕЦ-ОПЕРАЦИИ (2 аргумента) -----
    "gcd": _meta(math.gcd, 2, "int"),
    "lcm": _meta(math.lcm, 2, "int"),
}


# ======================================================================
# 6. ФУНКЦИИ ПАРСИНГА ЧИСЕЛ (ПРЕОБРАЗОВАНИЕ СТРОК В ЧИСЛА)
# ======================================================================
def parse_number(text, want_int):
    """Преобразует строку в число (int или float)"""
    t = text.strip().replace(",", ".")  # запятую на точку
    if want_int:
        if "." in t or "e" in t.lower():
            return int(float(t))
        return int(t)
    return float(t)


def parse_numbers(text, count, want_int):
    """Преобразует строку с несколькими числами в список"""
    parts = text.strip().replace(",", ".").split()
    if len(parts) != count:
        raise ValueError("Неверное количество аргументов")
    return [parse_number(p, want_int) for p in parts]


# ======================================================================
# 7. КНОПКИ (ОБЫЧНАЯ КЛАВИАТУРА ВНИЗУ ЭКРАНА)
# ======================================================================
# Кнопка для вызова калькулятора в главном меню
calc_button = KeyboardButton("🧮 Калькулятор")

# Главная клавиатура (отображается внизу всегда)
main_keyboard = ReplyKeyboardMarkup(
    [[calc_button]],
    resize_keyboard=True
)

# ======================================================================
# 8. INLINE-КНОПКИ (ПОД СООБЩЕНИЯМИ) - ГЛАВНОЕ МЕНЮ РАЗДЕЛОВ
# ======================================================================
calc_sections = InlineKeyboardMarkup([
    # Строка 1: Базовые и Тригонометрия
    [InlineKeyboardButton("➕ Базовые операции", callback_data="cat_basic"),
     InlineKeyboardButton("📐 Тригонометрия", callback_data="cat_trig")],
    # Строка 2: Обратные триг. и Гиперболические
    [InlineKeyboardButton("🔄 Обратные триг.", callback_data="cat_invtrig"),
     InlineKeyboardButton("📈 Гиперболические", callback_data="cat_hyp")],
    # Строка 3: Логи и корни и Целочисленные
    [InlineKeyboardButton("🔢 Логи и корни", callback_data="cat_log"),
     InlineKeyboardButton("🔢 Целочисленные", callback_data="cat_int")]
])

# ======================================================================
# 9. INLINE-КНОПКИ - БАЗОВЫЕ ОПЕРАЦИИ
# ======================================================================
basic_keys = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ Сложение (+)", callback_data="op_+"),
     InlineKeyboardButton("➖ Вычитание (-)", callback_data="op_-"),
     InlineKeyboardButton("✖️ Умножение (*)", callback_data="op_*")],
    [InlineKeyboardButton("➗ Деление (/)", callback_data="op_/"),
     InlineKeyboardButton("** Степень", callback_data="op_**")],
    [InlineKeyboardButton("// Цел. деление", callback_data="op_//"),
     InlineKeyboardButton("% Остаток", callback_data="op_%")],
    [InlineKeyboardButton("◀️ Назад", callback_data="back")]
])

# ======================================================================
# 10. INLINE-КНОПКИ - ТРИГОНОМЕТРИЯ
# ======================================================================
trig_keys = InlineKeyboardMarkup([
    [InlineKeyboardButton("sin", callback_data="op_sin"),
     InlineKeyboardButton("cos", callback_data="op_cos"),
     InlineKeyboardButton("tan", callback_data="op_tan")],
    [InlineKeyboardButton("◀️ Назад", callback_data="back")]
])

# ======================================================================
# 11. INLINE-КНОПКИ - ОБРАТНАЯ ТРИГОНОМЕТРИЯ
# ======================================================================
invtrig_keys = InlineKeyboardMarkup([
    [InlineKeyboardButton("asin", callback_data="op_asin"),
     InlineKeyboardButton("acos", callback_data="op_acos"),
     InlineKeyboardButton("atan", callback_data="op_atan")],
    [InlineKeyboardButton("◀️ Назад", callback_data="back")]
])

# ======================================================================
# 12. INLINE-КНОПКИ - ГИПЕРБОЛИЧЕСКИЕ ФУНКЦИИ
# ======================================================================
hyp_keys = InlineKeyboardMarkup([
    [InlineKeyboardButton("sinh", callback_data="op_sinh"),
     InlineKeyboardButton("cosh", callback_data="op_cosh"),
     InlineKeyboardButton("tanh", callback_data="op_tanh")],
    [InlineKeyboardButton("asinh", callback_data="op_asinh"),
     InlineKeyboardButton("acosh", callback_data="op_acosh"),
     InlineKeyboardButton("atanh", callback_data="op_atanh")],
    [InlineKeyboardButton("◀️ Назад", callback_data="back")]
])

# ======================================================================
# 13. INLINE-КНОПКИ - ЛОГАРИФМЫ, КОРНИ, ФАКТОРИАЛ
# ======================================================================
log_keys = InlineKeyboardMarkup([
    [InlineKeyboardButton("√ Квадратный корень", callback_data="op_sqrt"),
     InlineKeyboardButton("! Факториал", callback_data="op_factorial")],
    [InlineKeyboardButton("ln (натуральный)", callback_data="op_log"),
     InlineKeyboardButton("log10", callback_data="op_log10"),
     InlineKeyboardButton("log2", callback_data="op_log2")],
    [InlineKeyboardButton("◀️ Назад", callback_data="back")]
])

# ======================================================================
# 14. INLINE-КНОПКИ - ЦЕЛОЧИСЛЕННЫЕ ОПЕРАЦИИ
# ======================================================================
int_keys = InlineKeyboardMarkup([
    [InlineKeyboardButton("НОД (GCD)", callback_data="op_gcd"),
     InlineKeyboardButton("НОК (LCM)", callback_data="op_lcm")],
    [InlineKeyboardButton("// Цел. деление", callback_data="op_//"),
     InlineKeyboardButton("% Остаток", callback_data="op_%")],
    [InlineKeyboardButton("◀️ Назад", callback_data="back")]
])

# ======================================================================
# 15. СОЗДАНИЕ ЭКЗЕМПЛЯРА БОТА
# ======================================================================
bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# ======================================================================
# 16. ОБРАБОТЧИК КОМАНДЫ /start
# ======================================================================
@bot.on_message(filters.command("start"))
async def start_command(client, msg):
    """Приветствие при запуске бота"""
    await msg.reply(
        f"👋 Привет, {msg.from_user.first_name}!\n\n"
        f"🤖 Я бот-калькулятор!\n"
        f"📱 Нажми на кнопку '🧮 Калькулятор' внизу, чтобы начать.",
        reply_markup=main_keyboard
    )


# ======================================================================
# 17. ОСНОВНОЙ ОБРАБОТЧИК ТЕКСТОВЫХ СООБЩЕНИЙ
# ======================================================================
@bot.on_message(filters.text)
async def handle_text_messages(client, msg):
    """
    Обрабатывает:
    1. Нажатие на кнопку "🧮 Калькулятор"
    2. Ввод чисел для вычисления
    3. Обычные сообщения
    """

    # ----- 17.1. НАЖАТИЕ НА КНОПКУ "🧮 Калькулятор" -----
    if msg.text == "🧮 Калькулятор":
        await msg.reply(
            "📚 Выберите раздел калькулятора:",
            reply_markup=calc_sections
        )
        return

    # ----- 17.2. ВВОД ЧИСЕЛ ДЛЯ ВЫЧИСЛЕНИЯ -----
    user_id = msg.from_user.id

    # Проверяем, есть ли у пользователя активная операция
    if user_id in user_calc_state:
        state = user_calc_state[user_id]
        meta = OPS.get(state["op"])

        if not meta:
            del user_calc_state[user_id]
            return

        # Парсим введённые числа
        try:
            nums = parse_numbers(msg.text, meta["arity"], meta["type"] == "int")
        except:
            if meta["arity"] == 2:
                await msg.reply("❌ Нужно ввести 2 числа через пробел\n📝 Пример: 12 7")
            else:
                await msg.reply("❌ Нужно ввести 1 число\n📝 Пример: 0.5")
            return

        # Проверяем область определения
        domain_check = _check_domain(meta.get("domain"), *nums)
        if domain_check:
            await msg.reply(f"⚠️ {domain_check}")
            return

        # Вычисляем результат
        try:
            result = meta["func"](*nums)
            del user_calc_state[user_id]  # Очищаем состояние

            # Добавляем примечание для тригонометрии
            note = ""
            if state["op"] in ["sin", "cos", "tan", "asin", "acos", "atan",
                               "sinh", "cosh", "tanh", "asinh", "acosh", "atanh"]:
                note = "\n📐 (углы в радианах)"

            await msg.reply(
                f"✅ Результат: {result}{note}",
                reply_markup=main_keyboard
            )
        except Exception as e:
            await msg.reply(f"❌ Ошибка вычисления: {e}")

    # ----- 17.3. ОБЫЧНЫЕ СООБЩЕНИЯ (НЕ КОМАНДЫ, НЕ КАЛЬКУЛЯТОР) -----
    else:
        await msg.reply(
            "🤔 Используй кнопку 🧮 Калькулятор внизу!\n\n"
            "📌 Или напиши команду /start",
            reply_markup=main_keyboard
        )


# ======================================================================
# 18. ОБРАБОТЧИК НАЖАТИЙ НА INLINE-КНОПКИ
# ======================================================================
@bot.on_callback_query()
async def handle_inline_buttons(client, query):
    """
    Обрабатывает нажатия на inline-кнопки:
    - Выбор категории (cat_*)
    - Выбор операции (op_*)
    - Кнопка "Назад"
    """
    data = query.data

    # ----- 18.1. КНОПКА "НАЗАД" -----
    if data == "back":
        await query.message.edit_text(
            "📚 Выберите раздел калькулятора:",
            reply_markup=calc_sections
        )
        await query.answer()
        return

    # ----- 18.2. ВЫБОР КАТЕГОРИИ -----
    categories = {
        "cat_basic": ("🧮 Базовые операции:", basic_keys),
        "cat_trig": ("📐 Тригонометрия (углы в радианах):", trig_keys),
        "cat_invtrig": ("🔄 Обратные тригонометрические (радианы):", invtrig_keys),
        "cat_hyp": ("📈 Гиперболические функции:", hyp_keys),
        "cat_log": ("🔢 Логарифмы, корни, факториал:", log_keys),
        "cat_int": ("🔢 Целочисленные операции:", int_keys),
    }

    if data in categories:
        text, keyboard = categories[data]
        await query.message.edit_text(text, reply_markup=keyboard)
        await query.answer()
        return

    # ----- 18.3. ВЫБОР ОПЕРАЦИИ -----
    # Словарь соответствия callback_data -> имя операции
    op_map = {
        "op_+": "+", "op_-": "-", "op_*": "*", "op_/": "/", "op_**": "**",
        "op_//": "//", "op_%": "%", "op_sin": "sin", "op_cos": "cos",
        "op_tan": "tan", "op_asin": "asin", "op_acos": "acos", "op_atan": "atan",
        "op_sinh": "sinh", "op_cosh": "cosh", "op_tanh": "tanh",
        "op_asinh": "asinh", "op_acosh": "acosh", "op_atanh": "atanh",
        "op_sqrt": "sqrt", "op_factorial": "factorial", "op_log": "log",
        "op_log10": "log10", "op_log2": "log2", "op_gcd": "gcd", "op_lcm": "lcm"
    }

    if data in op_map:
        op = op_map[data]
        meta = OPS.get(op)

        if meta:
            # Сохраняем состояние пользователя
            user_calc_state[query.from_user.id] = {
                "op": op,
                "arity": meta["arity"],
                "type": meta["type"]
            }

            await query.answer("🔢 Введите числа!")

            # Подсказка о формате ввода
            if meta["arity"] == 2:
                await query.message.reply(
                    "📝 Введите 2 числа через пробел\n"
                    "Пример: 5 3",
                    reply_markup=main_keyboard
                )
            else:
                await query.message.reply(
                    "📝 Введите 1 число\n"
                    "Пример: 0.5",
                    reply_markup=main_keyboard
                )


# ======================================================================
# 19. ЗАПУСК БОТА
# ======================================================================
if __name__ == "__main__":
    print("=" * 50)
    print("✅ ТЕЛЕГРАМ БОТ-КАЛЬКУЛЯТОР ЗАПУЩЕН")
    print("=" * 50)
    print("📱 Имя бота: @Calc_16_bot")
    print("📝 Команды: /start")
    print("🔄 Для остановки нажмите Ctrl+C")
    print("=" * 50)

    bot.run()

