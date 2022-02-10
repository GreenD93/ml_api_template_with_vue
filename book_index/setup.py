from setuptools import setup, find_packages

__version__ = '0.0.1'

setup(
    name='',
    description='',
    version=__version__,
    install_requires=[
        'pymysql',
        'PyAthena',
        'pandas',
        'pyyaml'
        'sklearn',
        'lightgbm',
        'bayesian-optimization',
        'gensim'
    ],
    url='https://git.wjtb.kr/ai_model/dev_bookclub_index.git',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)