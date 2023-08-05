from setuptools import setup, find_packages

setup(
    name='help_bot',
    version='0.1.0',
    description='The simple tool to manage contacts and notes',
    author='f"{group4_name}"',
        author_email=[
        'nataliia.manushyna@gmail.com',
        'tovkun.andrii@gmail.com',
        'mr.sanscrit@gmail.com',
        'rolmf85@gmail.com'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'help_bot = help_bot.help_bot:main',
        ],
    },
)