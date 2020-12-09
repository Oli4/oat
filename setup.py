from setuptools import setup

requirements = [
    'PyQt5', 'numpy', 'opencv-python', 'qimage2ndarray', 'imageio',
    'sqlalchemy', 'cryptography', "requests", "pandas", "scikit-image"
]

test_requirements = [
    'pytest',
    'pytest-cov',
    'pytest-faulthandler',
    'pytest-mock',
    'pytest-qt',
    'pytest-xvfb',
]

setup(
    name='oat',
    version='0.0.1',
    description="A GUI to annotate multi modal retial images",
    author="Olivier Morelle",
    author_email='oli4morelle@gmail.com',
    url='https://github.com/Oli4/oat',
    packages=['oat', 'oat.tests', 'oat.models', 'oat.modules',
              'oat.utils', 'oat.views', 'oat.io', 'oat.core'],
    # package_data={'oat.images': ['*.png']},
    entry_points={
        'console_scripts': [
            'oat=oat.oatmain:main'
        ]
    },
    install_requires=requirements,
    zip_safe=False,
    keywords='oat',
    classifiers=[
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
