from distutils.core import setup

setup(
    name='dotf',
    version='0.0.1',
    description='A dotfiles manager',
    author='Nathan Gaberel',
    author_email='nathan@gnab.fr',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='dotfiles manager dot',
    url='https://github.com/n6g7/dot',
    license='MIT',
    packages=[
        'dot',
        'dot.commands',
    ],
    scripts=['bin/dot'],
    install_requires=[
        'crayons',
    ]
)
