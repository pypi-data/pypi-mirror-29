from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='de_conf_mat',
    version='0.1.0',
    description='混同行列から正解ラベル、予測ラベルのリストを取得するスクリプトです。ある事情があってこれをたくさん行う必要が出て来たため作りました。',
    long_description=readme,
    author='Yusuke Sakai',
    author_email='y.f.sakai@gmail.com',
    url='https://github.com/yuuuuwwww/de_conf_mat',
    install_requires=['numpy'],
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests'
)
