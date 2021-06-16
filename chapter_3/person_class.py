class Person():
    def __init__(self, age, name):
        self.age = age
        self.name = name
        
    def birthday(self):
        self.age = self.age + 1

class Parent(Person):
    def __init__(self, age, name):
        Person.__init__(self, age, name)
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
        
    def print_children(self):
        print("The children of ", self.name, "are:")
        for child in self.children:
            print(child.name)
        
#ben = Person(31, "Ben")
#paul = Person(42, "Paul")
#print(ben.name, ben.age)
#print(paul.name, paul.age)
#ben.birthday()
#paul.birthday()
#print(ben.name, ben.age)
#print(paul.name, paul.age)
john = Parent(60, "John")
ben = Person(32, "Ben")
print(john.name, john.age)
john.add_child(ben)
john.print_children()