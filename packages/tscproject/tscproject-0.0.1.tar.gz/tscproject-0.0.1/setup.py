# coding: utf-8
"""
tscproject
~~~~~~~~

Init typescript skeleton project.

Setup
-----

.. code-block:: bash

    > pip install tscproject

Links
-----
* `README <https://github.com/husu/typeProject_initializer>`_

"""

from setuptools import setup
from os import path
from setuptools.command.install import install

here = path.abspath(path.dirname(__file__))


class MyInstall(install):
    def run(self):
        print("-- installing... (powered by lesscli) --")
        install.run(self)


setup(
        name = 'tscproject',
        version='0.0.1',
        description='A simple tool for init typescript skeleton project.',
        long_description=__doc__,
        url='https://github.com/husu/typeProject_initializer',
        author='qorzj',
        author_email='inull@qq.com',
        license='MIT',
        platforms=['any'],

        classifiers=[
            ],
        keywords='typescript tsc tscproject',
        packages = ['tscproject'],
        install_requires=[],

        cmdclass={'install': MyInstall},
        entry_points={
            'console_scripts': [
                'tscproject = tscproject.tsc:tsc_project_init',
                ],
            },
    )
