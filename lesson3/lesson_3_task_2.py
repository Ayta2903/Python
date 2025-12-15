from smartphone import Smartphone

catalog = [
    Smartphone("Apple", "iPhone 16", "+79241738662")
]

for phone in catalog:
    print(f"{phone.brand} - {phone.model}. {phone.phone_number}")
