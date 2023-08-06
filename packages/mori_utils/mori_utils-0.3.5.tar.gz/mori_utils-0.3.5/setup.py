from setuptools import setup, find_packages

setup(
    name='mori_utils',
    version='0.3.5',
    description='Mori Personal Utils',
    author='moridisa',
    author_email='moridisa@moridisa.cn',
    url='https://github.com/moriW/mori_scaffold',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'pymongo',
        'pymysql',
        'pyodps',
        'kazoo',
    ],
)
