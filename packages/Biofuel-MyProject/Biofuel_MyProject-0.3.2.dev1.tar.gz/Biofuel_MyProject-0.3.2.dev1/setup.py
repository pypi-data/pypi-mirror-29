from setuptools import setup, find_packages

setup(
    name='Biofuel_MyProject',
    version='0.3.2.dev1',
    description='Predict flash point and cetane number of biofuel',
    long_description=open('README.md').read(),
    url='https://github.com/Zhangjt9317/Biofuel-Group-Project',
    author='Jingtian Zhang, Cheng Zeng, Renlong Zheng, Chenggang Xi',
    author_email='jtz9317@gmail.com',
    license='MIT',
    keywords='flash point and cetane number',
    packages=find_packages(exclude=['tests']),
#    install_requires=['neupy', 'pubchempy', 'sklearn', 'openbabel', 'pybel', 'tkinter'],
    project_urls={
        'Bug Reports': 'https://github.com/Zhangjt9317/Biofuel-Group-Project/issues',
        'Source': 'https://github.com/Zhangjt9317/Biofuel-Group-Project',
    },

)