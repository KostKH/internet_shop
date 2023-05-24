# internet_shop

internet_shop - это проект сайта интернет-магазина.

Посетители сайта могут добавить понравившиеся товары в корзину, оформить заказ и произвести оплату. После оформления заказа, а также после оплаты посетителю сайта отправляется e-mail с pdf-файлом, в котором указаны детали заказа (с использованием Celery и RabbitMQ). В интернет-магазине предусмотрена возможность ввода купонов для получения скидки на товары. Также, при посмотре карточки товара посетителю выводятся рекомендации по покупке других товаров (отображаются товары, которые чаще всего покупаются с просматриваемым товаром). Система рекомендаций сделана с использованием Redis. 

## Системные требования
- Python 3.11+
- Works on Linux, Windows

## Технологии:
- Python 3.11
- Django 4
- Celery
- RabbitMQ
- Redis
- Stripe API

## Как запустить проект:

Для запуска проекта на локальной машине в режиме Debug с целью доработки проекта под свои нужды необходимо выполнить следующие шаги:

- Проверьте, что свободны порты, необходимые для работы приложения: порт 8000 (требуется для работы приложения), порты 5672 и 15672 (требуется для работы RabbitMQ), порт 6379 (необходим для работы Redis)

- Проверьте, что на машине установлены docker и docker-compose 

- Скачайте docker-образ RabbitMQ и запустите RabbitMQ в контейнере:
```
docker pull rabbitmq
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
```

- Скачайте docker-образ Redis и запустите Redis в контейнере:
```
docker pull redis
docker run -it --rm --name redis -p 6379:6379 redis
```
- Клонируйте репозиторий данного приложения и перейдите в папку проекта, где расположен файл manage.py:
```
git clone https://github.com/KostKH/internet_shop.git
cd internet_shop/myshop/
```
- Сгенерируйте свой секретный ключ для Django:
```
python manage.py shell
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
exit()
```
- Перейдите в папку internet_shop. Cоздайте в ней файл .env с переменными окружения и занесите в файл сгенеринованный секретный ключ:
```
cd ..
touch .env
echo DJANGO_SECRET_KEY='сгенерированный вами секретный ключ' >>.env
```
- Создайте аккаунт на сайте www.stripe.com, чтобы настроить тестовую оплату:
```
https://dashboard.stripe.com/register
```
- Найдите публичный и секретный ключи API Stripe для тестовой среды (они должны быть на странице https://dashboard.stripe.com/test/apikeys). Внесите ключи, а также версию API в env-файл. Пример:
```
echo STRIPE_PUBLISHABLE_KEY='pk_test_.......' >>.env
echo STRIPE_SECRET_KEY='sk_test_.......' >>.env
echo STRIPE_API_VERSION='2022-11-15' >>.env
```
- Найдите ключ, необходимый для настройки webhooks. Для этого откройте в браузере страницу https://dashboard.stripe.com/test/webhooks, найдите на открывшейся странице ссылку Test in local environment, в примерах кода найдите строку endpoint secret. Занесите найденный ключ в env-файл:
```
echo STRIPE_WEBHOOK_SECRET='whsec_.......' >>.env
```
- Для тестирования вебхуков установите на локальную машину Stripe CLI. Скачать клиент можно, перейдя по ссылке: https://github.com/stripe/stripe-cli/releases/latest. После установки клиента нужно залогиниться в нём, а после этого запустить клиент:
```
stripe login
stripe listen --forward-to localhost:8000/payment/webhook/
```
- Перейдите в папку internet_shop, установите все необходимые зависимости:
```
pip install -r requirements.txt
```
- Перейдите в папку internet_shop/myshop, запустите миграции, создайте суперюзера, соберите статику:
```
cd myshop
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input
```
- Находясь в папке internet_shop/myshop, запустите Celery:
```
celery -A myshop worker -l INFO

# Если у вас Windows, тогда введите такую команду:
celery -A myshop worker -l INFO --pool solo
```
- После того, как вы запустили RabbitMQ и Redis, запустили клиента Stripe, запустили Celery, сделали миграции, создали суперюзера, собрали статику - находясь в папке internet_shop/myshop, запустите приложение:
```
python manage.py runserver
```

## О программе:
Код данного приложения был подготовлен в процессе изучения книги "Django 4 by Example, Antonio Mele" и с использованием примеров из неё.