from setuptools import setup

setup(
    name="pydotenv",
    version=__import__('pydotenv').__version__,
    author="Alexandre Varas",
    author_email="alej0varas@gmail.com",
    py_modules=['pydotenv', ],
    include_package_data=True,
    license='GNU Library or Lesser General Public License (LGPL)',
    description="A libray to write .env files",
    url='https://github.com/alej0varas/pydotenv',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
