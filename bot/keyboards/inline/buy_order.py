from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_continue_buy(order_id):
    markup_buy = InlineKeyboardMarkup()

    markup_buy.add(InlineKeyboardButton("Всё верно ✔", callback_data='PAYMENT_ORDER_'+str(order_id)))

    return markup_buy
