

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = open('README.md').read()


setup(

    name='square-pass',  # Required
    version='0.0.1',  # Required
    description='A sample Python project',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown', 
    url='https://github.com/jis4nx/square',  # Optional
    author='Rakibul Islam Jisan',  # Optional
    author_email='jis4nx@gmail.com',  # Optional

    classifiers =[

        'Development Status :: 5 - Stable',
        'Intended Audience :: Developers',
        'Topic :: Build Tools :: Reseach',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='sequence, generator, fibonacci',
    packages=['passwordManager'],
    python_requires ='>=3.6, <4',

    entry_points={  # Optional
        'console_scripts': [
            'ggshoaib=passwordManager.main:main',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/jis4nx/square/issues',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/jis4nx/square/',
    },
)
