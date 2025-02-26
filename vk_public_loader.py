import requests
import fetch_xkcd
import os
from dotenv import load_dotenv

API_VERSION = '5.101'


class VkError(Exception):
    pass


class PhotoIsEmpty(Exception):
    pass


def load_image_to_url(image_name, upload_url):
    with open(f'{image_name}', 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        check_for_vk_error(response)
        return response.json()


def check_for_vk_error(response):
    try:
        if 'error' in response.json():
            raise VkError
    except VkError:
        print(f"При выполнении произошла следующая ошибка: {response.json()['error']['error_msg']}")
        exit(-1)


def check_for_vk_error_and_delete_image(response, image_name):
    try:
        if 'error' in response.json():
            raise VkError
    except VkError:
        print(f"При выполнении произошла следующая ошибка: {response.json()['error']['error_msg']}")
        os.remove(image_name)
        exit(-1)


def check_for_photo_is_empty(image_params, image_name):
    try:
        if 'error' in image_params:
            raise VkError
        if len(image_params['photo']) == 2:
            raise PhotoIsEmpty
    except PhotoIsEmpty:
        print('Не удалось загрузить изображение на сервер')
        os.remove(image_name)
        exit(-1)


def get_response_for_get_wall_upload_server(group_id, access_vk_token):
    url_get_wall_upload_server = 'https://api.vk.com/method/photos.getWallUploadServer'
    params_get_wall_upload_server = {
        'group_id': group_id,
        'access_token': access_vk_token,
        'v': API_VERSION
    }
    response = requests.get(url_get_wall_upload_server, params=params_get_wall_upload_server)
    return response


def get_response_for_save_wall_photo(group_id, access_vk_token, image_params):
    url_save_wall_photo = 'https://api.vk.com/method/photos.saveWallPhoto'
    params_save_wall_photo = {
        'server': image_params['server'],
        'photo': image_params['photo'],
        'hash': image_params['hash'],
        'group_id': group_id,
        'access_token': access_vk_token,
        'v': API_VERSION
    }
    response = requests.post(url_save_wall_photo, params=params_save_wall_photo)
    return response


def get_response_for_wall_post(group_id, access_vk_token, image_title, loaded_image):
    url_wall_post = 'https://api.vk.com/method/wall.post'
    params_wall_post = {
        'owner_id': -group_id,
        'from_group': 1,
        'message': image_title,
        'attachments': f'photo{loaded_image["response"][0]["owner_id"]}_{loaded_image["response"][0]["id"]}',
        'access_token': access_vk_token,
        'v': API_VERSION
    }
    response = requests.get(url_wall_post, params=params_wall_post)
    return response


def get_response_wall_create_comment(group_id, access_vk_token, post_id, image_comment):
    url_wall_create_comment = 'https://api.vk.com/method/wall.createComment'
    params_wall_create_comment = {
        'owner_id': -group_id,
        'post_id': post_id,
        'from_group': group_id,
        'message': image_comment,
        'access_token': access_vk_token,
        'v': API_VERSION
    }
    response = requests.get(url_wall_create_comment, params=params_wall_create_comment)
    return response


def main():
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    access_vk_token = os.getenv('ACCESS_VK_TOKEN')
    group_id = int(os.getenv('GROUP_ID'))
    response = get_response_for_get_wall_upload_server(group_id, access_vk_token)
    check_for_vk_error(response)
    upload_url = response.json()['response']['upload_url']
    image_name, image_title, image_comment = fetch_xkcd.fetch_xkcd_random_comic_with_title_and_comment()
    image_params = load_image_to_url(image_name, upload_url)
    check_for_photo_is_empty(image_params, image_name)
    response = get_response_for_save_wall_photo(group_id, access_vk_token, image_params)
    check_for_vk_error_and_delete_image(response, image_name)
    loaded_image = response.json()
    response = get_response_for_wall_post(group_id, access_vk_token, image_title, loaded_image)
    check_for_vk_error_and_delete_image(response, image_name)
    post_id = response.json()['response']['post_id']
    response = get_response_wall_create_comment(group_id, access_vk_token, post_id, image_comment)
    check_for_vk_error_and_delete_image(response, image_name)
    os.remove(image_name)


if __name__ == '__main__':
    main()
