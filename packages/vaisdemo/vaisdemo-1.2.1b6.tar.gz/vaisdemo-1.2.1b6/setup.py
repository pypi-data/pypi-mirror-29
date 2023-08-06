import os
from setuptools import setup

if os.name == 'nt':
    required_packages = ["grpcio==1.4.0", "pyyaml", "future", "docutils", "pyaudio", "pygments", "pypiwin32", "kivy.deps.sdl2", "kivy.deps.glew", "kivy", "nltk", "rollbar", "ipgetter", "requests", "pygsheets"]
else:
    required_packages = ["grpcio==1.4.0", "pyyaml", "future", "docutils", "pyaudio", "pygments", "kivy", "nltk", "rollbar", "ipgetter", "requests", "pygsheets"]

if __name__ == "__main__":
    setup(
        name="vaisdemo",
        author='VAIS',
        packages=['vaisdemo'],
        package_data={'': ['vaisdemo/speech', 'vaisdemo/info']},
        author_email='support@vais.vn',
        url='https://vais.vn',
        include_package_data=True,
        install_requires=required_packages,
        version="1.2.1b6",
        python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
        provides=['vaisdemo'],
        entry_points = {'console_scripts': ['vaisdemo = vaisdemo.gui:main']}
    )
