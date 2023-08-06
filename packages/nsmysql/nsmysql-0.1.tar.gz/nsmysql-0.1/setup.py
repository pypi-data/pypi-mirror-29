from setuptools import setup

setup(name='nsmysql',
      version='0.1',
      description='Data exchange from net suite data to MySQL database',
      url='https://github.com/ghao2/nsmysql',
      author='Guoxuan Hao',
      author_email='haoguoxuan@gmail.com',
      license='MIT',
      packages=['nsmysql'],
      install_requires=[
          'pymysql',
          'pandas',
          'numpy',
      ],
      zip_safe=False)