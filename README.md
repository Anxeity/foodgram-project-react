![workflow](https://github.com/Anxeity/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?)

### foodgram-project-react

# Дипломный проект курса "Python Developer"



### Описание

Онлайн-сервис на React и API для него. На этом сервисе пользователи 
могут делиться своими рецептами, подписываться на публикации понравившихся пользователей, добавлять понравившиеся рецепты в список «Избранное», 
а перед походом в магазин скачивать сводный список продуктов.

### Запуск проекта на Docker Desktop

Скопируйте проект на локальный жесткий диск:

```
git clone https://github.com/Anxeity/foodgram-project-react.git
```

Cоздайте и активируйте виртуальное окружение для этого проекта:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установите зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перейдите в директорию проекта:

```
cd backend
```

Создайте файл .env в директории backend и заполните его данными по этому 
образцу:

```
SECRET_KEY = '&r-+k65)-z9v5)of7!yn#^4nt6iao^%hk(1evtkh6i07e4a1eh'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DEBUG = True
```

Создайте образ backend (текущая директория должна быть backend):

```
docker build -t ######### .
```

Перейдите в директорию infra:

```
cd ../infra
```

Запустите docker-compose:

```
docker-compose up
```

Выполните миграции в контейнере созданном из образа backend:

```
docker-compose exec -T backend python manage.py migrate
```

Загрузите статические файлы в контейнере созданном из образа backend:

```
docker-compose exec -T backend python manage.py collectstatic --no-input
```

Запустите проект в браузере.
Введите в адресную строку браузера:

```
localhost
```

#### В проекте использованы технологии:
* Python
* React
* Django REST Framework
* Django
* Linux
* Docker
* Docker-compose
* Postgres
* Gunicorn
* Nginx
* Workflow

