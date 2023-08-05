from setuptools import setup, find_packages

setup(
    name='torchlite',
    version='0.1.2',

    description='A high level library for Pytorch',
    long_description="https://github.com/EKami/Torchlite/master/README.md",
    url='https://github.com/EKami/Torchlite',
    author='GODARD Tuatini',
    author_email='tuatinigodard@gmail.com',
    license='MIT',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],

    keywords='development',
    packages=find_packages(exclude=['tests']),
    install_requires=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
)
