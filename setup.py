from setuptools import setup, find_packages

setup(
    name='tranpy',
    version='0.3.1',
    packages=find_packages(),
    install_requires=[
        'deep_translator',
        'requests',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'tranpy=tranpy.translator:main',
        ],
    },
    author='Blackflame44',
    author_email='anonzar1@gmail.com',
    description='A translation tool that translates what other bots can’t!',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/blackflame44/tranpy',
)