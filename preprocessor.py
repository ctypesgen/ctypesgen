#!/usr/bin/env python

'''Preprocess a C source file using gcc and convert the result into
   a token stream

Reference is C99:
  * http://www.open-std.org/JTC1/SC22/WG14/www/docs/n1124.pdf

'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: preprocessor.py 663 2007-02-17 05:52:03Z Alex.Holkner $'

import os, re, shlex, sys, compiler, errno, lex, yacc, traceback
import ctypes
from lex import TOKEN

tokens = (
    'HEADER_NAME', 'IDENTIFIER', 'PP_NUMBER', 'CHARACTER_CONSTANT',
    'STRING_LITERAL', 'OTHER',

    'PTR_OP', 'INC_OP', 'DEC_OP', 'LEFT_OP', 'RIGHT_OP', 'LE_OP', 'GE_OP',
    'EQ_OP', 'NE_OP', 'AND_OP', 'OR_OP', 'MUL_ASSIGN', 'DIV_ASSIGN',
    'MOD_ASSIGN', 'ADD_ASSIGN', 'SUB_ASSIGN', 'LEFT_ASSIGN', 'RIGHT_ASSIGN',
    'AND_ASSIGN', 'XOR_ASSIGN', 'OR_ASSIGN',  'PERIOD', 'ELLIPSIS',

    'LPAREN', 'NEWLINE'
)

subs = {
    'D': '[0-9]',
    'L': '[a-zA-Z_]',
    'H': '[a-fA-F0-9]',
    'E': '[Ee][+-]?{D}+',
    'FS': '[FflL]',
    'IS': '[uUlL]*',
}
# Helper: substitute {foo} with subs[foo] in string (makes regexes more lexy)
sub_pattern = re.compile('{([^}]*)}')
def sub_repl_match(m):
    return subs[m.groups()[0]]
def sub(s):
    return sub_pattern.sub(sub_repl_match, s)
CHARACTER_CONSTANT = sub(r"L?'(\\.|[^\\'])+'")
STRING_LITERAL = sub(r'L?"(\\.|[^\\"])*"')
IDENTIFIER = sub('{L}({L}|{D})*')

# --------------------------------------------------------------------------
# Token value types
# --------------------------------------------------------------------------

# Numbers represented as int and float types.
# For all other tokens, type is just str representation.

class StringLiteral(str):
    def __new__(cls, value):
        assert value[0] == '"' and value[-1] == '"'
        # Unescaping probably not perfect but close enough.
        value = value[1:-1].decode('string_escape')
        return str.__new__(cls, value)

class SystemHeaderName(str):
    def __new__(cls, value):
        assert value[0] == '<' and value[-1] == '>'
        return str.__new__(cls, value[1:-1])

    def __repr__(self):
        return '<%s>' % (str(self))


# --------------------------------------------------------------------------
# Token declarations
# --------------------------------------------------------------------------

punctuators = {
    # value: (regex, type)
    r'...': (r'\.\.\.', 'ELLIPSIS'),
    r'>>=': (r'>>=', 'RIGHT_ASSIGN'),
    r'<<=': (r'<<=', 'LEFT_ASSIGN'),
    r'+=': (r'\+=', 'ADD_ASSIGN'),
    r'-=': (r'-=', 'SUB_ASSIGN'),
    r'*=': (r'\*=', 'MUL_ASSIGN'),
    r'/=': (r'/=', 'DIV_ASSIGN'),
    r'%=': (r'%=', 'MOD_ASSIGN'),
    r'&=': (r'&=', 'AND_ASSIGN'),
    r'^=': (r'\^=', 'XOR_ASSIGN'),
    r'|=': (r'\|=', 'OR_ASSIGN'),
    r'>>': (r'>>', 'RIGHT_OP'),
    r'<<': (r'<<', 'LEFT_OP'),
    r'++': (r'\+\+', 'INC_OP'),
    r'--': (r'--', 'DEC_OP'),
    r'->': (r'->', 'PTR_OP'),
    r'&&': (r'&&', 'AND_OP'),
    r'||': (r'\|\|', 'OR_OP'),
    r'<=': (r'<=', 'LE_OP'),
    r'>=': (r'>=', 'GE_OP'),
    r'==': (r'==', 'EQ_OP'),
    r'!=': (r'!=', 'NE_OP'),
    r'<:': (r'<:', '['),
    r':>': (r':>', ']'),
    r'<%': (r'<%', '{'),
    r'%>': (r'%>', '}'),
    r';': (r';', ';'),
    r'{': (r'{', '{'),
    r'}': (r'}', '}'),
    r',': (r',', ','),
    r':': (r':', ':'),
    r'=': (r'=', '='),
    r')': (r'\)', ')'),
    r'[': (r'\[', '['),
    r']': (r']', ']'),
    r'.': (r'\.', 'PERIOD'),
    r'&': (r'&', '&'),
    r'!': (r'!', '!'),
    r'~': (r'~', '~'),
    r'-': (r'-', '-'),
    r'+': (r'\+', '+'),
    r'*': (r'\*', '*'),
    r'/': (r'/', '/'),
    r'%': (r'%', '%'),
    r'<': (r'<', '<'),
    r'>': (r'>', '>'),
    r'^': (r'\^', '^'),
    r'|': (r'\|', '|'),
    r'?': (r'\?', '?')
}

def punctuator_regex(punctuators):
    punctuator_regexes = [v[0] for v in punctuators.values()]
    punctuator_regexes.sort(lambda a, b: -cmp(len(a), len(b)))
    return '(%s)' % '|'.join(punctuator_regexes)

# Process line-number directives from the preprocessor
# See http://docs.freebsd.org/info/cpp/cpp.info.Output.html
def t_directive(t):
    r'\#\s+(\d+)\s+"([^"]+)"[ \d]*\n'
    t.lexer.filename = t.groups[2]
    t.lexer.lineno = int(t.groups[1])
    return None

DIRECTIVE = re.compile(t_directive.__doc__)

@TOKEN(punctuator_regex(punctuators))
def t_punctuator(t):
    t.type = punctuators[t.value][1]
    return t

@TOKEN(IDENTIFIER)
def t_identifier(t):
    if t.value == 'defined':
        t.type = 'DEFINED'
    else:
        t.type = 'IDENTIFIER'
    return t

    # missing: universal-character-constant
@TOKEN(sub(r'({D}|\.{D})({D}|{L}|e[+-]|E[+-]|p[+-]|P[+-]|\.)*'))
def t_pp_number(t):
    t.type = 'PP_NUMBER'
    return t
    
@TOKEN(CHARACTER_CONSTANT)
def t_character_constant(t):
    t.type = 'CHARACTER_CONSTANT'
    return t

@TOKEN(STRING_LITERAL)
def t_string_literal(t):
    t.type = 'STRING_LITERAL'
    t.value = StringLiteral(t.value)
    return t

def t_lparen(t):
    r'\('
    if t.lexpos == 0 or t.lexer.lexdata[t.lexpos-1] not in (' \t\f\v\n'):
        t.type = 'LPAREN'
    else:
        t.type = '('
    return t

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    return None

def t_error(t):
    t.type = 'OTHER'
    return t

t_ignore = ' \t\v\f\r'

# --------------------------------------------------------------------------
# Lexers
# --------------------------------------------------------------------------

class PreprocessorLexer(lex.Lexer):
    def __init__(self):
        lex.Lexer.__init__(self)
        self.filename = '<input>'

    def input(self, data, filename=None):
        if filename:
            self.filename = filename 
        self.lasttoken = None
        self.input_stack = []

        lex.Lexer.input(self, data)

    def push_input(self, data, filename):
        self.input_stack.append(
            (self.lexdata, self.lexpos, self.filename, self.lineno))
        self.lexdata = data
        self.lexpos = 0
        self.lineno = 1
        self.filename = filename
        self.lexlen = len(self.lexdata)

    def pop_input(self):
        self.lexdata, self.lexpos, self.filename, self.lineno = \
            self.input_stack.pop()
        self.lexlen = len(self.lexdata)

    def token(self):
        result = lex.Lexer.token(self)
        while result is None and self.input_stack:
            self.pop_input()
            result = lex.Lexer.token(self)

        if result:
            self.lasttoken = result.type
            result.filename = self.filename
        else:
            self.lasttoken = None

        return result

class TokenListLexer(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def token(self):
        if self.pos < len(self.tokens):
            t = self.tokens[self.pos]
            self.pos += 1
            return t
        else:
            return None

def symbol_to_token(sym):
    if isinstance(sym, yacc.YaccSymbol):
        return sym.value
    elif isinstance(sym, lex.LexToken):
        return sym
    else:
        assert False, 'Not a symbol: %r' % sym

def create_token(type, value, production=None):
    '''Create a token of type and value, at the position where 'production'
    was reduced.  Don't specify production if the token is built-in'''
    t = lex.LexToken()
    t.type = type
    t.value = value
    t.lexpos = -1
    if production:
        t.lineno = production.slice[1].lineno
        t.filename = production.slice[1].filename
    else:
        t.lineno = -1
        t.filename = '<builtin>'
    return t

# --------------------------------------------------------------------------
# Grammars
# --------------------------------------------------------------------------

DEFINE = re.compile("#define\s+(\w+)(?:\(([^)]+)\))?(?:\s+(.+))?")

# Extract variable names and/or strings from input data
ADJACENT_STRINGS = re.compile(r'"(?:\\.|[^\\"])*"|'
                              r'\b(\w+)\s+(?=["\w])|'
                              r'(?<=["\w])\s+(\w+)\b((?= "))?')

class PreprocessorDefine(object):
    def __init__(self, name, code, vars):
        self.deps = []
        self.argnames = []
        self.name = name
        self.emitted = False
        self.succeeded = False
        self.vars = vars
        self.code = code
        self.node = compiler.parse(code)
        try:
            compiler.walk(self.node, self)
        except:
            #print "Could not parse %s: %s" % (name, self.code)
            #traceback.print_exc(limit=0, file=sys.stdout)
            self.emitted = True

    def visitName(self, node):
        if node.name not in self.argnames:
            self.deps.append(self.vars[node.name])

    def visitLambda(self, node):
        self.argnames = node.argnames
        compiler.walk(node.code, self)

    def emit(self, file):
        if errno.__dict__.has_key(self.name):
            print >>file, 'from errno import %s' % self.name
            self.succeeded = True
        else:
            try:
                if not self.emitted:
                    self.emitted = True
                    for d in self.deps:
                        if d and not d.emit(file):
                            return False
                    print >>file, '%s = %s' % (self.name, self.code)
                    self.succeeded = True
            except:
                pass
        return self.succeeded

class PreprocessorParser(object):
    def __init__(self):
        self.cpp = "gcc -E"
        self.flags = ""
        self.defines = []
        self.include_path = []
        self.matches = []
        self.output = []
        self.lexer = lex.lex(cls=PreprocessorLexer)

    def parse(self, filename):
        """Parse a file and save its output"""

        for path in self.include_path:
            self.flags += " -I%s" % path 
 
        for define in self.defines:
            self.flags += " -D%s" % define
    
        print "%s -U __GNUC__ -dD %s %s" % (self.cpp, self.flags, filename)

        f = os.popen("%s -U __GNUC__ -dD %s %s" % (self.cpp, self.flags, filename))

        code = []
        for line in f:
            m = DEFINE.match(line)
            if m:
                self.matches.append((filename,) + m.groups())

            m = DIRECTIVE.match(line)
            if m:
                filename = m.group(2)

            if line.startswith("#") and not line.startswith("# "):
                # Replace any directives other than line numbers
                # with placeholder empty lines
                code.append("\n")
            else:
                code.append(line)

        self.lexer.input("".join(code))
        self.output = []
        while True:
            token = self.lexer.token()
            if token is not None:
                self.output.append(token)
            else:
                break

    def emit(self, file, regex, all_names, all_headers, headers,
             imported_symbols):
        """Emit all of the preprocessor symbols which match the
           specified REGEX, along with their dependencies"""

        defines = {}
        vars = {}
        replacements = []
        value = None

        # Anything defined in ctypes or imported_symbols is fair game
        for container in ctypes.__dict__, imported_symbols, all_names:
            for key in container:
                defines[key] = None
                vars[key] = None

        # NULL in C is just 'None' in Python
        defines['None'] = None
        defines['NULL'] = PreprocessorDefine('NULL', 'None', defines)

        QC_CONDITIONAL = re.compile(r" \? (.+?) : ")

        for (filename, name, params, code) in self.matches:

            # If not specified, define to "1"
            if code is None:
                code = "1"

            # Convert the value into a function if necessary
            if params:
                code = "lambda %s: (%s)" % (params, code)

            # Try to execute the code
            try:
                value = eval(code, vars)
            except:
                # Looks like the code doesn't execute. Let's fix any string
                # variables which pop up adjacent to strings, and make sure
                # that they're added together correctly.
                if not params:
                    def repl(m):
                        (a,b,c) = m.groups()
                        if (a and a in vars and isinstance(vars[a], str)):
                            return r"%s + " % a
                        elif (b and b in vars and isinstance(vars[b], str)):
                            if c is not None:
                                return r" + %s +" % b
                            else:
                                return r" + %s" % b
                        else:
                            return m.group()

                    code = ADJACENT_STRINGS.sub(repl, code)

                code = code.replace(" || ", " or ")
                code = code.replace(" && ", " and ")
                code = QC_CONDITIONAL.sub(r" and \1 or ", code)

                # Try to execute the modified code
                try:
                    value = eval(code, vars)
                except Exception, e:
                    # It still didn't work. Next!
                    continue

            # Save the calculated value
            vars[name] = value

            # Save this definition
            defines[name] = PreprocessorDefine(name, code, defines)

            # If this is a match, output it
            if (name not in imported_symbols and
                (not regex or regex.match(name)) and
                (all_headers or filename in headers)):
                defines[name].emit(file)

