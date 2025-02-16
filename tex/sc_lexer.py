import re

from pygments.lexer import RegexLexer
from pygments.token import *

__all__ = ['SuperColliderLexer']

class SuperColliderLexer(RegexLexer):
    """
    For SuperCollider source code.
    """

    name = 'SuperCollider'
    url = 'https://supercollider.github.io/'
    aliases = ['supercollider', 'sc']
    filenames = ['*.sc', '*.scd']
    mimetypes = ['application/supercollider', 'text/supercollider']

    flags = re.MULTILINE
    
    tokens = {
        'root': [
            (r'\s+', Whitespace),
            (r'/\*', Comment.Multiline, 'comment'),
            (r'//.*?$', Comment.Singleline),
            (r'\b(var|arg)\b', Keyword.Declaration),
            (r'~[a-z]\w+?\b', Name.Variable),
            # Class names begin with a capital letter
            (r'\b[A-Z][\w_]+?\b', Name.Class),
            (r'\b(true|false|nil|pi|inf)\b', Keyword.Constant), 
            (r'\'[a-z][\w_]+?\'', String.Symbol),
            (r'\\[a-z][\w_]+?\b', String.Symbol),
            (r'[0-9][0-9]*\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+', Number.Integer),
            (r'"(\\\\|\\"|[^"])*"', String),
            (r'[{}()\[\];,\.]', Punctuation),
            (r'[+\-*/%=<>!&|]', Operator),
        ],
        # Comments to be processed separately
        'comment':  [
            (r'[^*/]+', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline)
        ],
    }
