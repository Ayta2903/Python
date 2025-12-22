from address import Address
from mailing import Mailing

from_address = Address("677900", "Якутск", "Пушкина", "45", "32")

to_address = Address("114897", "Москва", "Тверская", "5", "10")

mailing = Mailing(to_address, from_address, 500, "2547896")

print(f"Отправление {mailing.track} из {mailing.from_address.index}, {mailing.from_address.city}, {mailing.from_address.street}, {mailing.from_address.house} - {mailing.from_address.apartment} в {mailing.to_address.index}, {mailing.to_address.city}, {mailing.to_address.street}, {mailing.to_address.house} -{mailing.to_address.apartment}. Стоимость {mailing.cost} рублей.")
