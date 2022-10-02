import random

def code(self):
    number_list = [x for x in range(10)]
    code_items=[]

    for i in range(5):
        num = random.choice(number_list)
        code_items.append(num)

    code_string = "".join(str(item) for item in code_items)
    self.number = code_string