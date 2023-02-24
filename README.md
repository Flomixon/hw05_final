# REST API сервис для отзывов пользователей на фильмы, книги и музыку

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
git clone https://github.com/Flomixon/api_yamdb.git
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
Выполнить миграции:
```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```

## :page_with_curl: Проектная документация:
Документация для API доступна по адресу
```
http://127.0.0.1:8000/redoc/
```

## :office_worker: Атор: 
[Ермолов Виталий](https://github.com/Flomixon)
