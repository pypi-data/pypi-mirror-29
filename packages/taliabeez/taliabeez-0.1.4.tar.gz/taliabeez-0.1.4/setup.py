from setuptools import setup

setup(
    name='taliabeez',
    version='0.1.4',
    packages=['taliabeez'],
    description='TaliaBee ZigBee interface',
    url = 'https://github.com/beyaznet/python-taliabeez-module',
    author = 'Beyaz R&D Team',
    author_email = 'arge@beyaz.net',
    license='MIT',
    keywords = 'raspberry pi medioex taliabee zigbee xbee',
    install_requires=['taliabeeio', 'xbee', 'pyserial'],
    python_requires='>=3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
