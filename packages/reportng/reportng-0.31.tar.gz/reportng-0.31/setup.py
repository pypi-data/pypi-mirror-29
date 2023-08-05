from distutils.core import setup

setup(
    name='reportng',
    packages=['reportng'],
    version='0.31',
    description='reportng is a simple python module that allows one to create beautiful yet simple Bootstrap 4 html reports. Reportng is capable of with any string type output that is generated by python.',
    author='securisec',
    author_email='',
    url='https://github.com/securisec/reportng',
    download_url='https://github.com/securisec/reportng/archive/0.31.tar.gz',
    keywords=['report', 'reporting', 'bootstrap'],
    classifiers=[],
    install_requires=[
        'dominate'
    ]
)
