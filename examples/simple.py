#!/usr/bin/python
import gtk
from gtkcodebuffer import CodeBuffer, SyntaxLoader, add_syntax_path

#
# This example shows how to use the CodeBuffer. 
#   Note: You need to have PyGTKCodeBuffer installed!


lang = SyntaxLoader("python")
buff = CodeBuffer(lang=lang)

win = gtk.Window(gtk.WINDOW_TOPLEVEL)
scr = gtk.ScrolledWindow()
win.add(scr)
scr.add(gtk.TextView(buff))
        
win.set_default_size(300,200)
win.show_all()
win.connect("destroy", lambda w: gtk.main_quit())
        
buff.set_text(open(__file__,'r').read())
        
gtk.main()        
