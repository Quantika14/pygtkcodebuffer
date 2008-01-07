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
    'comment':      {'foreground': '#0000FF'},
    'preprocessor': {'foreground': '#A020F0'},
    'keyword':      {'foreground': '#A52A2A',
                     'weight': 700},
    'special':      {'foreground': 'turquoise'},
    'mark1':        {'foreground': '#008B8B'},
    'mark2':        {'foreground': '#6A5ACD'},
    'string':       {'foreground': '#FF00FF'},
    'number':       {'foreground': '#FF00FF'},
    'datatype':     {'foreground': '#2E8B57',
                     'weight': 700},
    'function':     {'foreground': '#008A8C'} }
        


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
        try: self._regexp = re.compile(regexp, flag)
        except re.error, e: 
            raise Exception("Invalid regexp \"%s\": %s"%(regexp,str(e)))
        self._group  = group
        self.tag_name = style
        
        
    def __call__(self, txt, start, end):
        m = self._regexp.search(txt)
        if not m: return None
        
        mstart, mend = m.start(self._group), m.end(self._group)
        s = start.copy(); s.forward_chars(mstart)
        e = start.copy(); e.forward_chars(mend)
        
        return (s,e)    
    



class KeywordList(Pattern):
    def __init__(self, keywords, style="keyword", flags=""):
        regexp = "(?:\W|^)(%s)\W"%("|".join(keywords),)
        Pattern.__init__(self, regexp, style, group=1, flags=flags)
        
        
        
    
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
        start_match = self._starts.search(txt)
        if not start_match: return
        
        start_it = start.copy()
        start_it.forward_chars(start_match.start(0))
        end_it   = end.copy()
        
        end_match = self._ends.search(txt, start_match.end(0)-1)
        if end_match:
            end_it.set_offset(start.get_offset()+end_match.end(0))            
            
        return  start_it, end_it
        
        
        
        
class LanguageDefinition:
    def __init__(self, rules):
        self._grammar = rules
        
    def __call__(self, buf, start, end=None):
        # if no end given -> end of buffer
        if not end: end = buf.get_end_iter()
    
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
        self.__pattern = ""
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
        self.__pattern += unescape(txt)
                    

    # handle keyword-lists
    def start_keywordlist(self, attr):
        self.__style = "keyword"
        self.__flags = ""
        if 'style' in attr.keys():
            self.__style = attr['style']
        if 'flags' in attr.keys():
            self.__flags = attr['flags']
        self.__keywords = []
        
    def end_keywordlist(self):
        kwlist = KeywordList(self.__keywords, self.__style, self.__flags)
        self._grammar.append(kwlist)
        del self.__keywords
        del self.__style
        del self.__flags
        
    def start_keyword(self, attr):
        self.__keywords.append("")
    
    def end_keyword(self):
        if not self.__keywords[-1]:
            del self.__keywords[-1]
                
    def chars_keyword(self, txt):
        parent,pattr = self.__stack[-2]
        if not parent == "keywordlist": return
        self.__keywords[-1] += unescape(txt)


    #handle String-definitions
    def start_string(self, attr):
        self.__style = "string"
        self.__escape = None
        if 'escape' in attr.keys():
            self.__escape = attr['escape']
        if 'style' in attr.keys():
            self.__style = attr['style']
        self.__start_pattern = ""
        self.__end_pattern = ""

    def end_string(self):
        strdef = String(self.__start_pattern, self.__end_pattern,
                        self.__escape, self.__style)
        self._grammar.append(strdef)
        del self.__style
        del self.__escape
        del self.__start_pattern
        del self.__end_pattern
        
    def chars_starts(self, txt):
        self.__start_pattern += unescape(txt)
        
    def chars_ends(self, txt):
        self.__end_pattern += unescape(txt)




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
        self.connect('apply-tag', self._on_apply_tag)
        
        self._apply_tags = False
                
                
    def _on_apply_tag(self, buf, tag, start, end):
        # FIXME This is a hack! It allows apply-tag only while
        #       _on_insert_text() and _on_delete_range()
        if not self._apply_tags:
            self.emit_stop_by_name('apply-tag')
            return True
            
        if DEBUG_FLAG:    
            print "tag \"%s\" as %s"%(self.get_slice(start,end), tag.get_property("name"))
            
                            
    def _on_insert_text(self, buf, it, text, length):
        # if no syntax defined -> nop
        if not self._lang_def: return False
        
        it = it.copy()
        it.backward_chars(length)
        
        if not it.begins_tag():
            it.backward_to_tag_toggle(None)
            if DEBUG_FLAG:
                print "Not tag-start -> moved iter to %i (%s)"%(it.get_offset(), it.get_char()) 

        if it.begins_tag(self.get_tag_table().lookup("DEFAULT")):
            it.backward_to_tag_toggle(None)
            if DEBUG_FLAG:
                print "Iter at DEFAULT-start -> moved to %i (%s)"%(it.get_offset(), it.get_char())
            
        self._apply_tags = True    
        self.update_syntax(it)        
        self._apply_tags = False
        
        
    def _on_delete_range(self, buf, start, end):
        # if no syntax defined -> nop
        if not self._lang_def: return False

        start = start.copy()
        if not start.begins_tag():
            start.backward_to_tag_toggle(None)
    
        self._apply_tags = True                
        self.update_syntax(start)        
        self._apply_tags = False
        
    
    def update_syntax(self, start, end=None):
        if DEBUG_FLAG:
            print "Update syntax from %i"%start.get_offset()
            
        # if not end defined
        if not end: end = self.get_end_iter()
        
        # search first rule matching txt[start..end]            
        mstart, mend, tagname = self._lang_def(self, start, end)
        
        # optimisation: if mstart-mend is allready tagged with tagname 
        #   -> finished
        if tagname:     #if something found
            tag = self.get_tag_table().lookup(tagname)
            if mstart.begins_tag(tag) and mend.ends_tag(tag) and not mstart.equal(start):
                self.remove_all_tags(start,mstart)
                self.apply_tag_by_name("DEFAULT", start, mstart)
                if DEBUG_FLAG:
                    print "Optimized: Found old tag at %i (%s)"%(mstart.get_offset(), mstart.get_char())
                return
                
        # remove all tags from start..mend (mend == buffer-end if no match)        
        self.remove_all_tags(start, mend)
        # make start..mstart = DEFAUL (mstart == buffer-end if no match)
        if not start.equal(mstart):
            self.apply_tag_by_name("DEFAULT", start, mstart)                
        
        # nothing found -> finished
        if not tagname: 
            return
        
        # apply tag
        self.apply_tag_by_name(tagname, mstart, mend)
        
        # continue at mend
        self.update_syntax(mend, end)
        
        
    def reset_language(self, lang_def):
        # remove all tags from complete text
        start = self.get_start_iter()
        self.remove_all_tags(start, self.get_end_iter())
        # store lexer
        self._lang_def = lang_def
        # and ...
        self.update_syntax(start)
        
        
    def update_styles(self, styles):
        self.styles.update(styles)
        
        table = self.get_tag_table()
        for name, props in styles.items():
            style = dict(DEFAULT_STYLES['DEFAULT'])
            style.update(props)
            # if tagname is unknown:
            if not table.lookup(name):
                self.create_tag(name, **style) 
            else: # update tag
                tag = table.lookup(name)
                map(lambda k,v: tag.set_property(k,v), style.items())
                    
