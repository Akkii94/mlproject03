from setuptools import setup, find_packages
from typing import List


HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str)->List(str):
    """This function will return list of requirments
        from requirements.txt file
    """
    """initializing empty list for storing"""
    requirements=[]

    """opening the file"""
    with open(file_path, 'rb') as file_obj:
        requirements = file_obj.readlines()
        requirements = [i.replace('\n','') for i in requirements]

        '''Removing hypen_dot_e if present in requirments'''
        if HYPHEN_E_DOT = '-e .' in requirements:
            requirements.remove(HYPHEN_E_DOT)








setup(
    name='mlproject03',
    version='0.0.1',
    author='Akshay Gawande',
    author_email='avgawande@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')
    )