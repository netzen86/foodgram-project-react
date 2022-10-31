![foodgram_workflow](https://github.com/netzen86/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# Проект доступен по адресу
* [http://foodgram.netzen.su](http://foodgram.netzen.su)

## Админка проекта
* [http://foodgram.netzen.su/admin/](http://foodgram.netzen.ыг/admin/)

  Логин: admin

  Пароль: p@s$w0rd777

## API проекта
* [http://foodgram.netzen.su/api/docs/](http://foodgram.netzen.su/api/docs/)

# Технологии

Django 2.2.16
Django REST framework 3.12.4
Gunicorn 20.0.4
Nginx 1.21.3
Postgres 13.0
Docker-compose 1.29.2
Github actions

## Запуск приложения

Скопировать файл конфигурации nginx на сервер в домашний каталог
``` 
./nginx/default.conf
```
Запушить проект на github 
```
git add .
git commit -m 'коментарий'
git push
```

# Build docker image

```
docker login -u netzen86
docker build -f backend/Dockerfile -t netzen86/foodgram-back:v1 .
docker push netzen86/foodgram-back:v1 

cd frontend/
docker build . -t netzen86/foodgram-front:v2
docker push netzen86/foodgram-front:v2
```
# Создание миграций в исходниках
```
в папке проекта:
docker compose -f infra/docker-compose-local.yml up db --build -d
cd backend
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
```
# Запуск приложения локально

```
в папке проекта:
docker compose -f infra/docker-compose-local.yml up --build -d
cd infra
docker compose -f docker-compose-local.yml exec backend python3 manage.py migrate
docker compose -f docker-compose-local.yml exec backend python3 manage.py createadmin
docker compose -f docker-compose-local.yml exec backend python3 manage.py fill_db
docker-compose -f docker-compose-local.yml exec backend python manage.py collectstatic --no-input
```
[Docker Hub](https://hub.docker.com/repository/docker/netzen86/foodgram-back)