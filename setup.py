from setuptools import setup

setup(name='img',
    version='1.0',
    description='OpenShift App',
    author='S V',
    author_email='example@example.com',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=['Django>=1.5',
                      'MySQL-python',
                      'django-redis'],
     )
