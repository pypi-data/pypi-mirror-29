from setuptools import setup


def readme():
    with open('README.rst') as fpl:
        return fpl.read()


setup(
    name='url2vapi',
    version='1.2',
    description=(
        'Tools extracts constant elements from url (for example version)'
    ),
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: Utilities',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    url='https://github.com/Drachenfels/url2vapi',
    author="Drachenfels",
    author_email="drachu@gmail.com",
    license="MIT",
    packages=['url2vapi'],
    zip_safe=False
)
