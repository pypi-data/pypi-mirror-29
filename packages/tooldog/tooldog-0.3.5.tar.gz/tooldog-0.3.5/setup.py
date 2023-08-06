from setuptools import setup
import sys, os

exec(open('tooldog/version.py').read())

setup(name="tooldog",
        version=__version__,
        description='Tool description generator (from https//bio.tools to XML and CWL)',
        author='Kenzo-Hugo Hillion, Ivan Kuzmin and Herve Menager',
        author_email='kehillio@pasteur.fr',
        license='MIT',
        keywords = ['biotools','galaxy','xml','cwl'],
        install_requires=['rdflib', 'requests', 'galaxyxml', 'cwlgen>=0.2.3', 'docker==2.1.0'],
        packages=["tooldog", "tooldog.annotate", "tooldog.analyse"],
        package_data={
        'tooldog': ['annotate/data/*'],
        },
        entry_points={'console_scripts':['tooldog=tooldog.main:run']},
        classifiers=[
            'Development Status :: 4 - Beta',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            'Operating System :: OS Independent',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Environment :: Console',
            ],
        )
