import logging
import os
import ply.yacc as yacc
import threading

from ieml import parser_folder
from ieml.exceptions import CannotParse
from ieml.syntax.parser import IEMLParser
from ieml.usl.parser.lexer import tokens, get_lexer
from ieml.usl import Usl
from ieml.commons import Singleton


class USLParser(metaclass=Singleton):
    tokens = tokens
    lock = threading.Lock()

    def __init__(self):

        # Build the lexer and parser
        self.lexer = get_lexer()
        self.parser = yacc.yacc(module=self, errorlog=logging, start='usl',
                                debug=False, optimize=True, picklefile=os.path.join(parser_folder, "usl_parser.pickle"))

    def parse(self, s):
        """Parses the input string, and returns a reference to the created AST's root"""
        # self.usl = s
        # self.root = None
        with self.lock:
            try:
                return self.parser.parse(s, lexer=self.lexer)
            except CannotParse as e:
                e.s = s
                raise e

        #
        # if self.root is not None:
        #     return self.root
        # else:
        #     raise CannotParse(s, "Invalid usl.")

    # Parsing rules
    def p_usl(self, p):
        """ usl : IEML_OBJECT """
        p[0] = Usl(IEMLParser().parse(p[1]))

    def p_error(self, p):
        if p:
            msg = "Syntax error at '%s' (%d, %d)" % (p.value, p.lineno, p.lexpos)
        else:
            msg = "Syntax error at EOF"

        raise CannotParse(None, msg)

