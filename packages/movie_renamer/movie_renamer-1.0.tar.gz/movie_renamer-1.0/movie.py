import os
import shutil
import click
import shelve
import tmdbsimple as tmdb
from pathlib import Path
from string import digits
from operator import itemgetter
from subprocess import call


tmdb.API_KEY = os.environ['TMDB_API_KEY']
search = tmdb.Search()

map_genres = {'Science Fiction': 'Sci-Fi'}


def call_tag(path, tags):
    # the `path` argument is a `pathlib.Path`
    # the `tags` argument is a `list`
    call(f"tag -a {','.join(tags)} \"{path}\"", shell=True)


def make_title(movie, format_):
    # TODO
    year = get_year(movie['release_date'])
    original_title = movie['original_title']
    title = movie['title']
    output = f"{year} - {original_title}"
    if title != original_title:
        output += " " + f"({title})"
    return output


def input_index():
    return int(input('Your choice: ')) - 1


def is_director(person):
    return person['job'] == 'Director'


def print_ask(iterable):
    for i, x in enumerate(iterable, 1):
        print(f"{i}. {x}")


def movie_line(movie):
    year = get_year(movie['release_date'])
    string = f"{year} - {movie['original_title']}"
    if movie['title'] != movie['original_title']:
        string += " " + f"({movie['title']})"
    return string


def extract(string, formt):
    # TODO
    return None, string # (year, title)


def get_year(date_str):
    return date_str.split('-')[0]


def get_name(directors):
    if len(directors) > 1:
        print_ask(directors)
        name = formated_name(directors[input_index()])
    else:
        name = formated_name(directors[0])
    return name


def formated_name(name):
    frst_name = name.rsplit(' ')[0]
    scnd_name = name.rsplit(' ')[1]
    return f"{scnd_name}, {frst_name}"     


@click.command()
@click.option('--rename','-r', is_flag=True)
@click.option('--add-tags', '-t', is_flag=True)
@click.option('--formt', '-f', help='(TODO)') # '%y - %t', '%t (%y)'
@click.option('--output-format', '-o', help='(TODO)')
@click.option('--to-director-folder', '-d', is_flag=True)
@click.argument('path', type=click.Path(exists=True))
def cli(path, rename, add_tags, formt, output_format, to_director_folder):
    path = Path(path)
    oldname = path.stem
    parent = path.parent
    suffix = path.suffix
    # Год - int, title - str. Это нормальное 
    # название, а не что-то вроде phant0m_ThEat
    year, title = extract(oldname, formt)
    # search.movie() вернет dict с ключами: 'page', 
    # 'total_results', 'total_pages', 'results'
    results = search.movie(query=title, year=year)['results']
    # Попросить выбрать фильм. Так как 
    # results – это list of dicts в котором 
    # нужны несколько значений ключей (год, 
    # оригинальное название и обычное 
    # название), то используем movie_line() 
    # для каждого dict
    print_ask(map(movie_line, results))
    # movie_dict не содержит все необходимые 
    # ключи. Поэтому создаем экземпляр Movies 
    # данного фильма.
    movie_dict = results[input_index()]
    movie_obj = tmdb.Movies(movie_dict['id'])

    # ----------------
    if rename:
        new_name = make_title(movie_dict, output_format)
        target = parent.joinpath(new_name).with_suffix(suffix)
        path.rename(target)
        path = target

    if to_director_folder:
        # movie_obj.credits() вернет dict с ключами
        # 'id', 'cast', 'crew'.
        crew = movie_obj.credits()['crew']
        # Получить только имя режиссера
        directors = list(map(itemgetter('name'), filter(is_director, crew)))
        # Если имен несколько, то нужно выбрать одно
        if len(directors) > 1:
            print_ask(directors)
            director_name = formated_name(directors[input_index()])
        else:
            director_name = formated_name(directors[0])
        # 
        director_folder = parent.joinpath(director_name)
        if not director_folder.exists():
            director_folder.mkdir(parents=True)
        # (There is a bug in Python 3.6.2. 
        # It complains  that 'PosixPath' 
        # object has no attribute 'rstrip')
        path = Path(shutil.move(str(path), str(director_folder)))

    if add_tags:
        genres = list(map(itemgetter('name'), movie_obj.info()['genres']))
        for genre in genres:
            if genre in map_genres:
                del genres[genres.index(genre)]
                genres.append(map_genres[genre])
        call_tag(path, genres)
        call_tag(path, ['Movie'])


