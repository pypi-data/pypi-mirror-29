from setuptools import setup

setup(
    name = 'ppr',
    version = '0.1.0',
    packages = ['ppr'],
    description = 'Planar Python Robotics',
    author = 'Jeroen De Maeyer',
    author_email = 'jeroen.demaeyer@kuleuven.be',
    url = 'https://u0100037.pages.mech.kuleuven.be/planar_python_robotics/',
    download_url = 'https://www.dropbox.com/s/xmatlsnfo1wkvdm/planar_python_robotics-0.1.0-c73194204d7e0b21aba03f56808c07e268b1d887.tar.gz?dl=0',
    keywords = ['robotics', 'motion planning'],
    classifiers = [],
    install_requires=['scipy', 'matplotlib'],
    python_requires='>=3',
)
