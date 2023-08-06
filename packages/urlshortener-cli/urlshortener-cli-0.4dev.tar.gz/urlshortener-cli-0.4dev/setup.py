from distutils.core import setup

setup(
    name='urlshortener-cli',
    version='0.4dev',
    long_description='A command-line tool for shortening long URLs',
    author="Karan Suthar",
    author_email="karansthr97@gmail.com",
    license="MIT License",
    url="https://github.com/karansthr/Url-Shortener",
    packages=['shortener'],
    entry_points={
        'console_scripts': ['shrt=shortener:main'],
    },
    install_requires=[
        "requests==2.18.4",
        "pyperclip==1.6.0",
    ],
    keywords="url shortener",
)
