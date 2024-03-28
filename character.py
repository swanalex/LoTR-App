def transform_character(character):
    name = character['name']
    race = character['race']
    gender = character['gender']
    birth = character['birth']
    death = character['death']

    stats = [name, race, gender, birth, death]
    for i in range(len(stats)):
        if stats[i] == 'NaN' or stats[i] == '':
            stats[i] = 'Unknown'

    return f'Name: {stats[0]}, Race: {stats[1]}, Gender: {stats[2]}, Birth: {stats[3]}, Death: {stats[4]}'


def transform_quote(quote, movies_dict, chars_dict):
    dialogue = quote['dialog']
    movie = quote['movie']
    for name, id in movies_dict.items():
        if movie == id:
            movie = name
    char = quote['character']
    for name, id in chars_dict.items():
        if char == id:
            char = name
    return f'Quote: "{dialogue}", Movie: {movie}, Character: {char}', char
