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