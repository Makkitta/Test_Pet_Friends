from api import PetFriends
from settings import *
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """проверяем что запрос ключа возвращает статус код 200 и в результате содержится слово key."""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """проверяем что запрос списка питомцем возвращает не пустой список и статус код 200."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age= 4, pet_photo='images/pesiki.jpg'):
    """проверяем что можно добавить питомца с корректными данными и фотографией."""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """проверяем возможность удаления питомца из списка всех питомцев пользователя."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "мурзик", "кот", 10, "images/pesiki.jpg")
        _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()





