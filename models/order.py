from datetime import datetime

from peewee import IdentityField, CharField, DateTimeField, BigIntegerField, IntegerField
from playhouse.postgres_ext import BinaryJSONField

from .base import BaseModel


class OrderBuy(BaseModel):
    id = IdentityField(primary_key=True)
    user_id = BigIntegerField()
<<<<<<< HEAD
    user_name = CharField(null=True)
    products = BinaryJSONField()
    price = IntegerField(default='ru')
    payment_status = IntegerField(default=1)
    phone_number = CharField(null=True)
=======
    products = BinaryJSONField()
    price = IntegerField(default='ru')
    payment_status = IntegerField(default=1)
>>>>>>> origin/master
    address = CharField(default=None)
    address_price = IntegerField(default=None)
    payment_number = CharField(default=None)

    created_at = DateTimeField(default=lambda: datetime.utcnow())

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    class Meta:
        table_name = 'orders'
