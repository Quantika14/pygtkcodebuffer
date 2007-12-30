#!/usr/bin/python
import gtk
from codebuffer import CodeBuffer, SyntaxLoader, add_syntax_path


txt="""
import math

class test:
    ''' Test string 
        Multiline '''
    def __init__(self):
        pass
        
def testfunc(x):
    return 0, 0.1, 0.3e-10, 0.3e10
    """        



class App:
    def __init__(self):
        add_syntax_path("syntax")
        lang = SyntaxLoader("python")

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.on_delete)
        self.buffer = CodeBuffer(langdef=lang)
        self.window.add(gtk.TextView(self.buffer))
        
        self.window.set_default_size(300,200)
        self.window.show_all()
        
        self.buffer.set_text(txt)
        
    def on_delete(self, widget):
        gtk.main_quit()
        
        
app = App()

gtk.main()        
