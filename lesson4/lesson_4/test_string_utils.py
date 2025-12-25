import pytest
from string_utils import StringUtils

utils = StringUtils()


def test_capitalize_positive():
    assert utils.capitalize("hello") == "Hello"

def test_capitalize_empty():
    assert utils.capitalize("") == ""

def test_trim_positive():
    assert utils.trim("   hello") == "   hello"[len("   hello") - len("hello"):]

def test_trim_no_spaces():
    assert utils.trim("hello") == "hello"

def test_trim_all_spaces():
    assert utils.trim("     ") == ""

def test_to_list_default_delimiter():
    assert utils.to_list("a,b,c") == ["a", "b", "c"]

def test_to_list_custom_delimiter():
    assert utils.to_list("1:2:3", ":") == ["1", "2", "3"]

def test_to_list_empty_string():
    assert utils.to_list("") == []



def test_contains_positive():
    
    assert utils.contains("hello", "e") is True

def test_contains_negative():
    assert utils.contains("hello", "z") is False

def test_contains_empty_string():
    assert utils.contains("", "a") is False
    
def test_contains_empty_symbol():
    assert utils.contains("hello", "") is True 

def test_delete_symbol_single_char():
    assert utils.delete_symbol("программа", "г") == "прорама"

def test_delete_symbol_first_char():
    assert utils.delete_symbol("тест", "т") == "ес"

def test_delete_symbol_last_char():
    assert utils.delete_symbol("код", "д") == "ко"

def test_delete_symbol_multiple_occurrences():
    assert utils.delete_symbol("банан", "а") == "бнн"

def test_delete_symbol_substring_middle():
    assert utils.delete_symbol("автомобиль", "мобиль") == "авто"

def test_delete_symbol_substring_duplicates():
    assert utils.delete_symbol("хахаха", "ха") == ""

def test_delete_symbol_not_found():
    assert utils.delete_symbol("пример", "z") == "пример"
    assert utils.delete_symbol("текст", "абв") == "текст"

def test_delete_symbol_empty_string():
    assert utils.delete_symbol("", "а") == ""

def test_delete_symbol_empty_symbol():
    assert utils.delete_symbol("строка", "") == "строка"

def test_delete_symbol_identical_strings():
    assert utils.delete_symbol("abc", "abc") == ""

def test_delete_symbol_whitespace():
    assert utils.delete_symbol("раз два три", " ") == "раздватри"

def test_delete_symbol_special_chars():
    assert utils.delete_symbol("email@mail.ru", "@") == "emaimail.ru"
    assert utils.delete_symbol("путь/к/файлу", "/") == "путькфайлу"
