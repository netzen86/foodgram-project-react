![foodgram_workflow](https://github.com/netzen86/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# Проект доступен по адресу
* [http://foodgram.netzen.dev](http://foodgram.netzen.dev)

## Админка проекта
* [http://foodgram.netzen.dev/admin/](http://foodgram.netzen.dev/admin/)

## Оприсание API проекта
* [http://foodgram.netzen.dev/api/docs/](http://foodgram.netzen.dev/api/docs/)

# Технологии

- Django 2.2.16
- Django REST framework 3.12.4
- Gunicorn 20.0.4
- Nginx 1.21.3
- Postgres 13.0
- Docker-compose 1.29.2
- DockerHub
- GitHub
- Github actions
- Yandex cloud

# Запуск приложения
## Сборка docker image фронтэнда
```
docker login
cd frontend/
docker build . -t "ваш логин DockerHub"/foodgram-front:v1
docker push "ваш логин DockerHub"/foodgram-front:v1
```
## Запушить проект на github 
```
git add .
git commit -m 'коментарий'
git push
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
закоментировать строки конфигурации https в файле конфигурации NGINX (/infra/nginx.conf)
в папке проекта:
docker compose -f infra/docker-compose-local.yml up --build -d
cd infra
docker compose -f docker-compose-local.yml exec backend python3 manage.py migrate
docker compose -f docker-compose-local.yml exec backend python3 manage.py createadmin
docker compose -f docker-compose-local.yml exec backend python3 manage.py fill_db
docker-compose -f docker-compose-local.yml exec backend python manage.py collectstatic --no-input
```
# TODO
- добавить в piplene генерацию ssl сертификатов
- реализовать функцию подтверждения e-mail
- реализовать функцию сброса пароля
- написать тесты

# Авторы
- Бэкенд: Дмитрий Новиков
- GitHub Actions pipline: Дмитрий Новиков
- Фронтэнд: Яндекс Практикум