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
        
buff.set_text(r'A test string with "quot\\\"es"')
        
gtk.main()        
