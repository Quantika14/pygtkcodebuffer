# Introduction #
CodeBuffer derives from GTK's standard TextBuffer so it IS a TextBuffer unless you specify a language to highlight! Since a TextBuffer is just a model of a text you will need a view to view/edit this text. Such a view is provided by GTK it self. It is called TextView. Under _Examples_ you will find some code-examples how to use CodeBuffer in your application.

There are two different ways to use the CodeBuffer. The first way is to install the Python-package so you don't have to care about where the syntax-definitions are located. The other way is to ship CodeBuffer along with your code. In this case you need to say CodeBuffer where it finds the syntax-definitions or you "hard-code" a syntax-definition. Booth cases are shown in following section.


# Examples #

### Simplest usage ###
Following code-example will work if you have CodeBuffer installed.

```
#!/usr/bin/python
import gtk
from gtkcodebuffer import CodeBuffer, SyntaxLoader

lang = SyntaxLoader("python")
buff = CodeBuffer(lang=lang)

win = gtk.Window(gtk.WINDOW_TOPLEVEL)
scr = gtk.ScrolledWindow()
win.add(scr)
scr.add(gtk.TextView(buff))

win.set_default_size(300,200)
win.show_all()

buff.set_text('A test string with "quotes"')

gtk.main()
```

This example creates a small window with a TextView. I do not discuss the GTK stuff here but: TextView is the GTK-widget that displays the CodeBuffer. The CodeBuffer class is instanced with the optional argument `lang`. It specifies the language-description. A LanguageDescription is a set of rules and patterns that tells CodeBuffer which strings are to highlight! In this example this LanguageDescription is loaded from file by the SyntaxLoader-class. This class itself is a LanguageDescription but you do not need to know this. SyntaxLoader takes a single argument: The name of the language to highlight. SyntaxLoader now searches for a file named `python.xml` at the default locations `~/.pygtkcodeview/` and `sys.prefix+"share/pygtkcodeview/syntax/`.


### hard-coded syntax-definition ###
Following example shows you how to _hard-code_ a syntax-definition. Also this example only works if you have !PyGTKCodeBuffer installed.

```
import gtk

from gtkcodebuffer import CodeBuffer, Pattern, String, LanguageDefinition 

txt = """
# About 
This example shows you a hard-coded markdown 
syntax-definition. Supporting `code-segments`, 
**emphasized text** or *emphasized text*.

## list-support
- a simple list item
- an other

1. A ordered list
2. other item

#### n-th order heading
"""


# Syntax definition
emph  = String(r"\*", r"\*", style="datatype")
emph2 = String(r"\*\*", r"\*\*", style="datatype")
code  = String(r'`', r'`', style="special")
head  = Pattern(r"^#+.+$", style="keyword")
list1 = Pattern(r"^(- ).+$", style="comment", group=1)
list2 = Pattern(r"^(\d+\. ).+$", style="comment", group=1)
 
lang = LanguageDefinition([emph, emph2, code, head, list1, list2])

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
```

This example is an extended one of the first. It shows how you may _hard-code_ a syntax-definition instead of [using a syntax-file](LanguageDescription.md). The implemented syntax-definition is a small subset of the markdown-markup.