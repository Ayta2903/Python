# config.py
# ВНИМАНИЕ: Замените токен на свой перед запуском!
# Никогда не коммитьте этот файл с реальным токеном в git!

BASE_URL = "https://ru.yougile.com/api-v2"

# Инструкция для наставника:
# 1. Получите свой токен в Yougile
# 2. Замените значение ниже на ваш токен
API_KEY = "A25-EVvVVQgDlv2GvtJYoh21zCAAcJealS-vJEurG4JR4aXbp5S4Mwfc4xtpxk6U"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}