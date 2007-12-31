#!/usr/bin/python
import gtk
import os.path
from codebuffer import CodeBuffer, SyntaxLoader, add_syntax_path

class App:
    def __init__(self):
        add_syntax_path("syntax")
        lang = SyntaxLoader("python")

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.on_delete)
        self.buffer = CodeBuffer(langdef=lang)
        scr = gtk.ScrolledWindow()
        self.window.add(scr)
        scr.add(gtk.TextView(self.buffer))
        
        self.window.set_default_size(300,200)
        self.window.show_all()
        
        fname = os.path.join(os.path.dirname(__file__), "codebuffer.py")
        self.buffer.set_text(open(fname,"r").read())
        
    def on_delete(self, widget):
        gtk.main_quit()
        
        
app = App()

gtk.main()        
