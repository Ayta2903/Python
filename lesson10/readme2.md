## Тестирование калькулятора (Slow Calculator)

Проект также включает тесты для проверки калькулятора с задержкой на сайте [Slow Calculator](https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html).

### Особенности тестов калькулятора

- **Проверка сложения** с различными значениями задержки
- **Проверка всех операций**: сложение, вычитание, умножение, деление
- **Параметризованные тесты** для проверки множества сценариев
- **Работа с десятичными числами**

### Запуск только тестов калькулятора

```bash
# Запуск всех тестов калькулятора
pytest tests/test_calculator.py --alluredir=allure-results -v

# Запуск конкретного теста
pytest tests/test_calculator.py::TestCalculator::test_calculator_addition --alluredir=allure-results -v

# Запуск с параметризацией (будут выполнены все варианты)
pytest tests/test_calculator.py -k "addition" --alluredir=allure-results -v