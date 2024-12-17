from setuptools import find_packages, setup

setup(
    name='QApplication', 
    version='0.0.3',  
    author='Aditya',
    author_email='nysaditya@gmail.com',
    packages=find_packages(),
    install_requires=[],
    description='A modified version of QApplication, originally by Sunny Savita, replacing the deprecated ServiceContext module with the updated Setting module.',
    url='https://github.com/aditya-rac/QA_RAG_application',  
    project_urls={
        'Original Repository': 'https://github.com/sunnysavita10/Information-Retrival-Using-LlamaIdex-and-Google_Gemini',
        'Modified Repository': 'https://github.com/aditya-rac/QA_RAG_application',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',  # Ensures Python 3.9 compatibility.
)
