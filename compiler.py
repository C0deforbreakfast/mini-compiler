# git add .
# git commit -m ""
# git push https://github.com/C0deforbreakfast/mini-compiler.git (<remote_name>) master (<branch_name>)
# for setting upstream of git to https://github.com/C0deforbreakfast/mini-compiler.git remote and 
# master branch use git push -u https://github.com/C0deforbreakfast/mini-compiler.git master

index = 0
line = 1
file = open('input_file.txt', 'a').write(' ')

class Parser():
    def __init__(self):
        pass

    def match(self):
        pass

    def program(self):
        pass

    def block(self):
        pass

    def decls(self):
        pass

    def decl(self):
        pass


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
        if 49 <= ord(b[0]) <= 57:
            print(f"ERROR in line {line}")
            pass
        # For begin and end terminals
        elif b.lower() in ['begin', 'end']:
            print(b.lower())
        elif b.lower() in self.words.keys():
            if b.lower() in self.reserved_keywords_types:
                print(self.words[b.lower()].lexeme)
            else:
                print(b)
        else:
            self.words[b.lower()] = Word(self.tag.ID, b.lower())
            print(b)

    def terminal_tokenize(self):
        b = self.peek
        self.peek = ""
        print(b.lower())

    def scan(self):
        global index
        global line
        is_line_comment = False
        is_comment = False

        while index < len(self.input_file):
            # Handle comments // and /* */
            if "//"  in self.peek:
                is_line_comment = True
                self.peek = ""
            elif "/*" in self.peek:
                is_comment = True
                self.peek = ""

            if is_line_comment == False and is_comment == False:
                # Handling ' ', '\t'
                if self.input_file[index] == (' ' or '\t') and len(self.peek) == 0:
                    pass
                # Handling '\n'
                elif self.input_file[index] == '\n':
                    line += 1
                    if len(self.peek) != 0:
                        self.terminal_tokenize()
                # Getting characters
                elif self.input_file[index] not in [' ', '\n', '\t']:
                    self.peek += self.input_file[index]
                    if self.input_file[index + 1] == '/':
                        if self.input_file[index + 2] == '/':
                            self.tokenize()
                    elif self.input_file[index + 1] in [';', '{', '}']:
                        self.tokenize()
                    elif self.peek in [';', '{', '}']:
                        self.terminal_tokenize()
                # Handling tokenization
                    # Handling ';', '{', '}'
                elif self.peek in [';', '{', '}']:
                    self.terminal_tokenize()
                    # Handling ' ' after the word
                elif self.input_file[index] == ' ':
                    self.tokenize()
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
            
                    

if __name__ == '__main__':
    lexer = LexicalAnalyzer()
    lexer.scan()

    