from utils.text import tokens

def test_tokens_basic():
    result = tokens("Класс в Python")
    assert "класс" in result
    assert "python" in result

