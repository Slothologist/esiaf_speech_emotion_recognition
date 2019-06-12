from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# fetch values from package.xml
setup_args = generate_distutils_setup(
    name='esiaf_emotion_recognition',
    version='0.0.1',
    description='Emotion recognition using speech for the esiaf_ros framework',
    url='---none---',
    author='rfeldhans',
    author_email='rfeldh@gmail.com',
    license='---none---',
    install_requires=[
    ],
    packages=['esiaf_emotion_recognition']

)

setup(**setup_args)