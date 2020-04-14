'''
python setup.py build
python setup.py install --user
'''

"""
Poker AI
"""

from setuptools import setup
setup(
    name='PokerAI',
    version='0.1',
    description=__doc__,
    #long_description=open('README.md').read(),
    author='Fredrik Mårtensson, Jesper Holmblad',
    url='https://github.com/FredrikM97/Artificial-Intelligence/tree/master/Labs/PokerProject/PokerClientRandom',
    packages=['game', 'evolution'],
    install_requires = ['deuces @ https://github.com/FredrikM97/deuces']
)