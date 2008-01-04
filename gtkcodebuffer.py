""" This module contains the PyGTKCodeBuffer-class. This class is a 
    specialisation of the gtk.TextBuffer and enables syntax-highlighting for 
    PyGTK's TextView-widget. """


# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import gtk
import re
import sys
import os.path
import xml.sax
import imp
from xml.sax.handler import ContentHandler
from xml.sax.saxutils import unescape



DEFAULT_STYLES = {
    'DEFAULT':      {'font': 'monospace'},
    'comment':      {'foreground': 'blue'},
    'preprocessor': {'foreground': 'violet'},
    'keyword':      {'foreground': 'darkred',
                     'weight': 700},
    'special':      {'foreground': 'turquoise'},
    'string':       {'foreground': 'magenta'},
    'number':       {'foreground': 'magenta'},
    'datatype':     {'foreground': 'sea green',
                     'weight': 700} }
        


def main_is_frozen():
    return (hasattr(sys, "frozen") or # new py2exe
            hasattr(sys, "importers") # old py2exe
            or imp.is_frozen("__main__")) # tools/freeze


if main_is_frozen():
    this_module_path = os.path.dirname(sys.executable)
else:
    this_module_path = os.path.abspath(os.path.dirname(__file__))


SYNTAX_PATH = [ os.path.join('.', 'syntax'),
                this_module_path,
                os.path.join(os.path.expanduser('~'),".pygtkcodebuffer"),
                os.path.join(sys.prefix,"share","pygtkcodebuffer","syntax")]
         

DEBUG_FLAG  = False




def add_syntax_path(path_or_list):
    global SYNTAX_PATH
    if isinstance(path_or_list, (list, tuple)):
        for i in range(len(path_or_list)):
            SYNTAX_PATH.insert(0, path_or_list[-i])
    elif isinstance(path_or_list, basestring):
        SYNTAX_PATH.insert(0, path_or_list)
    else:
        raise TypeError, "Argument must be path-string or list of strings"
        
        
        

class Pattern:
    """ More or less internal used class representing a pattern. """

    def __init__(self, regexp, style="DEFAULT", group=0, flags=""):
        # assemble re-flag
        flags += "ML"; flag   = 0
        if DEBUG_FLAG: 
            print "init rule %s -> %s (%s)"%(regexp, style, flags)
        for char in flags:
            if char == 'M': flag |= re.M
            if char == 'L': flag |= re.L
            if char == 'S': flag |= re.S
            if char == 'I': flag |= re.I
            if char == 'U': flag |= re.U
            if char == 'X': flag |= re.X
        # compile re        
        self._regexp = re.compile(regexp, flag)
        self._group  = group
        self.tag_name = style
        
        
    def __call__(self, txt, start, end):
        m = self._regexp.search(txt)
        if DEBUG_FLAG:
            print "Search for %s at %s..."%(self._regexp.pattern, start.get_offset())
        if not m: return None
        if DEBUG_FLAG:
            print "... found \"%s\" (%s)"%(m.group(self._group), self.tag_name)
        
        mstart, mend = m.start(self._group), m.end(self._group)
        s = start.copy(); s.forward_chars(mstart)
        e = start.copy(); e.forward_chars(mend)
        
        return (s,e)    
    



class KeywordList(Pattern):
    def __init__(self, keywords, style="keyword"):
        regexp = "(?:\W|^)(%s)\W"%("|".join(keywords),)
        Pattern.__init__(self, regexp, style, group=1, flags="")
        
        
        
    
class String:
    def __init__(self, starts, ends, escape=None, style="string"):
        self._starts  = re.compile(starts)
        
        if escape:
            end_exp = "[^%(esc)s](?:%(esc)s%(esc)s)*%(end)s"
            end_exp = end_exp%{'esc':escape*2,'end':ends}
        else:
            end_exp = ends
            
        self._ends    = re.compile(end_exp)
        self.tag_name = style


    def __call__(self, txt, start, end):
        if DEBUG_FLAG:
            print "Search string (%s) at %i..."%(self._starts.pattern, start.get_offset())
        
        start_match = self._starts.search(txt)
        if not start_match: return
        
        if DEBUG_FLAG:
            print "... found string start at %s"%(start_match.start(0))
            
        start_it = start.copy()
        start_it.forward_chars(start_match.start(0))
        end_it   = end.copy()
        
        end_match = self._ends.search(txt, start_match.end(0))
        if end_match:
            if DEBUG_FLAG:
                print "... found string and at %s"%(start.get_offset()+end_match.end(0))
            end_it.set_offset(start.get_offset()+end_match.end(0))            
            
        return  start_it, end_it
        
        
        
        
class LanguageDefinition:
    def __init__(self, rules):
        self._grammar = rules
        
    def __call__(self, buf, start, end=None):
        # if no end given -> end of buffer
        if not end: end = buf.get_end_iter()
    
        if DEBUG_FLAG:
            print "Apply lang-rules at %s..."%(start.get_offset())
            
        mstart = mend = end
        mtag   = None
        txt = buf.get_slice(start, end)    
        
        # search min match
        for rule in self._grammar:
            # search pattern
            m = rule(txt, start, end)            
            if not m: continue
            
            # prefer match with smallest start-iter 
            if m[0].compare(mstart) < 0:
                mstart, mend = m
                mtag = rule.tag_name
                continue
            
            if m[0].compare(mstart)==0 and m[1].compare(mend)>0:
                mstart, mend = m
                mtag = rule.tag_name
                continue

        return (mstart, mend, mtag)                




class SyntaxLoader(ContentHandler, LanguageDefinition):
    def __init__(self, lang_name):
        LanguageDefinition.__init__(self, [])
        ContentHandler.__init__(self)
       
        print SYNTAX_PATH 
        # search for syntax-files:
        fname = None
        for syntax_dir in SYNTAX_PATH:
            fname = os.path.join(syntax_dir, "%s.xml"%lang_name)
            if os.path.isfile(fname): break

        if DEBUG_FLAG:
            print "Loading syntaxfile %s"%fname

        xml.sax.parse(fname, self)
      
        
    # Dispatch start/end - document/element and chars        
    def startDocument(self):
        self.__stack   = []
                
    def endDocument(self):
        del self.__stack
        
    def startElement(self, name, attr):
        self.__stack.append( (name, attr) )
        if hasattr(self, "start_%s"%name):
            handler = getattr(self, "start_%s"%name)
            handler(attr)
    
    def endElement(self, name):
        if hasattr(self, "end_%s"%name):
            handler = getattr(self, "end_%s"%name)
            handler()
        del self.__stack[-1]

    def characters(self, txt):
        if not self.__stack: return
        name, attr = self.__stack[-1]
        
        if hasattr(self, "chars_%s"%name):
            handler = getattr(self, "chars_%s"%name)
            handler(txt)
            

    # Handle regexp-patterns
    def start_pattern(self, attr):
        self.__pattern = None
        self.__group   = 0
        self.__flags   = ''
        self.__style   = attr['style']
        if 'group' in attr.keys(): self.__group = int(attr['group'])
        if 'flags' in attr.keys(): self.__flags = attr['flags']
        
    def end_pattern(self):
        rule = Pattern(self.__pattern, self.__style, self.__group, self.__flags)
        self._grammar.append(rule)
        del self.__pattern
        del self.__group
        del self.__flags
        del self.__style
        
    def chars_pattern(self, txt):
        self.__pattern = unescape(txt)
                    

    # handle keyword-lists
    def start_keywordlist(self, attr):
        self.__style = "keyword"
        if 'style' in attr.keys():
            self.__style = attr['style']
        self.__keywords = []
        
    def end_keywordlist(self):
        kwlist = KeywordList(self.__keywords, self.__style)
        self._grammar.append(kwlist)
        del self.__keywords
        del self.__style
            
    def chars_keyword(self, txt):
        parent,pattr = self.__stack[-2]
        if not parent == "keywordlist": return
        self.__keywords.append(unescape(txt))


    #handle String-definitions
    def start_string(self, attr):
        self.__style = "string"
        self.__escape = None
        if 'escape' in attr.keys():
            self.__escape = attr['escape']
        if 'style' in attr.keys():
            self.__style = attr['style']
        self.__start_pattern = None
        self.__end_pattern = None

    def end_string(self):
        strdef = String(self.__start_pattern, self.__end_pattern,
                        self.__escape, self.__style)
        self._grammar.append(strdef)
        del self.__style
        del self.__escape
        del self.__start_pattern
        del self.__end_pattern
        
    def chars_starts(self, txt):
        self.__start_pattern = unescape(txt)
        
    def chars_ends(self, txt):
        self.__end_pattern = unescape(txt)




class CodeBuffer(gtk.TextBuffer):
    def __init__(self, table=None, lang=None, styles={}):
        gtk.TextBuffer.__init__(self, table)

        # default styles    
        self.styles = DEFAULT_STYLES
                       
        # update with user-defined
        self.styles.update(styles)
        
        # create tags
        for name, props in self.styles.items():
            style = dict(self.styles['DEFAULT'])    # take default
            style.update(props)                     # and update with props
            self.create_tag(name, **style)
        
        # store lang-definition
        self._lang_def = lang
        
        self.connect_after("insert-text", self._on_insert_text)
        self.connect_after("delete-range", self._on_delete_range)
        
        
    def _on_insert_text(self, buf, it, text, length):
        # if no syntax defined -> nop
        if not self._lang_def: return False
        
        it.backward_chars(length-1)
        tags = it.get_tags()
        if len(tags)>0:
            it.backward_to_tag_toggle(tags[0])
                
        self.update_syntax(it)        
        
        
    def _on_delete_range(self, buf, start, end):
        # if no syntax defined -> nop
        if not self._lang_def: return False
        
        tags = start.get_tags()
        if len(tags)>0:
            start.backward_to_tag_toggle(tags[0])
        
        self.update_syntax(start)        
        
    
    def update_syntax(self, start, end=None):
        # if not end defined
        if not end: end = self.get_end_iter()
        
        # search first rule matching txt[start..end]            
        mstart, mend, tagname = self._lang_def(self, start, end)
        
        # optimisation: if mstart-mend is allready tagged with tagname 
        #   -> finished
        if tagname:     #if something found
            tag = self.get_tag_table().lookup(tagname)
            if mstart.begins_tag(tag) and mend.ends_tag(tag):
                return
                
        # remove all tags from start..mend (mend == buffer-end if no match)        
        self.remove_all_tags(start, mend)
        # make start..mstart = DEFAUL (mstart == buffer-end if no match)
        self.apply_tag_by_name("DEFAULT", start, mstart)                
        
        # nothing found -> finished
        if not tagname: 
            return
        
        # apply tag
        self.apply_tag_by_name(tagname, mstart, mend)
        
        # continue at mend
        self.update_syntax(mend, end)
        
        
    def reset_language(self, lang_def):
        start = self.get_start_iter()
        self.remove_all_tags(start, self.get_end_iter())
        self._lang_def = lang_def
        self.update_syntax(start)
        
        
        
    
