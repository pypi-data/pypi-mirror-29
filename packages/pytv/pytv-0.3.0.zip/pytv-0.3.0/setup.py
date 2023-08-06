from distutils.core import setup

setup(
    name='pytv',
    version='0.3.0',
    packages=['pytv'],
    url='https://github.com/DadImScared/pytv',
    license='MIT',
    author='Matthew Bernheimer',
    author_email='matthewbernheimer@gmail.com',
    description='Python library to use the TV MAZE API (www.tvmaze.com)',
    install_requires=['requests'],
)
