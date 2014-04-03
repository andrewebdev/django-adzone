from setuptools import setup, find_packages

setup(
    name="django-adzone",
    version="0.2",
    url="http://github.com/winterweaver/django-adzone",
    description="A django app to manage adverts according to zones on a website.",
    author="Andre Engelbrecht",
    packages=find_packages(),
    install_requires=[
        'django>=1.4',
    ],
    include_package_data=True,
)
