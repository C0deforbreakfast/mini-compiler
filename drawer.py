import graphviz


class Graphizer:
    def __init__(self):
        # Initialize a digraph
        self.dot = graphviz.Digraph('structs', node_attr={'shape': 'record'})
        self.counter = 0
        self.labeling = f'<f{self.counter}>'
        self.block = 0
        self.blocking = f'B{self.block}:'

    def check_after(self, string, value):
        string += ' | '
        return string

    def draw(self, table_data):
        # Draw tables according to table data
        for key, value in table_data.items():
            count = 0
            string = '{' + '{' + self.labeling + self.blocking + '}'
            node_name = self.block
            self.counter += 1
            self.block += 1
            self.labeling = f'<f{self.counter}>'
            self.blocking = f'B{self.block}:'
            if len(value[0]) != 0:
                string = self.check_after(string, value)
                for key1, value1 in value[0].items():
                    string += '{' + self.labeling + f' {key1}' + '| '
                    self.counter += 1
                    self.labeling = f'<f{self.counter}>'
                    string += self.labeling + f' {value1}' + '}'
                    self.counter += 1
                    self.labeling = f'<f{self.counter}>'
                    count += 1
                    if count != len(value[0]):
                        string += ' | '
            string += '}'
            print(node_name ,string)
            self.dot.node(str(node_name), string)

        # Draw edges according to table data
        for key, value in table_data.items():
            for table_number in value[1]:
                self.dot.edge(key, str(table_number))

        self.dot.view()


table_data = {
    '0': ({}, [1]),
    '1': ({'x': 'int', 'z': 'int'}, [2]),
    '2': ({'y': 'int'}, [])
}

if __name__ == '__main__':
    G = Graphizer()
    G.draw(table_data)
