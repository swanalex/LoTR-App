import os
from dotenv import load_dotenv


def get_pic(character):

    load_dotenv()
    # replace with your own image folder location
    IMAGE_FOLDER = os.path.join('static', 'images')
    

    for image in os.listdir(IMAGE_FOLDER):
        if image == character + '.jpg':
            return f'./images/{character}.jpg'
    return False
