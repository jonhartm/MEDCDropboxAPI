"""
DropApi python modules.
Ahmed Usman <usmanaa@umich.edu>
"""

from setuptools import setup

setup(
    name='medcbox',
    version='0.1.0',
    packages=['medcbox'],
    include_package_data=True,
    install_requires=[
            'click',
            'dropbox',
        ],
    python_requires='>=3.6',

)
"""
entry_points={
        'console_scripts': [
                'medcbox = medcbox.__main__:main',
            ]
        },

"""
