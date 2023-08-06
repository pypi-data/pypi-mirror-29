from setuptools import setup

__version__ = '1.0.0'

setup(
    name='facturacom',
    packages=['facturacom'], # this must be the same as the name above
    version=__version__,
    description='Integracion de factura.com',
    author='Ricardo Tapia',
    author_email='rtapia92@gmail.com',
    url='https://github.com/richipargo/facturacom',
    download_url='https://github.com/richipargo/facturacom/archive/1.0.0.tar.gz',
    keywords=['testing', 'logging', 'example'], # arbitrary keywords
    classifiers=[],
    install_requires=[
        'requests',
    ]
)
