import sys
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter

def format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    if type(color) is not str:
        _color.setRgb(color[0], color[1], color[2])
    else:
        _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages

STYLES2 = {
    'keyword': format([200, 120, 50], 'bold'),
    'operator': format([150, 150, 150]),
    'brace': format('darkGray'),
    'defclass': format([220, 220, 255], 'bold'),
    'string': format([20, 110, 100]),
    'string2': format([30, 120, 110]),
    'comment': format([128, 128, 128]),
    'self': format([150, 85, 140], 'italic'),
    'this': format([150, 85, 140], 'italic'),
    'numbers': format([100, 150, 190]),

    'c#_access_modifiers': format([150, 150, 190]),
    'c#_modifiers': format([123, 150, 120]),
    'c#_exception': format([150, 190, 200]),
    'c#_checked': format([20, 42, 129]),
    'c#_method_params': format([98, 60, 10], 'italic'),
    'c#_namespace': format([245, 95, 75]),
    'c#_generic': format([193, 240, 85]),
    'c#_access': format([65, 193, 42], 'italic'),
    'c#_literal': format([42, 65, 240], 'bold'),
    'c#_context': format([100, 100, 193]),
    'c#_query': format([75, 200, 42]),
    'c#_loopandcondition': format([75, 200, 42], 'bold'),
    'c#_types': format([75, 200, 42], 'italic'),
}

STYLES = {
       'keyword': format('blue'),
       'operator': format('red'),
       'brace': format('darkGray'),
       'defclass': format('black', 'bold'),
       'string': format('magenta'),
       'string2': format('darkMagenta'),
       'comment': format('darkGreen', 'italic'),
       'self': format('black', 'italic'),
       'numbers': format('brown'),
   }
class CommonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for the Python and C# languages.
    """
    # Python keywords
    python_keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False',
    ]

    # Python operators
    python_operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=',
        # Bitwise
        '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    # Python braces
    python_braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    # C# keywords
    csharp_keywords = ['abstract', 'as', 'base', 'bool', 'break', 'byte', 'case', 'catch', 'char', 'checked', 'class', 'const',
                'continue', 'decimal', 'default', 'delegate', 'do', 'double', 'else', 'enum', 'event', 'explicit',
                'extern', 'false', 'finally', 'fixed', 'float', 'for', 'foreach', 'goto', 'if', 'implicit', 'in', 'int',
                'interface', 'internal', 'is', 'lock', 'long', 'namespace', 'new', 'null', 'object', 'operator',
                'out', 'override', 'params', 'private', 'protected', 'public', 'readonly', 'ref', 'return', 'sbyte',
                'sealed', 'short', 'sizeof', 'stackalloc', 'static', 'string', 'struct', 'switch', 'this', 'throw',
                'true', 'try', 'typeof', 'uint', 'ulong', 'unchecked', 'unsafe', 'ushort', 'using', 'virtual', 'void',
                'volatile', 'while']

    # C# operators
    csharp_operators = [
        # Arithmetic
        '+', '-', '*', '/', '%', '++', '--',
        # Relational
        '==', '!=', '>', '<', '>=', '<=',
        # Logical
        #'&&', '||', '!',
        # Bitwise
        #'\&', '\|', '\^', '\~', '<<', '>>',
        # Assignment
        #'=', '\+=', '\-=', '\*=', '/=', '&=', '<<=', '>>=', '&=', '^=', '|=',
        # Conditional
        #'?', ':',

    ]
    # C# braces
    csharp_braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]
    def __init__(self, document, extension):
        QSyntaxHighlighter.__init__(self, document)
        self.extension = extension
        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])
        self.set_extenstion_rules()

    def set_extenstion_rules(self):
        rules = []

        config_dict = {
            "py_rules": rules,
            "cs_rules": rules,

            "py_styles": STYLES,
            "cs_styles": STYLES2,

            "py_keywords": CommonHighlighter.python_keywords,
            "cs_keywords": CommonHighlighter.csharp_keywords,

            "py_operators": CommonHighlighter.python_operators,
            "cs_operators": CommonHighlighter.csharp_operators,

            "py_braces": CommonHighlighter.python_braces,
            "cs_braces": CommonHighlighter.csharp_braces,
        }

        # Keyword, operator, and brace rules for Python
        config_dict[self.extension + "_rules"] += [(r'\b%s\b' % w, 0, config_dict[self.extension + "_styles"]['keyword'])
                                              for w in config_dict[self.extension + "_keywords"]]
        config_dict[self.extension + "_rules"] += [(r'%s' % o, 0, config_dict[self.extension + "_styles"]['operator'])
                                              for o in config_dict[self.extension + "_operators"]]
        config_dict[self.extension + "_rules"] += [(r'%s' % b, 0, config_dict[self.extension + "_styles"]['brace'])
                                              for b in config_dict[self.extension + "_braces"]]

        # All other rules
        config_dict[self.extension + "_rules"] += [
                # 'self'
                (r'\bself\b', 0, STYLES['self']),
                # Double-quoted string, possibly containing escape sequences
                (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
                # Single-quoted string, possibly containing escape sequences
                (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

                # 'def' followed by an identifier
                (r'\bdef\b\s*(\w+)', 1, STYLES['defclass']),
                # 'class' followed by an identifier
                (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),

                # From '#' until a newline
                (r'#[^\n]*', 0, STYLES['comment']),

                # Numeric literals
                (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
                (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
                (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
            ]


        # All other rules
        config_dict[self.extension + "_rules"] += [
                (r'\binternal|private|protected|public|protected internal|private protected\b', 0,
                 STYLES2['c#_access_modifiers']),
                (r'\bthrow|try|catch|finally\b', 0, STYLES2['c#_exception']),
                (r'\bchecked\unchecked|fixed\b', 0, STYLES2['c#_checked']),
                (r'\busing\b', 0, STYLES2['c#_namespace']),
                (r'\bnew|where\b', 0, STYLES2['c#_generic']),
                (r'\bthis|base\b', 0, STYLES2['c#_access']),
                (r'\bnull|true|false|default\b', 0, STYLES2['c#_literal']),
                (r'\badd|get|init|partial|remove|set|when|value|yield\b', 0, STYLES2['c#_context']),
                (r'\bfrom|where|select|group|into|orderby|join|let|ascending|descending|equals\b', 0,
                 STYLES2['c#_query']),
                (r'\bint|short|long|string|char|bool|float|double|byte|decimal|sbyte|uint|ulong|void|return\b', 0,
                 STYLES2['c#_types']),
                (r'\bif|switch|case|then|else|else if|while|for\b', 0, STYLES2['c#_loopandcondition']),
                # Double-quoted string, possibly containing escape sequences
                (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES2['string']),
                # Single-quoted string, possibly containing escape sequences
                (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES2['string']),

                # 'class' followed by an identifier
                (r'\bclass\b\s*(\w+)', 1, STYLES2['defclass']),

                # From '#' until a newline
                (r'//[^\n]*', 0, STYLES2['comment']),

                # Numeric literals
                (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES2['numbers']),
                (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES2['numbers']),
                (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES2['numbers']),
            ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in config_dict[self.extension + "_rules"]]

    def set_extension(self, new_extension):
        self.extension = new_extension
        self.set_extenstion_rules()
    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):

        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False


