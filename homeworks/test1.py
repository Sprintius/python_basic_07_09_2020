import os
import requests


def get_html():
    url ='https://geekbrains.ru'
    response = requests.get(url)
    return response.text


def get_image(url):
    response = requests.get(url)
    return response.content


def save_html_to_file(file_path, html_text):
    with open(file_path, 'w', encoding='UTF-8') as file:
        file.write(html_text)

def save_image(file_path, image_bytes):
    with open(file_path, 'wb') as file:
        file.write(image_bytes)

if __name__ == '__main__':
    img_url = 'https://d2xzmw6cctk25h.cloudfront.net/recommendations/41/image/base_1x-f312e705b26d4daa83d1c5027b0bb325.png'
    file_name = 'temp_gb_mail.html'
    file_folder = os.path.dirname(__file__)
    file_path = os.path.join(file_folder, file_name)
    image_path = os.path.join(file_folder, 'base_1x-f312e705b26d4daa83d1c5027b0bb325.png')
    # html_text = get_html()
    # save_html_to_file(file_path, html_text)
    img_bytes = get_image(img_url)
    save_image(image_path, img_bytes)