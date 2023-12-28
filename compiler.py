from drawer import Graphizer
# Global variables
file_name = 'input_file.txt'
index = 0
line = 1
file = open(file_name, 'a').write(' ')
block_number = 0
last_block_number = 0
table_data = {}
# SDT (Syntax-Directed translator)
def printf(a):
    print(a, end=' ')
    pass

# Error handling 
class Error:
    def __init__(self):
        global line

    def printing(self, text):
        print(text, end=' ')

    def print_error(self):
        error_message = f"ERROR in line {line}"
        self.printing(error_message)
        exit()
    # Check validaty of variable name
    def valid_variable_names(self, string):
        digits = '0123456789'
        letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
        if string[0] not in letters:
            return False
        for letter in string:
            if letter not in digits and letter not in letters:
                return False
        return True
    # Handle missmatch
    def missmatch(self):
        self.print_error()

# Each row in symbol table is a symbol object
class Symbol:
    def __init__(self, type):
        # Type is word object #
        self.type = type
        self.block_number = block_number

# AKA symbol table
class Env:
    def __init__(self, prev=None):
        global table_data
        global last_block_number
        self.prev = prev
        self.error = Error()
        self.symbol_table = {}
        self.block_number = block_number
        self.keywords = ['begin', 'end', 'float', 'int', 'char', 'bool']
        last_block_number = self.block_number
        table_data[f'{block_number}'] = ({}, [])
        if self.prev is not None:
            table_data[f'{self.prev.block_number}'][1].append(self.block_number)

    def put(self, word, symbol):
        # Symbol is a word object #

        if word.lexeme.lower() in self.symbol_table or word.lexeme.lower() in self.keywords:
            self.error.print_error()
        else:
            if self.error.valid_variable_names(word.lexeme):
                self.symbol_table[word.lexeme.lower()] = symbol
                new_data = table_data[f'{self.block_number}'][0]
                new_data[word.lexeme.lower()] = symbol.type
                table_data[f'{self.block_number}'] = (new_data,
                                                      table_data[f'{self.block_number}'][1])
            else:
                self.error.print_error()

    def get(self, id):
        if id.lexeme.lower() in self.keywords:
            self.error.print_error()
        symbol_table_ids = self.symbol_table.keys()
        if id.lexeme.lower() in symbol_table_ids:
            symbol = self.symbol_table[id.lexeme.lower()]
            return symbol
        elif self.prev is not None:
            s = self.prev.get(id)
        else:
            return None

        if s is None:
            s = Symbol('ND')
            s.block_number = line
        return s


class Parser:
    def __init__(self):
        self.lexer = LexicalAnalyzer()
        self.error = Error()
        self.lookahead = self.lexer.scan()
        self.top = Env(None)

    def match(self, t):
        if self.lookahead != t:
            self.error.missmatch()

        self.lookahead = self.lexer.scan()

    def program(self):
        global block_number
        self.match('begin')
        printf('begin')
        self.decls()
        self.block()
        self.match('end')
        printf('end')
        if self.lookahead is not None:
            self.error.print_error()

    def block(self):
        global block_number
        block_number = last_block_number + 1 
        saved = self.top
        self.top = Env(self.top)
        self.match('{')
        printf('{')
        self.decls()
        self.stmts()
        self.match('}')
        printf('}')
        self.top = saved
        block_number = self.top.block_number

    def decls(self):
        self.rest1()

    def rest1(self):
        if self.lookahead.lower() in ['int', 'float', 'char', 'bool']:
            self.decl()
            self.rest1()

    def decl(self):
        type = self.lookahead
        self.match(type)
        word = Word(type, self.lookahead)
        self.match(self.lookahead)
        s = Symbol(type)
        s.type = type
        self.top.put(word, s)
        self.match(';')

    def stmts(self):
        self.rest2()

    def rest2(self):
        if self.error.valid_variable_names(self.lookahead) or self.lookahead == '{':
            self.stmt()
            self.rest2()

    def stmt(self):
        if self.lookahead == '{':
            self.block()
        else:
            self.factor()
            self.match(';')

    def factor(self):
        word = Word('int', self.lookahead)
        s = self.top.get(word)
        printf(f'{self.lookahead}:{s.type}{s.block_number};')
        self.match(self.lookahead)

# Struct
class Tag:
    def __init__(self):
        self.ID = 1
        self.INT = 2
        self.CHAR = 3
        self.BOOL = 4
        self.FLOAT = 5


class Token:
    def __init__(self, tag):
        self.tag = tag


class Word:
    def __init__(self, tag: int, lexeme):
        self.tag = Token(tag).tag
        self.lexeme = lexeme


class LexicalAnalyzer:
    def __init__(self):
        self.input_file = open(file_name).read()
        self.length = len(self.input_file)
        self.tag = Tag()
        self.error = Error()
        # For better readabliity 
        INT = Word(self.tag.INT, 'int')
        FLOAT = Word(self.tag.FLOAT, 'float')
        BOOL = Word(self.tag.BOOL, 'bool')
        CHAR = Word(self.tag.CHAR, 'char')
        self.peek = ""
        # Initialize string table with keywords
        self.words = {
            'int': INT,
            'float': FLOAT,
            'bool': BOOL,
            'char': CHAR,
        }
        self.reserved_keywords_types = ['int', 'bool', 'char', 'float']

    def tokenize(self):
        b = self.peek
        self.peek = ""
        # For begin and end terminals
        if b.lower() in ['begin', 'end']:
            return b.lower()
        elif b.lower() in self.words.keys():
            if b.lower() in self.reserved_keywords_types:
                return self.words[b.lower()].lexeme
            else:
                return b
        else:
            self.words[b.lower()] = Word(self.tag.ID, b.lower())
            return b

    def terminal_tokenize(self):
        b = self.peek
        self.peek = ""
        return b.lower()

    def scan(self):
        global index
        global line
        is_line_comment = False
        is_comment = False
        token = ""
        terminals = [';', '{', '}', '+', '=', '-', ')', '(', '&', '^', '%', '$'
                     '#', '@', '!', '?', '>', '<', '`', ',', '.', '[', ']', ':'
                     '~', '|']

        while index < len(self.input_file):
            # Handle comments // and /* */
            if "//" in self.peek:
                is_line_comment = True
                self.peek = ""
            elif "/*" in self.peek:
                is_comment = True
                self.peek = ""

            if is_line_comment is False and is_comment is False:
                # Handling ' ', '\t'
                if self.input_file[index] == (' ' or '\t') and len(self.peek) == 0:
                    pass
                # Handling '\n'
                elif self.input_file[index] == '\n':
                    line += 1
                    if len(self.peek) != 0:
                        token = self.terminal_tokenize()
                # Getting characters
                elif self.input_file[index] not in [' ', '\n', '\t']:
                    self.peek += self.input_file[index]
                    # Check for comments
                    if self.input_file[index + 1] == '/':
                        if self.input_file[index + 2] == '/' \
                            or self.input_file[index + 2] == '*':
                            token = self.tokenize()
                    elif self.peek == '/':
                        if self.input_file[index + 1] == '/':
                            token = self.tokenize()
                    # Check for / and * terminals which are not allowed
                    elif self.input_file[index + 1] == '/':
                        if self.input_file[index + 2] != '/':
                            token = self.tokenize()
                    elif self.input_file[index + 1] == '*':
                        if self.input_file[index + 2] != '/':
                            token = self.tokenize()
                    # Check for next character that is allowed or not
                    elif self.input_file[index + 1] in terminals:
                        token = self.tokenize()
                    elif self.peek in [';', '{', '}']:
                        token = self.terminal_tokenize()
                # Handling tokenization
                # Handling ';', '{', '}'
                elif self.peek in [';', '{', '}']:
                    token = self.terminal_tokenize()
                    # Handling ' ' after the word
                elif self.input_file[index] == ' ':
                    token = self.tokenize()
            # Handling end conditions for comments
            if is_line_comment:
                if self.input_file[index] == '\n':
                    is_line_comment = False
                    line += 1
            elif is_comment:
                if self.input_file[index] == '*' and self.input_file[index + 1] == '/':
                    is_comment = False
                    index += 1
                elif self.input_file[index] == '\n':
                    line += 1

            index += 1

            if len(token) != 0:
                return token


if __name__ == '__main__':
    p = Parser()
    p.program()
    
    user_input = input("\nDo you want to visualize symbol tables?(y/n)")
    if user_input == 'y':
        G = Graphizer()
        G.draw(table_data)