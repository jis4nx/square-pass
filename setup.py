from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = open('README.md').read()


setup(
    name='square-pass3',
    version='0.0.2',
    description='A sample Python project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jis4nx/square-pass',
    author='Rakibul Islam Jisan',
    author_email='jis4nx@gmail.com',


    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='password_manager, encryption, aes256, cli-password-manager',
    packages=find_packages(),
    python_requires='>=3.6, <3.12',
    install_requires=[
        "pycryptodome==3.10.1",
        "prettytable==2.4.0",
        "colorama==0.4.4",
        "rich==10.15.2",
        "pyperclip",
        "psutil",
        "setuptools",
        "wheel",
        "PyYAML"
    ],

    entry_points={
        'console_scripts': [
            'sq-init=sqpass.install:setmain',
            'sq=sqpass.main:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/jis4nx/square-pass/issues',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/jis4nx/square-pass/',
    },
)
