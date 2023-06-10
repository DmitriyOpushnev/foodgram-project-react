# Foodgram. Дипломный проект. РИДМИ БУДЕТ ДОДЕЛАН ПОСЛЕ ВТОРОЙ ЧАСТИ!

sudo curl -L "https://github.com/docker/compose/releases/download/v2.17.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

Уникальный юзернейм: admin
Адрес электронной почты: admin@admin.ru
Имя: admin
Фамилия: admin
Пароль: admin

### Используемые технологии:
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![image](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

## Описание проекта:
Это продуктовый помощник, сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Работа с API:
| Увидеть спецификацию API вы сможете по адресу | `.../api/docs/` |
|--------|:---------|
- Аутентификация выполняется с помощью djoser-токена.

### Доступные запросы:
| Запрос | Эндпоинт | Метод |
|--------|:---------|-------|
| Регистрация нового пользователя |`.../api/users/`| GET, POST |
| Запрос или сменна данных пользователя |`.../api/users/me/`| GET, POST |
| Запрос данных о пользователе |`.../api/users/{user_id}/`| GET |
| Получение токена (авторизация)|`.../api/auth/token/login/`| POST |
| Получение всех рецептов, создать новый рецепт|`.../api/recipes/`| GET, POST |
| Получение, редактирование, удаление рецепта по id|`.../api/recipes/`| GET, PUT, PATCH, DELETE |
| Список всех тегов|`.../api/tags/`| GET |
| Получение информации о теге по id|`.../api/tags/{tag_id}/`| GET |
| Получение списка всех ингредиентов|`.../api/igredients/`| GET |
| Получение информации о ингредиенте по id|`.../api/igredients/{igredient_id}/`| GET |
| Подписаться, отписаться или получить список всех избранных постов |`.../api/recipes/{recipes_id}/favorite`| GET, POST |
| Добавить, удалить или получить список всех рецептов в корзин |`.../api/recipes/{recipes_id}/favorite`| GET, POST |
| Получение списока ингредиентов в формате pdf|`.../api/recipes/download_shopping_cart`| GET |

### Установка
**Как запустить проект:**
```
Клонировать репозиторий и перейти в него в командной строке:
git clone https://github.com/DmitriyOpushnev/foodgram-project-react
```
```
Cоздать и активировать виртуальное окружение:
python -m venv venv (если вы пользователь MacOS python3 -m venv venv)
source venv/bin/activate
```
```
Установить зависимости из файла requirements.txt:
python -m pip install --upgrade pip (если вы пользователь MacOS python3 -m pip install --upgrade pip)
pip install -r requirements.txt (если вы пользователь MacOS python3 pip install -r requirements.txt)
```
```
Выполнить миграции:
python manage.py migrate (если вы пользователь MacOS python3 manage.py migrate)
```
```
Запустить проект:
python manage.py runserver (если вы пользователь MacOS python3 manage.py runserver)
```
```
Создайте супер пользователя.
Например:
python manage.py createsuperuser
Username: Admin
Password: Admin
```
```
Загрузите данные в базу. Для этого в проект встроен механизм Import-Export. Таблицу ингредиентов и тэгов из папки data можно загрузить в базу данных прямо в панели администратора.
```

### Шаблон для .env файла
```
DB_HOST=localhost
DB_PORT=5432
DB_ENGINE=django.db.backends.postgresql
POSTGRES_PASSWORD=postgres
POSTGRES_USER=postgres
POSTGRES_DB=postgres
```