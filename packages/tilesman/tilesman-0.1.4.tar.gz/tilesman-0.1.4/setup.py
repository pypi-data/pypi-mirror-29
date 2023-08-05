from setuptools import setup

setup(
    name = 'tilesman',
    author = 'Fernando Urzedo',
    author_email = 'furzedo@yahoo.com',
    version = '0.1.4',
    packages = ['tilesman', 'tilesman.tests', 'tilesman.tests.helpers'],
    url = 'https://github.com/furzedo/tilesman',
    license = 'LICENSE.txt',
    description = 'A library to tile photos at different resolution levels, for loading performance',
    long_description = open('README.txt').read(),
    python_requires = '>=3',
    install_requires = [
        "Pillow>=5.0.0",
    ],
    entry_points = {
        'console_scripts': [
            'tilesman = tilesman.core:main',
        ]
    }
)
