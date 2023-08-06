from setuptools import setup, find_packages

setup(
    name             = 'teak',
    version          = '0.0.2',
    description      = 'JSON validator/selector',
    author           = 'Beomyeong Kim',
    license          = 'BSD 3-Clause License',
    author_email     = 'ttl74283@gmail.com',
    url              = 'https://github.com/tibyte/teak',
    download_url     = 'https://github.com/tibyte/teak/archive/master.tar.gz',
    install_requires = [],
    packages         = find_packages(exclude = []),
    keywords         = ['json validator', 'json selector'],
    python_requires  = '>=3.4',
    package_data     =  {
        'teak' : [
    ]},
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
