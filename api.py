import os
import requests
import json

class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключом пользователя, найденного по указанным email и паролем"""

        headers = {
            'email': email,
            'password': password,
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: int, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        res = requests.post(self.base_url+'api/pets', headers=headers, data=data, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет на сервер(постит) данные о добавляемом питомце без фотографии и возвращает
         статус запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.post(self.base_url+'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет на сервер данные о питомце и назначаемой фотографии и возвращает статус
        запроса на сервер и результат в формате JSON с данными о питомце"""

        headers = {'auth_key': auth_key['key']}
        photo_path = os.path.join(os.path.dirname(__file__), pet_photo)
        with open(photo_path, 'rb') as photo_file:
            files = {'pet_photo': (os.path.basename(photo_path), photo_file, 'image/jpeg')}
            res = requests.post(self.base_url+'api/pets/set_photo/' + pet_id, headers=headers, files=files)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца на указанный ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления об успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url+'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    def update_information_about_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер об обновлении данных питомца по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлёнными данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.put(self.base_url+'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result
