# git add .
# git commit -m ""
# git push https://github.com/C0deforbreakfast/mini-compiler.git (<remote_name>) master (<branch_name>)
# for setting upstream of git to https://github.com/C0deforbreakfast/mini-compiler.git remote and 
# master branch use git push -u https://github.com/C0deforbreakfast/mini-compiler.git master

index = 0
line = 1
file = open('input_file.txt', 'a').write(' ')
block_number = 0
table_data = {}

def printd(a):
    # print(a)
    pass

def printm(a):
    print(a, end=' ')
    pass


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
                return False
        return True

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

    def put(self, id, symbol):
        # Symbol is a word object #
        self.symbol_table[id.lexeme] = symbol

    def get(self, id):
        symbol_table_ids = self.symbol_table.keys()
        if id.lexeme in symbol_table_ids:
            symbol = self.symbol_table[id.lexeme]
            # table_data[self.block_number] = self.symbol_table
            return symbol


class Parser:
    def __init__(self):
        self.lexer = LexicalAnalyzer()
        self.error = Error()
        self.lookahead = self.lexer.scan()

    def match(self, t=None):
        printd('match')
        printd(f'lookahead is : {self.lookahead}')
        if t is not None:
            if self.lookahead != t:
                self.error.missmatch()
        else:
            pass
            # printm(self.lookahead)

        self.lookahead = self.lexer.scan()

    def program(self):
        self.top = None
        printd('program')
        self.match('begin')
        printm('begin')
        self.decls()
        self.block()
        self.match('end')
        printm('end')

    def block(self):
        printd('block')
        global block_number
        block_number += 1
        self.saved = self.top
        self.top = Env(self.top)
        # self.top = self.saved
        self.match('{')
        printm('{')
        self.decls()
        self.stmts()
        self.match('}')
        printm('}')
        block_number -= 1

    def decls(self):
        printd('decls')
        self.rest1()

    def rest1(self):
        printd('rest1')
        printd(f'lookahead is :{self.lookahead}')
        if self.lookahead.lower() in ['int', 'float', 'char', 'bool']:
            self.decl()
            self.rest1()

    def decl(self):
        printd('decl')
        type = self.lookahead
        printd(f'lookahead is (type): {type}')
        id = self.lexer.scan()
        printd(f'lookahead is (id): {id}')
        self.lookahead = self.lexer.scan()
        self.word = Word(type, id)
        self.s = Symbol()
        self.s.type = type
        self.top.put(self.word, self.s)
        self.match(';')

    def stmts(self):
        printd('stmts')
        self.rest2()

    def rest2(self):
        printd('rest2')
        printd(f'lookahead is : {self.lookahead}')
        if self.error.valid_variable_names(self.lookahead) or self.lookahead == '{':
            self.stmt()
            self.rest2()
    def stmt(self):
        printd(f'index is {index}')
        printd(f'length is {len(self.lexer.input_file)}')
        if self.lookahead == '{':
            self.block()
        else:
            self.factor()
            self.match(';')

    def factor(self):
        printd('factor')
        # self.word = Word(0, self.lookahead)
        self.s = self.top.get(self.word)
        printm(f'{self.lookahead}:{self.s.type};')
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
        printd('tokenize')
        b = self.peek
        self.peek = ""
        '''if self.error.valid_variable_names(b):
            self.error.print_error()'''
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
        printd('scan')
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
                        if self.input_file[index + 2] == '/' \
                            or self.input_file[index + 2] == '*':
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
