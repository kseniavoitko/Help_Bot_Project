from setuptools import setup, find_packages

with open("requirements.txt", "r") as req_file:
    requirements = req_file.read().splitlines()

with open("readme.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

with open("LICENSE", "r", encoding="utf-8") as license_file:
    license_text = license_file.read()

setup(
    name='help_bot',
    version='0.1.0',
    description='A simple tool to manage yours contacts and notes. Also you can sort your directories',
    author='f"{group4_name}',
    author_email=['kseniavoytko95@gmail.com', 'nataliia.manushyna@gmail.com', 'tovkun.andrii@gmail.com', 'mr.sanscrit@gmail.com', 'rolmf85@gmail.com'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'help_bot = help_bot.switcher:main',
        ],
    },
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=license_text,
)