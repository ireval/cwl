import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='cwl-eval',
    version='1.0',
    
    scripts=['cwl-eval'],
    
    author='Leif Azzopardi, Paul Thomas, Alistair Moffat',
    author_email='leifos@acm.org, pathom@microsoft.com, ammffat@unimelb.edu.au',
    
    description='An information retrieval evaluation script based on the C/W/L framework that is TREC Compatible and provides a replacement for INST_EVAL, RBP_EVAL, TBG_EVAL, UMeasure, TREC_EVAL.',
    
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    url='https://github.com/ireval/cwl',
    
    packages=setuptools.find_packages(),
    
    python_requires='>=3',
    
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    
    install_requires=[
        'numpy == 1.15.0',
    ]
)