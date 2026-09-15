from pyrogram.types import KeyboardButton, InlineKeyboardButton
from pyrogram import emoji
calc_button = KeyboardButton("🧮 Калькулятор")  # калькулятор в главном меню


# === Калькулятор: кнопки навигации по разделам ===
calc_home_button = InlineKeyboardButton("🏠 Разделы", "calc_home")
calc_back_inline_button = InlineKeyboardButton(f"{emoji.BACK_ARROW} Назад", "calc_back")

# Категории калькулятора
cat_basic_inline = InlineKeyboardButton("Базовые", "calc_cat:basic")
cat_trig_inline = InlineKeyboardButton("Тригонометрия", "calc_cat:trig")
cat_invtrig_inline = InlineKeyboardButton("Обратные триг.", "calc_cat:invtrig")
cat_hyp_inline = InlineKeyboardButton("Гиперболические", "calc_cat:hyp")
cat_log_inline = InlineKeyboardButton("Логарифмы/√", "calc_cat:log")
cat_int_inline = InlineKeyboardButton("Целочисленные", "calc_cat:int")

# === Калькулятор: операции ===
# Базовые бинарные
op_add_inline = InlineKeyboardButton("➕", "calc_op:+")
op_sub_inline = InlineKeyboardButton("➖", "calc_op:-")
op_mul_inline = InlineKeyboardButton("✖️", "calc_op:*")
op_div_inline = InlineKeyboardButton("➗", "calc_op:/")
op_pow_inline = InlineKeyboardButton("xʸ", "calc_op:**")
op_fdiv_inline = InlineKeyboardButton("//", "calc_op://")
op_mod_inline = InlineKeyboardButton("%", "calc_op:%")

# Тригонометрия
op_sin_inline = InlineKeyboardButton("sin", "calc_op:sin")
op_cos_inline = InlineKeyboardButton("cos", "calc_op:cos")
op_tan_inline = InlineKeyboardButton("tan", "calc_op:tan")

# Обратные тригонометрические
op_asin_inline = InlineKeyboardButton("asin", "calc_op:asin")
op_acos_inline = InlineKeyboardButton("acos", "calc_op:acos")
op_atan_inline = InlineKeyboardButton("atan", "calc_op:atan")

# Гиперболические и обратные гиперболические
op_sinh_inline = InlineKeyboardButton("sinh", "calc_op:sinh")
op_cosh_inline = InlineKeyboardButton("cosh", "calc_op:cosh")
op_tanh_inline = InlineKeyboardButton("tanh", "calc_op:tanh")
op_asinh_inline = InlineKeyboardButton("asinh", "calc_op:asinh")
op_acosh_inline = InlineKeyboardButton("acosh", "calc_op:acosh")
op_atanh_inline = InlineKeyboardButton("atanh", "calc_op:atanh")

# Логи, корень, факториал
op_sqrt_inline = InlineKeyboardButton("√", "calc_op:sqrt")
op_log_inline = InlineKeyboardButton("ln", "calc_op:log")
op_log10_inline = InlineKeyboardButton("log10", "calc_op:log10")
op_log2_inline = InlineKeyboardButton("log2", "calc_op:log2")
op_fact_inline = InlineKeyboardButton("n!", "calc_op:factorial")

# Целочисленные спец-операции
op_gcd_inline = InlineKeyboardButton("НОД", "calc_op:gcd")
op_lcm_inline = InlineKeyboardButton("НОК", "calc_op:lcm")
