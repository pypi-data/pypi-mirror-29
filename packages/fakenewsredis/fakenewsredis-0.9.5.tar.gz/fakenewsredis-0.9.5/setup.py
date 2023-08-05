import os

from setuptools import setup


setup(
    name='fakenewsredis',
    version='0.9.5',
    description="Fake implementation of redis API for testing purposes.",
    long_description=open(os.path.join(os.path.dirname(__file__),
                                       'README.rst')).read(),
    license='BSD',
    url="https://github.com/ska-sa/fakenewsredis",
    author='James Saryerwinnie',
    author_email='js@jamesls.com',
    maintainer='Bruce Merry',
    maintainer_email='bmerry@ska.ac.za',
    py_modules=['fakenewsredis'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'redis',
    ],
    extras_require={
        "lua": ['lupa']
    }
)
