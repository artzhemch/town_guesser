import requests
from functools import lru_cache
# API_KEY = '0387b561-9bdb-4062-866e-2fd58446914e'
API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"


@lru_cache(100)
def geocode(address: str):
    """Нахождение объекта по названию. Результаты кешируются"""
    # Собираем запрос для геокодера.
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}" \
                       f"&geocode={address}&format=json"

    # Выполняем запрос.
    response = requests.get(geocoder_request)

    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
                request=geocoder_request, status=response.status_code, reason=response.reason))

    # Получаем первый топоним из ответа геокодера.
    # Согласно описанию ответа он находится по следующему пути:
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


def get_coordinates(address: str):
    """Получаем координаты объекта по его адресу"""
    toponym = geocode(address)
    if not toponym:
        return None, None

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Широта, преобразованная во float:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return float(toponym_longitude), float(toponym_lattitude)


def get_adress_info(address: str):
    """Получаем информацию об объекте по его адресу"""
    toponym = geocode(address)
    if not toponym:
        return None, None
    return toponym['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['CountryName']
    # return toponym['description']