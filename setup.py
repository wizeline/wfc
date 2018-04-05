import re

from pip.req import parse_requirements
from setuptools import setup, find_packages


def requirements(filename):
    reqs = parse_requirements(filename, session=False)
    return [str(r.req) for r in reqs]


def get_property(prop):
    with open('wfc/__init__.py', 'r') as f:
        prop_regex = r'__{}__\s*=\s*[\'"](.+)[\'"]'.format(prop)
        return re.search(prop_regex, f.read(), re.MULTILINE).group(1)


if __name__ == '__main__':
    package_name = get_property('name')
    setup(
        name=package_name,
        version=get_property('version'),
        url='https://github.com/wizeline/wfc',
        author=get_property('author'),
        author_email='engineering@wizeline.com',
        description='Wizeline Flow Compiler',
        packages=find_packages(exclude=['tests']),
        include_package_data=True,
        zip_safe=False,
        classifiers=[
            'Development Status :: Development',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS :: MacOS X',
            'Programming Language :: Python 3.6.2',
            'Topic :: Utilities'
        ],
        test_require=requirements('requirements.txt'),
        install_requires=requirements('requirements.txt'),
        entry_points={"console_scripts": ["wfc = wfc.cli:main"]}
    )
