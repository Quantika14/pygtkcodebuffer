#!/usr/bin/python
import gtk
from gtkcodebuffer import CodeBuffer, SyntaxLoader, add_syntax_path


txt = """
# About 
This example shows you a markdown with XML file
syntax-definition. Supporting `code-segments`, 
**emphasized text** or *emphasized text*. 

Alterative emphasis style:
_single underscores_ and __double underscores__.
Note that a variable like some_stuff_list is not _emphasized_. 
See "Middle-World Emphasis" at 
<http://www.freewisdom.org/projects/python-markdown/Features> 
along with <http://six.pairlist.net/pipermail/markdown-discuss/2005-October/001610.html>


This is simply multiplication, 3 * 23 + constant * 11 = x.
I.e. it is not emphasized.


For more Markdown information see URLs <http://en.wikipedia.org/wiki/Markdown>
and <http://daringfireball.net/projects/markdown/>


## list-support
- a simple list item
+ an other style
* yet other list/bullet style

1. A ordered list
2. other item

#### n-th order heading

## Indents/code
This demos the other code markup style, space indentation:

    this is pre-formated text
    as is this.

Indentation with tabs:

\tthis is pre-formated text
\tas is this. Prefixed with tab

Next is quoting (indentation):

> This is quoted text,
> as is this.


## TODO and Unsupported Markup

TODO! I've overloaded some of the styles/colours in the XML file,
e.g. URLs are datatypes (like emphasis).

Currently does not handle:

*   Horizontal Rules/Lines
*   Square bracket "[]" style links/urls
*   lists that have multiple lines and the extra lines
    are indented (appear as code). E.g. this line :-)
*   lists with leading spaces (it should).
*   Underlined header.
*   br line breaks (not sure it makes sense to do so)

"""

add_syntax_path("../syntax/")

lang = SyntaxLoader("markdown")
buff = CodeBuffer(lang=lang)

win = gtk.Window(gtk.WINDOW_TOPLEVEL)
scr = gtk.ScrolledWindow()
win.add(scr)
scr.add(gtk.TextView(buff))
        
win.set_default_size(300,200)
win.show_all()
win.connect("destroy", lambda w: gtk.main_quit())
        
buff.set_text(txt)
        
gtk.main()        
