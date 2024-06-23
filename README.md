## DRF-project
DRF-проект для управления информацией о жильцах дома.

### Описание
Цель проекта — разработка Desktop-приложения для удобного просмотра и управления информацией о жильцах жилого дома. Приложение предоставляет возможность просмотра адреса дома, списка жильцов в алфавитном порядке и их основных данных. Пользователи могут добавлять новых жильцов, редактировать существующих, а также удалять записи.

### Установка
1. Создать и активировать виртуальное окружение 
```bash
python -m venv venv
source venv/bin/activate
```
2. Установить зависимости
```bash
pip install -r requirements.txt
```
3. Перейти в каталог
```bash
cd info
```
4. Создать и применить миграции
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Создать администратора для использования админ сайта
```bash
python manage.py createsuperuser
```
6. Запуск сервера
```bash
python manage.py runserver
```
7.  http://127.0.0.1:8000/admin/ - административная панель приложения

**Доступные эндпоинты:**
- GET http://127.0.0.1:8000/api/house/ - просмотр домов с отображением информации - город, улица, дом


- GET http://127.0.0.1:8000/api/house/<int:pk>/ - отображение подробной информации о выбранном доме, включая список всех жильцов  


- POST http://127.0.0.1:8000/api/house/<int:house_id>/residents/new/ - создание нового жильца   

*Обязательные параметры:*  
**full_name** ФИО, **passport_data** паспортные данные  
**ownerships** список, содержащий информацию о квартире(ах): **apartment** id-квартиры, **percentage_ownership** процент собственности

 *Необязательные параметры:*  
**cars** список, содержащий информацию о машине(ах): **state_number** гос.номер, **brand** марка  
**reserved_parking_spaces** список, содержащий информацию о парковке(ах): **location** место

*Пример запроса:* 
````json
{
    "full_name": "Говоров Александр",
    "passport_data": "1221 343434",
    "ownerships": [
        {
            "apartment": 8,
            "percentage_ownership": 100.00
        }
    ],
    "cars": [{
            "state_number": "007",
            "brand": "Audi"
        }],
    "reserved_parking_spaces": [{
            "location": "B28"
        }]
}
````
- GET http://127.0.0.1:8000/api/house/<int:house_id>/residents/<int:pk>/ - просмотр данных о жильце


- PUT http://127.0.0.1:8000/api/house/<int:house_id>/residents/<int:pk>/ - обновление информации о жильце  
*Пример запроса для обновления существующих данных:*  
Обновлению подлежат - full_name, passport_data, percentage_ownership, state_number, brand, location
````json
{
    "full_name": "Петров Сергей Вадимович",
    "passport_data": "5949 111111",
    "ownerships": [
        {
            "id": 1,
            "apartment": {
                "id": 1,
                "number": "121",
                "residents_count": 2
            },
            "percentage_ownership": "100.00"
        }
    ],
    "cars": [
        {
            "id": 2,
            "state_number": "500",
            "brand": "Toyota"
        }
    ],
    "reserved_parking_spaces": [
        {
            "id": 1,
            "location": "B28"
        }
    ]
}
````  
*Пример запроса для добавления данных:*  
Обязательные поля:
Добавление квартиры  -  id квартиры, percentage_ownership  
Добавление авто - state_number, brand  
Добавления парковки - location
````json
{
    "full_name": "Петров Сергей Вадимович",
    "passport_data": "5949 111111",
    "ownerships": [
        {
            "apartment": {
                "id": 1
            },
            "percentage_ownership": "100.00"
        }
    ],
    "cars": [
        {
            "state_number": "500",
            "brand": "Toyota"
        }
    ],
    "reserved_parking_spaces": [
        {
            "location": "B28"
        }
    ]
}
````  

- DELETE  http://127.0.0.1:8000/api/house/<int:house_id>/residents/<int:pk>/- удаление жильца




