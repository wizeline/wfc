from setuptools import setup, find_packages

import wfc


def requirements(filename):
    with open(filename) as file:
        return [req for req in map(
            lambda line: line.strip(),
            filter(
                lambda line: not line.startswith('#'),
                file.readlines()
            )
        )]


if __name__ == '__main__':
    setup(
        name=wfc.get_name(),
        version=wfc.get_version(),
        url='https://github.com/wizeline/wfc',
        author=wfc.get_author(),
        author_email='diego.guzman@wizeline.com',
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
            'Programming Language :: Python 3.6.8',
            'Topic :: Utilities'
        ],
        test_require=requirements('requirements.txt'),
        install_requires=requirements('requirements.txt'),
        entry_points={"console_scripts": ["wfc = wfc.cli:main"]}
    )
