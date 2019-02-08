import setuptools

with open('README.md', 'r') as fh:
    readme = fh.read()

requirements = [
    'requests',
]

setuptools.setup(
    name='active_campaign',
    version='0.1.0',
    author='Lorence Lim',
    author_email='jlorencelim@gmail.com',
    description='ActiveCampaign API library using version 3 of the API endpoints.',
    long_description=readme,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    url='https://github.com/rev365/active-campaign',
    packages=setuptools.find_packages(),
    license='MIT License',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='ActiveCampaign, CRM',
)
