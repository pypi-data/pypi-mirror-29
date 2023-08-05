from setuptools import setup
setup(
    name='masonite',
    packages=['masonite',
              'masonite.auth',
              'masonite.facades',
              'masonite.providers',
              'masonite.drivers',
              'masonite.managers',
              'masonite.testsuite',
              'masonite.queues',
             ],
    version='1.3.0',
    install_requires=[
        'validator.py==1.2.5',
        'cryptography==2.1.4',
        'bcrypt==3.1.4',
        'requests==2.18.4',
        'boto3==1.5.24',
        'tldextract==2.2.0',
    ],
    description='The core for the Masonite ',
    author='Joseph Mancuso',
    author_email='idmann509@gmail.com',
    url='https://github.com/josephmancuso/masonite',  # use the URL to the github repo
    download_url='',
    keywords=['python web framework', 'python3'],  # arbitrary keywords
    classifiers=[],
)
