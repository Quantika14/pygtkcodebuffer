#!/usr/bin/python


from distutils.core import setup

desc = """ PyGTKCodeBuffer """

long_desc = """ PyGTKCodeBuffer"""

setup ( name = 'PyGTKCodeBuffer',
        version = '0.99.5',
        description = desc,
        long_description = long_desc,
        author = 'Hannes Matuschek',
        author_email = 'hmatuschek@gmail.com',
        url = 'http://pygtkcodebuffer.googlecode.com',

        classifiers = ['Development Status :: 5 - Production/Stable',
                       'Environment :: X11 Applications :: GTK',
                       'Intended Audience :: Education',
                       'Intended Audience :: End Users/Desktop',
                       'License :: OSI Approved :: GNU General Public License (GPL)',
                       'Operating System :: POSIX :: Linux',
                       'Programming Language :: Python',
                       'Topic :: Communications :: Ham Radio'], 

        py_modules = ['gtkcodebuffer'],
        
        data_files = [('share/pygtkcodebuffer/syntax',   
                        ['syntax/python.xml', 'syntax/cpp.xml'])]
      )                
