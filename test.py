#!/usr/bin/python
import gtk
from gtkcodebuffer import CodeBuffer, SyntaxLoader, add_syntax_path


txt = """
#include <stdio.h>

// main()
int main(void){

    return 0;
}
"""

add_syntax_path("./syntax/")

lang = SyntaxLoader("cpp")
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
