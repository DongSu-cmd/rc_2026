class person:
    def __init__(self, b):
        self.b = b

class university:
    def __init__(self, a):
        self.a = a


class undergraduate(person, university):
    def __init__(self, c):
        person.__init__(self, 2)
        university.__init__(self, 1)
        self.c = c

def main():
    lol = undergraduate(3)
    print(lol.a, lol.b, lol.c)
    
    if __name__ == "__main__":
        main()