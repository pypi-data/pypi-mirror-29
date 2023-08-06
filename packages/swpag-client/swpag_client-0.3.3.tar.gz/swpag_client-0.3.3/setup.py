from distutils.core import setup

setup(
    name='swpag_client',
    version='0.3.3',
    description='This is a python module that provides an interface to the SWPAG team API.',
    packages=['swpag_client'],
    install_requires=[
        'requests',
        'future',
        'pyOpenSSL>=17.5.0',
        'urllib3>=1.22',
        'six>=1.11.0',
    ],
)
