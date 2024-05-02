from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from get_pic import get_pic
from character import transform_character, transform_quote
import zmq
import random


app = Flask(__name__)

load_dotenv()

# replace with your personal bearer token
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

# ZeroMQ setup
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:8888")


# def generate_random_numbers():
#     socket.send_string("generate_numbers")
#     response = socket.recv_json()
#     return response["num1"], response["num2"]

def generate_random_numbers():
    num1 = random.randint(1, 932)
    num2 = random.randint(1, 2383)
    return num1, num2


# Initialize chars_dict, movies_dict, and quotes_list
chars_dict = {}
movies_dict = {}
quotes_list = []


def initialize_chars_dict():
    global chars_dict, chars_list
    api_endpoint1 = 'https://the-one-api.dev/v2/character'
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}

    # Compile chars_dict {'Char_name1': '_charID1', etc..}
    response1 = requests.get(api_endpoint1, headers=headers)
    data1 = response1.json()
    chars_list = data1['docs']
    for i in range(933):
        char_obj = data1['docs'][i]
        specific_char = data1['docs'][i]['name']
        chars_dict[specific_char] = char_obj['_id']


def initialize_movies_dict():
    global movies_dict
    api_endpoint_movies = 'https://the-one-api.dev/v2/movie'
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}

    # Compile movies_dict {'Movie_name1': '_movieID1', etc..}
    response2 = requests.get(api_endpoint_movies, headers=headers)
    data2 = response2.json()
    movies_dict = {}
    for i in range(2, 8):
        movie = data2['docs'][i]
        specific_movie = data2['docs'][i]['name']
        movies_dict[specific_movie] = movie['_id']


def initialize_quote_list():
    global quotes_list
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}

    response_page1 = requests.get('https://the-one-api.dev/v2/quote?page=1',
                                   headers=headers)
    response_page2 = requests.get('https://the-one-api.dev/v2/quote?page=2',
                                   headers=headers)
    response_page3 = requests.get('https://the-one-api.dev/v2/quote?page=3',
                                   headers=headers)
    data_page1 = response_page1.json()
    data_page2 = response_page2.json()
    data_page3 = response_page3.json()
    quotes_list = data_page1['docs']
    quotes_list += data_page2['docs']
    quotes_list += data_page3['docs']


# Call the functions to initialize dicts and quote list when app starts
initialize_chars_dict()
initialize_movies_dict()
initialize_quote_list()


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    global chars_dict, movies_dict, quotes_list, chars_list

    if request.method == 'POST':
        show_image = True
        num1, num2 = generate_random_numbers()

        # Getting character info
        # Take care of fields that have 'NaN' or '' to read 'Unknown'
        character = chars_list[num1]
        char_string = transform_character(character)

        # Use the global chars_dict and movies_dict to display movie name
        # and character name for each quote, instead of movie_id and char_id
        quote = quotes_list[num2]
        quote_string, char = transform_quote(quote, movies_dict, chars_dict)

        button_value = request.form['button']
        if button_value == 'get_char':
            return render_template('index.html', text=char_string)
        if button_value == 'get_quote':
            if get_pic(char):
                character = get_pic(char)
                return render_template('index.html', text=quote_string, image=character, show_image=show_image)
            else:
                return render_template('index.html', text=quote_string)
        else:
            return render_template('index.html', text='')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
