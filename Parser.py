# --- Parser
from Lexer import Lexer
from ply.yacc import yacc

class Parser:

    # Grammar by 
    # https://github.com/blukat29/regex-crossword-solver/blob/master/grammar.md

    def p_regex_term(self, p):
        ''' regex : outer_term '''
        p[0] = p[1]
    def p_regex_union(self, p):
        ''' regex : outer_term BAR regex '''
        p[0] = ("union", p[1], p[3])

    def p_outer_term_term(self, p):
        ''' outer_term : term '''
        p[0] = p[1]
    
    def p_outer_term_caret(self, p):
        ''' outer_term : CARET term '''
        p[0] = ("caret", p[2])

    def p_term_factor(self, p):
        ''' term : factor '''
        p[0] = p[1]
    
    def p_term_concat(self, p):
        ''' term : factor term '''
        p[0] = ("concat", p[1], p[2])
    
    def p_factor_char(self, p):
        ''' factor : CHAR '''
        p[0] = ("char", p[1])

    def p_factor_digit(self, p):
        ''' factor : DIGIT'''
        p[0] = ("digit", p[1])
    
    def p_factor_group(self, p):
        ''' factor : LPAREN regex RPAREN '''
        p[0] = ("group", p[2])

    def p_factor_factor_star(self, p):
        ''' factor : factor STAR '''
        p[0] = ("star", p[1])
    
    def p_factor_factor_plus(self, p):
        ''' factor : factor PLUS '''
        p[0] = ("concat", p[1], ("star", p[1]))

    def p_factor_factor_question(self, p):
        ''' factor : factor QUESTION '''
        p[0] = ("union", p[1], ("empty",))

    def p_factor_dot(self, p):
        ''' factor : DOT '''
        p[0] = ("any", )

    def p_factor_set(self, p):
        ''' factor : set '''
        p[0] = p[1]

    def p_set_set_item(self, p):
        ''' set : LBRACKET set_items RBRACKET '''
        p[0] = ("set", p[2])
    
    def p_set_not_set_items(self, p):
        ''' set : LBRACKET CARET set_items RBRACKET '''
        p[0] = ("set_not", p[3])

    def p_set_items_set_item(self, p):
        ''' set_items : set_item '''
        p[0] = p[1]
    
    def p_set_items_set_item_set_items(self, p):
        ''' set_items : set_item set_items'''
        p[0] = ("set_concat", p[1], p[2])

    def p_set_item_char(self, p):
        ''' set_item : set_char '''
        p[0] = p[1]
    
    def p_set_item_range(self, p):
        ''' set_item : set_char DASH set_char '''
        p[0] = ("set_range", p[1], p[3])
    
    def p_set_char_char(self, p):
        ''' set_char : CHAR '''
        p[0] = ("char", p[1])
    
    def p_set_char_digit(self, p):
        ''' set_char : DIGIT '''
        p[0] = ("digit", p[1])




    def p_error(self, p):
        print(f'Syntax error at {p.value!r}')
    
    # Build the parser
    def __init__(self):
        self.lexer = Lexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc(module=self)

    # Parse expressions.
    def parse(self, regex):
        ast = self.parser.parse(regex)
        return ast