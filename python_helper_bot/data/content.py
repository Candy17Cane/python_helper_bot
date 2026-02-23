CONTENT = {
    "oop": {
        "title": "ООП",
        "topics": {
            "classes": {
                "title": "Классы",
                "text": "Класс - это шаблон для создания обьектов.",
                "simple": "Класс - это как чертеж дома",
                "example": "class Car:\n    pass",
                # "image": "images/.png"
            },
            "encapsulation": {
                "title": "Инкапсуляция",
                "text": "Инкапсуляция скрывает внутреннюю реализацию обьекта.",
                "simple": "Ты пользуешься кнопкой, не зная, что внутри.",
                "example": (
                    "class User:\n"
                    "   def __init__(self):\n"
                    "       self.__password = '1234'"
                ),
            },
        },
    },

    "syntax": {
        "title": "Синтаксис",
        "topics": {
            "variables": {
                "title": "Переменная",
                "text": "Переменная - это имя ссылающееся на обьект.",
                "simple": "Это как ярлык на коробке",
                "example": "x = 10\nname = 'Alex'",
            },
        }, 
    },

    "stdlib": {
        "title": "Библиотеки",
        "topics": {
            "requests": {
                "title": "requests",
                "text": "requests - библиотека для HTTP-запросов.",
                "simple": "Позволяет ходить в интернет из Python.",
                "example": "import requests\nr = requests.get('https://example.com')",
            },
        },
    },
}
