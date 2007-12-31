#!/usr/bin/python
import gtk
from gtkcodebuffer import CodeBuffer, SyntaxLoader

txt = """
#include <stdio.h>

// main()
int main(void){

    return 0;
}
"""


lang = SyntaxLoader("cpp")
buff = CodeBuffer(lang=lang)

win = gtk.Window(gtk.WINDOW_TOPLEVEL)
scr = gtk.ScrolledWindow()
win.add(scr)
scr.add(gtk.TextView(buff))
        
win.set_default_size(300,200)
win.show_all()
        
buff.set_text(txt)
        
gtk.main()        
