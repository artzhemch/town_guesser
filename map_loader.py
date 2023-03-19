import sys

import requests
from urllib3 import Retry
from requests.adapters import HTTPAdapter

def load_next_slide(counter):
    # Запрашиваем изображение.
    request = map_requests[counter % len(map_requests)]
    response = requests.get(request)
    if not response:
        print("Ошибка выполнения запроса:", file=sys.stderr)
        print(request, file=sys.stderr)
        print("Http статус:", response.status_code, "(", response.reason, ")", file=sys.stderr)
        raise MyError()

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        raise MyError()


def refresh_map(map_coords: list[float, float], map_size: list[float, float]):
    map_params = {
        "ll": f'{map_coords[0]},{map_coords[1]}',
        "l": 'sat',
        "spn": ','.join([str(x) for x in map_size])
    }
    session = requests.Session()
    retry = Retry(total=3, connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get('https://static-maps.yandex.ru/1.x/',
                           params=map_params)
    print(response)
    with open('tmp.png', mode='wb') as tmp:
        tmp.write(response.content)
    return True


if __name__ == '__main__':
    refresh_map([15, 13], [3, 3])