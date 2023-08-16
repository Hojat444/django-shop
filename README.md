# django-shop

# insatll RabbitMQ
1 - docker pull rabbitmq:3-management
2 - create container: docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
3 - start: docker start rabbitmq
4 - stop: docker stop rabbitmq
5 - after runserver and run rabbitmq, we should run celery: celery -A myshop worker -l INFO --pool=solo
6- monetoring with flower : celery -A myshop flower  
