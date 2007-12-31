import gtk
import cProfile
import pstats
from codebuffer import CodeBuffer, Range, Pattern, LanguageDefinition
import codebuffer


test1 = """
buf1.insert_at_cursor(open('codebuffer.py',"r").read())
while gtk.events_pending():
    gtk.main_iteration(False)
"""

test2 = """
buf2.insert_at_cursor(open('codebuffer.py',"r").read())
while gtk.events_pending():
    gtk.main_iteration(False)
"""


lang1 = LanguageDefinition([Range('"""','"""','string')])
lang2 = LanguageDefinition([Pattern('""".*?"""','string', flags="S")])

buf1 = CodeBuffer(langdef=lang1)
buf2 = CodeBuffer(langdef=lang2)

cProfile.run(test2, 'pattern')
cProfile.run(test1, 'range')

p1 = pstats.Stats('range')
p2 = pstats.Stats('pattern')

p1.print_stats('codebuffer')
p2.print_stats('codebuffer')

