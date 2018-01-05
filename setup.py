try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    longdesc = open('README.md').read()
except:
    longdesc = ''

setup(
    name='telebot',
    version='1.0.0',
    description='Python Telegram Bot.',
    long_description=longdesc,
    author='Kien Nguyen',
    author_email='kiennt2609@gmail.com',
    license='Apache-2.0',
    scripts=['bin/telebot'],
    url='https://github.com/ntk148v/telebot/',
    packages=['telebot', 'telebot.plugins'],
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache-2.0 License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
