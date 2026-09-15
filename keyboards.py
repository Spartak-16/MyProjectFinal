from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
import buttons

# Главное меню
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [buttons.calc_button]
    ],
    resize_keyboard=True
)

# Калькулятор: главное меню разделов
calc_sections_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.cat_basic_inline, buttons.cat_trig_inline],
        [buttons.cat_invtrig_inline, buttons.cat_hyp_inline],
        [buttons.cat_log_inline, buttons.cat_int_inline],
        [buttons.calc_home_button]
    ]
)

# Калькулятор: страницы категорий
calc_basic_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.op_add_inline, buttons.op_sub_inline, buttons.op_mul_inline],
        [buttons.op_div_inline, buttons.op_pow_inline],
        [buttons.op_fdiv_inline, buttons.op_mod_inline],
        [buttons.calc_back_inline_button]
    ]
)

calc_trig_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.op_sin_inline, buttons.op_cos_inline, buttons.op_tan_inline],
        [buttons.calc_back_inline_button]
    ]
)

calc_invtrig_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.op_asin_inline, buttons.op_acos_inline, buttons.op_atan_inline],
        [buttons.calc_back_inline_button]
    ]
)

calc_hyp_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.op_sinh_inline, buttons.op_cosh_inline, buttons.op_tanh_inline],
        [buttons.op_asinh_inline, buttons.op_acosh_inline, buttons.op_atanh_inline],
        [buttons.calc_back_inline_button]
    ]
)

calc_log_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.op_sqrt_inline, buttons.op_fact_inline],
        [buttons.op_log_inline, buttons.op_log10_inline, buttons.op_log2_inline],
        [buttons.calc_back_inline_button]
    ]
)

calc_int_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.op_gcd_inline, buttons.op_lcm_inline],
        [buttons.op_fdiv_inline, buttons.op_mod_inline],
        [buttons.calc_back_inline_button]
    ]
)
