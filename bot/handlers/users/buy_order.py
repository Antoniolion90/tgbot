from datetime import datetime

from aiogram.dispatcher.filters import Regexp
from aiogram.types import CallbackQuery, LabeledPrice, ContentType, PreCheckoutQuery, Message

from data import config
from loader import dp, bot
from models import OrderBuy


async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def process_successful_payment(message: Message):
    currency = message.successful_payment.currency
    total_amount = message.successful_payment.total_amount
    id_order = message.successful_payment.invoice_payload
    phone_number = message.successful_payment.order_info.phone_number
    name_client = message.successful_payment.order_info.name
    provider_payment = message.successful_payment.provider_payment_charge_id

    info_pay_user = (
            'ООО Pizza\n' +
            '\n   ОПЛАТА\nДата оплаты: ' + str(datetime.now().strftime("%H:%M %d.%m.%Y")) +
            '\nНОМЕР ПЛАТЕЖА: ' + str(provider_payment) +
            '\nID КЛИЕНТА: ' + str(message.chat.id) +
            ('\nСУММА: {:,} ').format(total_amount / 100).replace(',', ' ') + str(currency) +
            '\nТелефон клиента: ' + str(phone_number) +
            '\n\n   СПАСИБО ЗА ПОКУПКУ!'
    )

    await message.answer(text=info_pay_user)
    
    orderbuy = OrderBuy.update(user_name=name_client, phone_number=phone_number, payment_status=2, payment_number=provider_payment).where(OrderBuy.id == id_order)
    orderbuy.execute()

    for admin_id in config.ADMINS:
        await bot.send_message(admin_id, info_pay_user)


@dp.pre_checkout_query_handler(process_pre_checkout_query)
@dp.message_handler(process_successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)


@dp.callback_query_handler(Regexp('PAYMENT_ORDER_'))
async def _change_payment_markup(callback_query: CallbackQuery):

    code = callback_query.data[14:]

    order = OrderBuy.select().where(OrderBuy.id==code)

    res_list = ''
    total = 0

    for res in order:
        for prod in res.products:
            for ord in prod:
                res_list = res_list + ord["title"] + '. Кол-во: ' + str(ord["qty"]) + '\n'
                total = int(total) + int(ord["price"]) * int(ord["qty"])

    for res in order:
        address = res.address
        res_list = res_list + 'Доставка: ' + address + '\n'
        price_dostavka = int(res.address_price)

    print(total, res_list, price_dostavka)

    await callback_query.message.edit_reply_markup(reply_markup=None)

    currency = "rub"
    foto_url = 'https://i.pinimg.com/736x/5d/b1/7a/5db17ab1f8e0bad184cf9a879b46aaa3.jpg'

    PRICES = [
        LabeledPrice(label='Заказ', amount=total*100),
        LabeledPrice(label='Доставка', amount=price_dostavka*100)
    ]

    await callback_query.bot.send_invoice(chat_id=callback_query.from_user.id,
                                          title='Оформление заказа',
                                          description=res_list,
                                          payload=str(code),
                                          start_parameter='service-pizza-pay',
                                          currency=currency,
                                          prices=PRICES,
                                          photo_url=foto_url,
                                          provider_token=config.PAYMENT_TOKEN,
                                          need_name=True,
                                          need_phone_number=True,
                                          need_email=False,
                                          need_shipping_address=False,
                                          )

