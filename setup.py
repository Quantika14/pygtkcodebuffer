#!/usr/bin/python


from distutils.core import setup

desc = """PyGTKCodeBuffer - Lightweight syntax-highlighting for PyGTK's TextView-widget."""

long_desc = """PyGTKCodeBuffer is a syntax-highlighting engine written in pure 
Python to provide maximum portability. It depends only on PyGTK and the Python 
standard library. No Gnome nor Scintilla libraries are needed so it should run 
perfectly under all platforms supported by PyGTK!"""

setup ( name = 'PyGTKCodeBuffer',
        version = '0.1.0',
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
