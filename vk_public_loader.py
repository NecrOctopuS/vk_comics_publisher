import requests
import fetch_xkcd
import os
from dotenv import load_dotenv

API_VERSION = '5.101'


def load_image_to_url(image_name, upload_url):
    with open(f'{image_name}', 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        return response.json()


class VkError(Exception):
    pass

class PhotoIsEmpty(Exception):
    pass

def main():
    load_dotenv()
    CLIENT_ID = os.getenv('CLIENT_ID')
    ACCESS_VK_TOKEN = os.getenv('ACCESS_VK_TOKEN')
    GROUP_ID = int(os.getenv('GROUP_ID'))
    url_get_wall_upload_server = 'https://api.vk.com/method/photos.getWallUploadServer'
    params_get_wall_upload_server = {
        'group_id': GROUP_ID,
        'access_token': ACCESS_VK_TOKEN,
        'v': API_VERSION
    }
    response = requests.get(url_get_wall_upload_server, params=params_get_wall_upload_server)
    try:
        if 'error' in response.json():
            raise VkError
        upload_url = response.json()['response']['upload_url']
    except VkError:
        print(f"При выполнении произошла следующая ошибка: {response.json()['error']['error_msg']}")
        exit(-1)
    image_name, image_title, image_comment = fetch_xkcd.fetch_xkcd_random_comic_with_title_and_comment()
    url_save_wall_photo = 'https://api.vk.com/method/photos.saveWallPhoto'
    image_params = load_image_to_url(image_name, upload_url)
    try:
        if 'error' in image_params:
            raise VkError
        if len(image_params['photo']) == 2:
            raise PhotoIsEmpty
        params_save_wall_photo = {
            'server': image_params['server'],
            'photo': image_params['photo'],
            'hash': image_params['hash'],
            'group_id': GROUP_ID,
            'access_token': ACCESS_VK_TOKEN,
            'v': API_VERSION
        }
    except VkError:
        print(f"При выполнении произошла следующая ошибка: {response.json()['error']['error_msg']}")
        os.remove(image_name)
        exit(-1)
    except PhotoIsEmpty:
        print('Не удалось загрузить изображение на сервер')
        os.remove(image_name)
        exit(-1)
    response = requests.post(url_save_wall_photo, params=params_save_wall_photo)
    loaded_image = response.json()
    url_wall_post = 'https://api.vk.com/method/wall.post'
    try:
        if 'error' in loaded_image:
            raise VkError
        params_wall_post = {
            'owner_id': -GROUP_ID,
            'from_group': 1,
            'message': image_title,
            'attachments': f'photo{loaded_image["response"][0]["owner_id"]}_{loaded_image["response"][0]["id"]}',
            'access_token': ACCESS_VK_TOKEN,
            'v': API_VERSION
        }
    except VkError:
        print(f"При выполнении произошла следующая ошибка: {loaded_image['error']['error_msg']}")
        os.remove(image_name)
        exit(-1)
    response = requests.get(url_wall_post, params=params_wall_post)
    try:
        if 'error' in response.json():
            raise VkError
        post_id = response.json()['response']['post_id']
    except VkError:
        print(f"При выполнении произошла следующая ошибка: {response.json()['error']['error_msg']}")
        os.remove(image_name)
        exit(-1)
    url_wall_create_comment = 'https://api.vk.com/method/wall.createComment'
    params_wall_create_comment = {
        'owner_id': -GROUP_ID,
        'post_id': post_id,
        'from_group': GROUP_ID,
        'message': image_comment,
        'access_token': ACCESS_VK_TOKEN,
        'v': API_VERSION
    }
    requests.get(url_wall_create_comment, params=params_wall_create_comment)
    os.remove(image_name)

if __name__ == '__main__':
    main()
