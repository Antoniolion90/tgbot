from datetime import datetime

from aiogram.dispatcher.filters import Regexp
from aiogram.types import CallbackQuery, LabeledPrice, ContentType, PreCheckoutQuery, Message

from data import config
from loader import dp, _, bot


async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def process_successful_payment(message: Message):
    currency = message.successful_payment.currency
    total_amount = message.successful_payment.total_amount
    id_order = message.successful_payment.invoice_payload
    phone_number = message.successful_payment.order_info.phone_number
    provider_payment = message.successful_payment.provider_payment_charge_id

    info_pay_user = (
            'ООО Pizza\n' +
            '\n   ОПЛАТА\nДата оплаты: ' + str(datetime.now().strftime("%H:%M %d.%m.%Y")) +
            '\nНОМЕР ПЛАТЕЖА: ' + str(provider_payment) +
            '\nID КЛИЕНТА: ' + str(message.chat.id) +
            ('\nСУММА: {:,} ').format(total_amount / 100).replace(',', ' ') + str(currency) +
            '\nТелефон пассажира: ' + str(phone_number) +
            '\n\n   СПАСИБО ЗА ПОКУПКУ!'
    )

    await message.answer(text=info_pay_user)

    for admin_id in config.ADMINS:
        await bot.send_message(admin_id, info_pay_user)


@dp.pre_checkout_query_handler(process_pre_checkout_query)
@dp.message_handler(process_successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)


@dp.callback_query_handler(Regexp('PAYMENT_SERVICE_'))
async def _change_payment_markup(callback_query: CallbackQuery):

    await callback_query.message.edit_reply_markup(reply_markup=None)

    for serv in services:
        title = serv.service
        description = serv.info_reys
        amount = (serv.total_sum) * 100

    currency = "rub"
    foto_url = 'https://i.pinimg.com/736x/5d/b1/7a/5db17ab1f8e0bad184cf9a879b46aaa3.jpg'

    PRICES = [
        LabeledPrice(label='Заказ', amount=4200000),
        LabeledPrice(label='Доставка', amount=30000)
    ]

    await callback_query.bot.send_invoice(chat_id=callback_query.from_user.id,
                                          title=title,
                                          description=description,
                                          payload=str(idService),
                                          start_parameter='service-uzair-pay',
                                          currency=currency,
                                          prices=PRICES,
                                          photo_url=foto_url,
                                          provider_token=config.PAYMENT_TOKEN,
                                          need_name=True,
                                          need_phone_number=True,
                                          need_email=False,
                                          need_shipping_address=False,
                                          )

