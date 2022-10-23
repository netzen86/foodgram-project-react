![foodgram_workflow](https://github.com/netzen86/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
## Пример

* [http://foodgram.netzen.dev/](http://foodgram.netzen.dev/)

  Логин: ivan@mail.ru

  Пароль: p@s$w0rd777

* [http://foodgram.netzen.dev/admin/](http://foodgram.netzen.dev/admin/)

  Логин: admin

  Пароль: p@s$w0rd777

* [http://foodgram.netzen.dev/api/docs/](http://foodgram.netzen.dev/api/docs/)

## Установка

1. `git clone git@github.com:netzen86/foodgram-project-react.git`

2. Заполнить файл `infra/.env` (пример в `infra/.env.example`)

```
# указываем, что работаем с postgresql
DB_ENGINE=django.db.backends.postgresql

# имя базы данных
DB_NAME=

# логин для подключения к базе данных
POSTGRES_USER=

# пароль для подключения к БД
POSTGRES_PASSWORD=

# название сервиса (контейнера)
DB_HOST=db

# порт для подключения к БД
DB_PORT=5432

# django secret key
SECRET_KEY=

```

### Docker

```bash
docker-compose -f ./infra/docker-compose.yml up -d

# docker build . -f ./backend/Dockerfile

docker-compose -f ./infra/docker-compose.yml exec web python manage.py fill_db
docker-compose -f ./infra/docker-compose.yml exec web python manage.py createsuperuser

```

[Docker Hub](https://hub.docker.com/repository/docker/nezen86/foodgram)


## API

[http://food.gram/api/docs/](http://food.gram/api/docs/)