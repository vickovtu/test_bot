# Требования
- Python 3.8
- pip as package manager
- 3rd packages - in `requirements.txt`
- .env файл

# Установка и запуск
Надо зарегистрировать своего юзер бота на сайте:
```sh
https://my.telegram.org/
```

Создать бота в чате с @BotFather

Создть и активировать виртуальное окружение пайтона
```sh
python -m venv env
source env/bin/activate
``` 

Установить необходимые зависимости
```sh
pip install -r requirements.txt
```
Создать .env файл с параметрами как example.env
nv переменные
```
API_ID=                        апи ид юзер бота с https://my.telegram.org/
API_HASH=                      хеш бота с https://my.telegram.org/
PHONE=                         телефон бота
BOT_TOKEN=                     токен бота зарегистрированого в @BotFather

```
```sh
cp example.env .env
```

Также следует запустить,
при запуске может попросить телефон и пароль с сообщения, что прейдет в телеграм
```sh
python bot.py
```

