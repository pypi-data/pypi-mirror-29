from setuptools import setup


setup(
    name='jutily',
    version='0.0.0.3',
    description='',
    url='https://github.com/the16thpythonist/ScopusWp',
    author='Jonas Teufel',
    author_email='jonseb1998@gmail.com',
    license='MIT',
    packages=['jutil'],
    include_package_data=True,
    install_requires=[
        'sqlalchemy>=1.2',
        'jinja2>=2.10',
    ],
    python_requires='>=3, <4'
)