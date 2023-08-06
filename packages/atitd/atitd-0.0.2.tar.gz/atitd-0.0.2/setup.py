from setuptools import find_packages, setup

setup(
    name="atitd",
    author='Levi Noecker',
    author_email='levi.noecker@gmail.com',
    url='https://github.com/levi-rs/atitd',
    description="Python automation tools for A Tale In The Desert (ATITD)",
    packages=find_packages(),
    use_scm_version={'root': '.', 'relative_to': __file__},
    setup_requires=['setuptools_scm'],
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'atitd=atitd.cli:main',
        ]
    }
)
