![foodgram_workflow](https://github.com/netzen86/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
## Пример

* [http://foodgram.netzen.dev/](http://foodgram.netzen.dev/)

  Логин: ivan@mail.ru

  Пароль: p@s$w0rd777

* [http://foodgram.netzen.dev/admin/](http://foodgram.netzen.dev/admin/)

  Логин: admin

  Пароль: p@s$w0rd777

* [http://foodgram.netzen.dev/api/docs/](http://foodgram.netzen.dev/api/docs/)

# Технологии

Django 2.2.16
Django REST framework 3.12.4
Gunicorn 20.0.4
Nginx 1.21.3
Postgres 13.0
Docker-compose 1.29.2
Github actions

## Запуск приложения

Скопировать файлы на сервер в домашний каталог
```
docker-compose.yaml и 
./nginx/default.conf
```
Запушить проект на github 
```
git add .
git commit -m 'коментарий'
git push
```
Для выполнения миграции выполните на сервере команду
```
docker-compose exec web python manage.py migrate
````
Для создания пользователя с правами администратора выполните на сервере команду
```
docker-compose exec web python manage.py createsuperuser
```
Собрать статические файлы из нескольких приложений в один каталог
```
docker-compose exec web python manage.py collectstatic --no-input 
```

### Docker

```bash
docker-compose -f ./infra/docker-compose.yml up -d

docker build . -f ./backend/Dockerfile

docker-compose -f ./infra/docker-compose.yml exec web python manage.py fill_db
docker-compose -f ./infra/docker-compose.yml exec web python manage.py createsuperuser

```

[Docker Hub](https://hub.docker.com/repository/docker/nezen86/foodgram)


## API

[http://food.gram/api/docs/](http://food.gram/api/docs/)