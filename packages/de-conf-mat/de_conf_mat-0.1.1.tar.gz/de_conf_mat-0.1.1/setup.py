from setuptools import setup, find_packages

setup(
    name='de_conf_mat',
    version='0.1.1',
    description='混同行列から正解ラベル、予測ラベルのリストを取得するスクリプトです。ある事情があってこれをたくさん行う必要が出て来たため作りました。',
    author='Yusuke Sakai',
    author_email='y.f.sakai@gmail.com',
    url='https://github.com/yuuuuwwww/de_conf_mat',
    install_requires=['numpy'],
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests'
)
