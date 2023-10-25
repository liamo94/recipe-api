# recipe-api

### Getting started

Python is run inside a docker container. To get started, run:

```
docker-compose build
docker-compose start
```

### Testing

```
docker-compose run --rm app sh -c "python manage.py test"
```
