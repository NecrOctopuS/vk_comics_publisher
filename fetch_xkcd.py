import requests
import random


def download_image(image_url, image_name):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(image_name, 'wb') as file:
        file.write(response.content)


def get_total_number_of_comics():
    response = requests.get(f'http://xkcd.com/info.0.json')
    response.raise_for_status()
    return response.json()['num']


def fetch_xkcd_random_comic_with_title_and_comment():
    total_number = get_total_number_of_comics()
    comics_number = random.randint(1, total_number)
    response = requests.get(f'http://xkcd.com/{comics_number}/info.0.json')
    response.raise_for_status()
    media = response.json()
    images_link = media["img"]
    images_name = f'xkcd_comics_number_{comics_number}.png'
    download_image(images_link, images_name)
    images_comment = media['alt']
    images_title = media['title']
    return images_name, images_title, images_comment
