from setuptools import setup, find_packages

setup(
    name='aiogram_toolkit',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
    ],
    description='A compact utility library extending Aiogram with ready-to-use helpers for everyday bot development. It includes safe callback data unpacking, deep link generation, long message handling, markdown formatting, pagination, and async SQLAlchemy session helpers. Designed for clean, modular, and production-grade Telegram bot architecture.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ruhiddin Turdaliyev',
    author_email='niddihur@gmail.com',
    url='https://github.com/ruhiddin/aiogram_toolkit',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',
)


