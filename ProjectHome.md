# About #
PyGTKCodeBuffer is a syntax-highlighting engine written in pure Python to provide maximum portability. It depends only on PyGTK and the Python standard library. No Gnome nor Scintilla libraries are needed so it should run perfectly under all platforms supported by PyGTK!


# Features #
To keep this project lightweight the PyGTKCodeBuffer only provides you a model/buffer for code-viewing/editing. To view a code-buffer simply use the default gtk.TextView widget. This buffer provides you a simple way to build a editor with syntax-highlight support.

All code for PyGTKCodeBuffer is located in one source-file to allow you to ship PyGTKCodeBuffer along with your application so your costumers do not have to care about having PyGTKCodeBuffer installed.

  * Very portable: written in pure Python
  * No additionally dependencies: except PyGTK
  * Easy to integrate: Supports the gtk.TextBuffer-interface
  * Easy to distribute along your code: All code is located in one file.


# Get it & install #
Simply get the source-code package and untar it. cd into the created directory labelled `PyGTKCodeBuffer-0.x.x/` and execute `python setup.py install`.


# Projects using GtkCodeBuffer #
  * http://rednotebook.sf.net


# ChangeLog #
#### 1.0-RC2 - (2008-01-27) ####
  * fixed `reset_language()` and `update_styles()` methods
  * prevent recursion-limit problem on big files

#### 1.0-RC1 - (2008-01-15) ####
  * embedded styles in syntax-files (Chris+Me)
  * Updated Markdown syntax-file (Chris)

#### 0.3.4 - (2008-01-07) ####
  * A lot of bug-fixes! I recommend you to update...

#### 0.3.0 - (2008-01-05) ####
  * A lot of new languages (converted from GtkSourceView)
  * Improved markdown-support (Chris)
  * Custom styles (only for hard-coded lexers)

#### 0.2.0 - (2008-01-04) ####
  * Applied Chris's patch
  * Fixed minor-bugs
  * Added markdown syntax-file and example

#### 0.1.0 - (2008-01-01) ####
  * First release! Works so far and seems to be stable. Needs some more syntax-files and optimizations.