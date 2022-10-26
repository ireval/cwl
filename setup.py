import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='cwl-eval',
    version='1.0.12',
    
    scripts=['cwl-eval'],
    
    author='Leif Azzopardi, Paul Thomas, Alistair Moffat',
    author_email='leifos@acm.org, pathom@microsoft.com, ammoffat@unimelb.edu.au',
    
    description='An information retrieval evaluation script based on the C/W/L framework '
                'that is TREC Compatible and provides a replacement for INST_EVAL, RBP_EVAL, '
                'TBG_EVAL, UMeasure and TREC_EVAL scripts. All measurements are reported in '
                'the same units making all metrics directly comparable.',
    
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    url='https://github.com/ireval/cwl',

    packages=setuptools.find_packages(),
    
    python_requires='>=3',

    install_requires=[
        'numpy',
    ],
    
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',

    ],

)
