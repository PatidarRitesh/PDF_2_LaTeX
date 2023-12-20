from setuptools import setup, find_packages
from typing import List


def get_requirements(file_path:str)->List[str]:
    """
    This function will return the list of requirements from the requirements.txt file
    
    """
    hyphen_e_dot='-e .'
    requirements=[]
    with open(file_path,"r") as f:
        requirements=f.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if hyphen_e_dot in requirements:
            requirements.remove(hyphen_e_dot)


    return requirements
setup(
    name="pdf_2_tex",
    version="0.0.1",
    author="Ritesh " ,
    author2="Husain",
    author_email="riteshpatidar2499@gmail.com",
    author2_email="husainmalwat@iitgn.ac.in",
    description="A tool to convert pdf to latex",
    long_description="",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)
