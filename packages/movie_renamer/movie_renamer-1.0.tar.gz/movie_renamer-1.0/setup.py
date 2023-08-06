from setuptools import setup


setup(
    name='movie_renamer',
    version='1.0',
    py_modules=['movie'],
    install_requires=[
        'Click',
        'tmdbsimple',
    ],
    entry_points='''
        [console_scripts]
        movie=movie:cli

   '''

)
