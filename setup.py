from setuptools import setup, find_packages

setup(
    name="proyecto integrado V",
    version="0.0.1",
    author="Adriana Aguilar - Edwin Villa",
    author_email="",
    description="",
    py_modules=["actividad_1","actividad_2","actividad_3"],
    install_requires=[
        "pandas==2.2.3",
        "openpyxl",
        "scikit-learn>=0.24.0",
        "requests==2.32.3",
        "beautifulsoup4==4.13.3"
    ]
) 
