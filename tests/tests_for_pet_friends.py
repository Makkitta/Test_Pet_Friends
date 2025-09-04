import json

from api import PetFriends
from settings import *
import os

pf = PetFriends()

#1
def test_get_api_key_with_invalid_email():
    """проверяем, что запрос ключа с неверным email возвращает статус код 403"""
    status, result = pf.get_api_key("invalid_email@test.com", valid_email)
    assert status == 403
    assert 'key' not in result

#2
def test_get_api_key_with_invalid_password():
    """проверяем, что запрос ключа с неверным password возвращает статус код 403"""
    status, result = pf.get_api_key(valid_email, "invalid_password")
    assert status == 403
    assert 'key' not in result

#3
def test_get_all_pets_with_invalid_key():
    """проверяем, что запрос списка питомцев с неверным ключом возвращает статус код 403"""
    invalid_auth_key = {'key' : 'invalid_key_123456789'}
    status, result = pf.get_list_pets(invalid_auth_key, '')
    assert status == 403

#4
def test_add_new_pet_without_photo_valid_data(name ='Кашин' , animal_type ='кот', age = 10):
    """проверяем, что можно добавить питомца без фотографии с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == "Мурзик"
    assert result['animal_type'] == "кот"
    assert result['age'] == "10"

#5
def test_add_photo_to_existing_pet():
    """"проверяем, что можно добавить фотографию к существующему питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, pet_result = pf.add_new_pet_without_photo(auth_key, "Джарахов", "собака", 3)
    assert status == 200

    pet_photo = os.path.join(os.path.dirname(__file__), 'images/pesiki.jpg')
    status, result = pf.add_photo_of_pet(auth_key, pet_result['id'], pet_photo)
    assert status == 200
    assert 'pet_photo' in result

#6
def test_add_pet_without_name():
    """проверяем, что можно оставить поле с именем пустым при создании питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, "", "собака", 3)
    assert status == 200

#7
def test_add_pet_with_special_characters():
    """проверяем питомца со специальными символами в имени"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, "Тест!@#$%", "собака", 5)
    assert status == 200
    assert result['name'] == "Тест!@#$%"

#8
def test_delete_nonexistent_pet():
    """проверяем попытку удаления несуществующего питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.delete_pet(auth_key, "nonexistent_pet_id_12345")
    assert status == 404

#9
def test_get_my_pets_filter():
    """проверяем работу фильтра "my_pets"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_pets(auth_key, "my_pets")
    assert status == 200

    if len(result['pets']) > 0:
        for pet in result['pets']:
            assert 'id' in pet
            assert 'name' in pet
            assert 'animal_type' in pet
            assert 'age' in pet

#10
def test_add_pet_with_max_age_value():
    """проверяем создание питомца с максимально допустимым значением возраста"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    max_age = 100
    status, result = pf.add_new_pet_without_photo(auth_key, "Шерсть", "собака", max_age)
    assert status == 200
    assert result['name'] == "Шерсть"
    assert result['animal_type'] == "собака"
    assert int(result['age']) == max_age