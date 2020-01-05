import os
import setuptools

here = os.path.abspath(os.path.dirname(__file__))

info = {}
with open(os.path.join(here, 'enmon', '__info__.py'), 'r') as f:
    exec(f.read(), info)

with open('requirements.txt', 'r') as f:
    requirements = f.read()

with open('README.md', 'r') as f:
    readme = f.read()

setuptools.setup(
    name=info['TITLE'],
    version=info['VERSION'],
    author=info['AUTHOR'],
    author_email=info['EMAIL'],
    description=info['DESCRIPTION'],
    long_description=readme,
    long_description_content_type='text/markdown',
    url=info['URL'],
    license=info['LICENSE'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux'
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
    ],
    keywords='hardwario iot mqtt bridge sensor cli temperature humidity pressure altitude illuminance',
    platforms='any',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            '{}={}:main'.format(info['TITLE'], info['TITLE'])
        ]
    }
)
