
import configparser
import ply.lex as lex
import ply.yacc as yacc

# Read the config file
config = configparser.ConfigParser()
config.read("parser.cfg")

# Lexer definition from config
tokens = config.get("lexer", "tokens").split(", ")

t_NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"
t_NUMBER = r"\d+"
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_SEMI = r";"
t_COMMA = r","
t_EQUAL = r"="
t_INT = r"\bint\b"
t_VOID = r"\bvoid\b"

# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


    
def t_error(t):
"""Generated docstring placeholder."""
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


# Define parsing rules from config (simplified example)
def p_declaration(p):
    """declaration : type_specifier NAME SEMI
    | type_specifier NAME EQUAL NUMBER SEMI"""
    if len(p) == 4:
        p[0] = f"{p[1]} {p[2]};"
    else:
        p[0] = f"{p[1]} {p[2]} = {p[4]};"


def p_type_specifier(p):
    """type_specifier : INT
    | VOID"""
    p[0] = p[1]


    
# Error handling rule
def p_error(p):
"""Generated docstring placeholder."""
    print("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")


# Build the parser
parser = yacc.yacc()

    

# Test the parser
def parse_code(code):
"""Generated docstring placeholder."""
    lexer.input(code)
    return parser.parse(lexer=lexer)


# Example code for parsing
if __name__ == "__main__":
    code = """
    int x;
    int y = 10;
    void foo;
    """
    result = parse_code(code)
    print("Parsed code:\n", result)