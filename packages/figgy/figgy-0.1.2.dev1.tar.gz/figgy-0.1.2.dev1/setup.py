from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='figgy',
    version='0.1.2.dev1',
    description='Enable end-user Configuration generation for development.',
    long_description=long_description,
    url='https://github.com/dyspop/figgy',
    author='Dan Black',
    author_email='dyspop@gmail.com',
    license='GPL-3.0+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['config', 'configuration generator', 'dev tool', 'json'],
    packages=find_packages(exclude=[]),
    install_requires=[],
    download_url='https://github.com/dyspop/figgy/archive/0.1.2dev1.tar.gz'
)
