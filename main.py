class translator:
    def up(self, value=1):
        return "self.memory_array[self.memory_pointer] += "+ str(value)
        
    def down(self, value=1):
        return "self.memory_array[self.memory_pointer] -= "+ str(value)

    def fright(self, value=1):
        self.ident += value
        return "\n".join(["\t" * (self.ident*(i>0) + i - value) + "while self.memory_array[self.memory_pointer] != 0:" for i in range(value)])

    def fleft(self, value=1):
        self.ident -= value
        return ""

    def right(self, value=1):
        return "self.memory_pointer += "+ str(value)

    def left(self, value=1):
        return "self.memory_pointer -= " + str(value)

    def front(self, value=1):
        return "print(chr(self.memory_array[self.memory_pointer])*" + str(value) + ", end='')" 
    
    commands_to_python = {
    '👆' : up,
    '👇' : down,
    '🤜' : fright,
    '🤛' : fleft,
    '👉' : right,
    '👈' : left,
    '👊' : front,
    }
    
    def __init__(self, name):
        self.header = \
f"""import numpy as np
class {name}:
\tdef __init__(self):
\t\tself.memory_pointer = 0
\t\tself.memory_array_lenght = 1000
\t\tself.memory_array = np.zeros(1000, dtype=np.uint8)
    
\tdef main(self):"""
        self.finisher = \
f"""\n\n
if __name__=='__main__':
\tfoo = {name}()
\tfoo.main()
"""

        self.code = ""
        self.ident = 2
        
        
    def __getitem__(self, key):
        return "\n" + "\t"*self.ident + self.commands_to_python[key](self, self.value)

    def read_input(self, filename):
        with open(filename, 'r', encoding='utf8') as input_file:
            self.last_command = None
            
            for line in input_file:
                for command in line:
                    if self.last_command is None:
                        self.value = 1
                        self.last_command = command
                        continue
                        
                    if command == self.last_command:
                        self.value += 1
                        continue
                    
                    self.code += self[self.last_command]
                    self.value = 1
                    self.last_command = command
                    
                self.code += self[self.last_command]
                
    def save_program(self, filename):
        with open(filename, 'w') as output_file:
            output_file.write(self.header)
            output_file.write(self.code)
            output_file.write(self.finisher)
            
if __name__=='__main__':
    name = "test2"
    tr = translator(name)
    tr.read_input(f"{name}.hand")
    tr.save_program(f"{name}.py")