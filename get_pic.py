import os


def get_pic(character):
    image_folder = 'C:/Users/16316/Desktop/OSU/CS 361/Simple_Flask_App/static/images'
    for image in os.listdir(image_folder):
        if image == character + '.jpg':
            return f'./images/{character}.jpg'
    return False
