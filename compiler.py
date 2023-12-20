# git add .
# git commit -m ""
# git push https://github.com/C0deforbreakfast/mini-compiler.git (<remote_name>) master (<branch_name>)
# for setting upstream of git to https://github.com/C0deforbreakfast/mini-compiler.git remote and 
# master branch use git push -u https://github.com/C0deforbreakfast/mini-compiler.git master

index = 0
line = 1
file = open('input_file.txt', 'a').write(' ')
block_number = 0

def printm(a):
    print(a, end=' ')


class Error:
    def __init__(self):
        global line

    def printing(self, text):
        print(text, end=' ')
    
    def print_error(self, text):
        self.printing(text)
        exit()

    def valid_variable_names(self, string):
        error_message = f"ERROR in line {line}"
        for character in string:
            if ord(character) < 65 or ord(character) > 122 or 90 < ord(character) < 95 \
            or ord(character) == 96:
                self.print_error(error_message)

    def missmatch(self):
        error_message = f"ERROR in line {line}"
        self.print_error(error_message)


class Symbol:
    def __init__(self):
        # Type is word object #
        self.type = None


class Env:
    def __init__(self, next, prev=None):
        global block_number
        global table_data
        self.prev = prev
        self.next = next
        self.block_number = block_number
        self.symbol_table = {}

    def put(self, symbol, id):
        # Symbol is a word object #
        self.symbol_table[id.lexeme] = symbol

    def get(self, id):
        symbol_table_ids = self.symbol_table.keys()
        if id.lexeme in symbol_table_ids:
            symbol = self.symbol_table[id.lexeme]
            table_data[self.block_number] = self.symbol_table
            # print(id.lexeme, end=' ')
            # print(':', end=' ')
            # print(symbol.type)


class Parser:
    def __init__(self):
        self.lexer = LexicalAnalyzer()
        self.top = None
        self.saved = None
        self.error = Error()

    def match(self, t=None):
        print('match')
        self.lookahead = self.lexer.scan()
        print('lookahead is :', self.lookahead)
        if t is not None:
            if self.lookahead != t:
                Error()
        else:
            self.error.missmatch()

    def program(self):
        print('program')
        self.match('begin')
        printm('begin')
        self.decls()
        self.block()
        self.match('end')

    def block(self):
        print('block')
        global block_number
        block_number += 1
        self.saved = self.top
        self.top = Env(self.top)
        self.match('{')
        printm('{')
        self.decls()
        self.stmts()
        self.match('}')
        printm('}')
        block_number -= 1

    def decls(self):
        print('decls')
        self.rest1()

    def rest1(self):
        print('rest1')
        global index
        this_index = index
        first = self.lexer.scan()
        print('lookahead is :', first)
        index = this_index
        if first.lower() in ['int', 'float', 'char', 'bool']:
            self.decl()
            self.rest1()

    def decl(self):
        print('decl')
        type = self.lexer.scan()
        print('lookahead is (type):', type)
        id = self.lexer.scan()
        print('lookahead is (id):', type)
        s = Symbol()
        s.type = type

    def stmts(self):
        print('stmts')
        self.rest2()

    def rest2(self):
        print('rest2')
        global index
        this_index = index
        first = self.lexer.scan()
        print('lookahead is :', first)
        index = this_index
        if self.error.valid_variable_names(first):
            self.stmt()
            self.rest2()

    def stmt(self):
        print(f'index is {index}')
        print(f'length is {len(self.lexer.input_file)}')
        first = self.lexer.input_file[index]
        if first == '{':
            self.block()
        else:
            self.factor()

    def factor(self):
        print('factor')
        self.match()


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
    def __init__(self, tag:int, lexeme):
        self.tag = Token(tag).tag
        self.lexeme = lexeme


class LexicalAnalyzer:
    def __init__(self):
        self.input_file = open("input_file.txt").read()
        self.length = len(self.input_file)
        self.tag = Tag()
        self.error = Error()
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
        print('tokenize')
        b = self.peek
        self.peek = ""
        if self.error.valid_variable_names(b):
            self.error.print_error()
        # For begin and end terminals
        elif b.lower() in ['begin', 'end']:
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
        return (b.lower())

    def scan(self):
        print('scan')
        global index
        global line
        is_line_comment = False
        is_comment = False
        token = ""

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
                    if self.input_file[index + 1] == '/':
                        if self.input_file[index + 2] == '/':
                            token = self.tokenize()
                    elif self.input_file[index + 1] in [';', '{', '}']:
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
    