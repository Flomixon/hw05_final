# Yatube проект социальной сети

## :books:Описание:
  Проект Yatube социальная сеть для публикации постов. Можно создавать личные страницы, подписываться на других авторов.
  Публиковать записи в группах по интересам. Комментировать публикации других авторов.

## :satellite: Технологии: 

  - Python
  - Django
  - HTML
  - CSS
  - Bootstrap

## :hammer_and_wrench: Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Flomixon/hw05_final.git
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
Создать и запустить виртуальное окружение.
```
    Windows:
        python -m venv venv
        source venv/Scripts/activate
```
```
    Linux:
        python3 -m venv env
        source env/bin/activate
        python3 -m pip install --upgrade pip
```
        
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

В директории с файлом manage.py создать файл .env и указать в нем:

```
SECRET_KEY = '...' ключ Django
EMAIL_HOST = '...' Хост почтового клиента
EMAIL_PORT = ...  Номер порта клиента
EMAIL_HOST_USER = "..." Логин
EMAIL_HOST_PASSWORD = "..." Пароль
```

Выполнить миграции:
```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```

## :office_worker: Атор: 
[Ермолов Виталий](https://github.com/Flomixon)
