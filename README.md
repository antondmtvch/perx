# perx test
## запуск
```
$ docker build --no-cache -t perx .
$ docker run -d -p 8080:8080 --name=perx perx
```
## Доступные методы

#### Поставить задачу в очередь

*Пример запроса*
 ```
curl --location --request POST 'http://<HOST>:<PORT>/put' \
--header 'Content-Type: application/json' \
--data-raw '{
    "count":100,
    "delta":0.15,
    "start":10,
    "interval":0.1
}'
```
*Пример ответа*
```
{
    "status": 200,
    "message": "OK"
}
```
*Описание параметров запроса*
- `count` - количество элементов целочисленное (int)
- `delta` - дельта между элементами последовательности (float)
- `start` - Стартовое значение (int)
- `interval` - интервал в секундах между итерациями (float)

#### Получить список задач и статусы выполнения этих задач

*Пример запроса*
 ```
curl --location --request GET 'http://<HOST>:<PORT>/get'
```

*Пример ответа*
```
{
    "tasks": [
        {
            "count": 100,
            "delta": 0.15,
            "start": 10,
            "interval": 0.1,
            "id": 9,
            "current_value": 17.050000000000004,
            "started_at": "2020-11-26T14:05:19.708359",
            "status": 2
        },
        {
            "count": 100,
            "delta": 0.15,
            "start": 10,
            "interval": 0.1,
            "id": 10,
            "current_value": 14.950000000000012,
            "started_at": "2020-11-26T14:05:21.056058",
            "status": 2
        },
        {
            "count": 100,
            "delta": 0.15,
            "start": 10,
            "interval": 0.1,
            "id": 11,
            "current_value": 14.50000000000001,
            "started_at": "2020-11-26T14:05:21.428884",
            "status": 2
        }
    ]
}
```