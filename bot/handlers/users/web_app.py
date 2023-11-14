
import json
import requests

from aiogram.types import Message, ContentType

from loader import dp
from models import User

@dp.message_handler(content_types=[ContentType.WEB_APP_DATA])
async def _web_app(message: Message, user: User):
    resp = json.loads(message.web_app_data.data)
    res_list = ''
    total = 0
    products = []
    products.append(resp[0])

    for res in resp[0]:
        res_list = res_list + res["title"] + '. Кол-во: ' + str(res["qty"]) + '\n'
        total = int(total) + int(res["price"]) * int(res["qty"])

    for res in resp[1]:
        address = res["address"]
        res_list = res_list + 'Доставка: ' + address + '\n'
        price_dostavka = int(res["price"])

    text = f'Вы выбрали:\n' + str(res_list) + 'Итого к оплате: ' + str(total+price_dostavka) + ' руб.'

    data = {
        'products': json.dumps(products),
        'price': total,
        'user_id': message.from_user.id,
        'address': address,
        'address_price': price_dostavka,
    }

    print(data)
    headers = {'Content-Type': 'application/json'}

    response = requests.post('http://127.0.0.1:8000/api/orders', json=data, headers=headers)
    print(response)

    await message.answer(text)
