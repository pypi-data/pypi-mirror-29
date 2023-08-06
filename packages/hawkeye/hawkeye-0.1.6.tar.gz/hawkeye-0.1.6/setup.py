from distutils.core import setup

setup(
    name='hawkeye',
    author='Todd L. Jarolimek II',
    author_email='tljarolimek@gmail.com',
    version='0.1.6',
    license='Apache License 2.0',
    # classifiers=[
    # 	'Development Status :: 3 - Alpha',
    # 	'Environment :: Console',
    # 	'Intended Audience :: Developers',
    # 	'License :: OSI Approved :: Apache Software License',
    # 	'Topic :: Software Development :: Build Tools',
    # 	'Natural Language :: English',
    # 	'Programming Language :: Python :: 3',
    # 	'Topic :: Database',
    # 	'Topic :: Internet :: WWW/HTTP',
    # 	'Topic :: Software Development'
    # ],
    keywords=['python', 'database', 'internet request', 'list', 'dictionary'],
    long_description=open('README.txt').read(),
    packages=["hawkeye",],
)