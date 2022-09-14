from ply.lex import lex

class Lexer:
    # Defining tokens
    tokens = ( 
        'CHAR', 
        'DIGIT',
        'DOT', 
        'DASH',
        'BAR', 
        'CARET',
        'LPAREN', 
        'RPAREN', 
        'LBRACKET', 
        'RBRACKET',
        'PLUS',
        'STAR',
        'QUESTION' 
    )
    
    t_ignore = ' \t'
    
    t_CHAR      = r'[A-Z]'
    t_DIGIT     = r'[0-9]'
    t_DOT       = r'\.'
    t_DASH      = r'\-'

    t_BAR       = r'\|'
    t_CARET     = r'\^'
    
    t_LPAREN    = r'\('
    t_RPAREN    = r'\)'
    t_LBRACKET  = r'\['
    t_RBRACKET  = r'\]'

    t_PLUS      = r'\+'
    t_STAR      = r'\*'
    t_QUESTION  = r'\?'
    
    def t_ignore_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t):
        print(f'Illegal character {t.value[0]!r}')
        t.lexer.skip(1)

    # Build the lexer
    def __init__(self):
        self.lexer = lex(module=self)