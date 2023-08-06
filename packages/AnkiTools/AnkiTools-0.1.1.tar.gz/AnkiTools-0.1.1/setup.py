from setuptools import setup

setup(name='AnkiTools',
      version='0.1.1',
      description='Anki *.apkg reader in a human-readable format; and an editor.',
      url='https://github.com/patarapolw/AnkiTools',
      author='Pacharapol Withayasakpunt',
      author_email='patarapolw@gmail.com',
      license='MIT',
      packages=['AnkiTools'],
      install_requires=['requests'],
      python_requires='>=2.7'
      )
