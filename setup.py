"""The setup script for installing the package."""
from setuptools import setup, find_packages


# read the contents of the README
with open('README.md') as README_md:
    README = README_md.read()


setup(
    name='gym_zelda_1',
    version='0.2.2',
    description='The Legend of Zelda for OpenAI Gym',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords=' '.join([
        'OpenAI-Gym',
        'NES',
        'The-Legend-Of-Zelda',
        'Zelda-1',
        'Reinforcement-Learning-Environment',
    ]),
    classifiers=[
        'License :: Free For Educational Use',
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.13',
        'Topic :: Games/Entertainment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    url='https://github.com/Kautenja/gym-zelda-1',
    author='Christian Kauten',
    author_email='kautencreations@gmail.com',
    license='Proprietary',
    python_requires='>=3.13',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    package_data={ 'gym_zelda_1': ['_roms/*.nes'] },
    install_requires=[
        'gym>=0.25.2,<0.26',
        'nes-py>=8.2.1',
    ],
    extras_require={
        'release': [
            'twine>=6.1.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'gym_zelda_1 = gym_zelda_1._app.cli:main',
        ],
    },
)
