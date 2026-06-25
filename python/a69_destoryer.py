class test:
    def __inti__(self, name):
        self.name = name
        print(f"{self.name}이 생성됐다")

    def __del__(self):
        print(f"{self.name}이 파괴됐다")

def main():
    a = test("A")
    b = test("B")
    c = test("C")

    print(a, b, c)
    del C

    if __name__ == "__m         ain__":
        main()