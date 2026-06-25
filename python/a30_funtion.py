def print_hello(a:int, value: str | int) -> tuple:
    #print("Hello, World!", a)
    #print("안녕하세요, 세계!")

    """a: 반복 횟수, return: 실행 완료 메시지, value: 추가프린트할 데이터"""


    for i in range(a):
        print("Hello, World!",value, i)
    if isinstance(value, int): #파이썬 타입체크
    
        for _ in range(value):
            print("test")
    return "execution ok" ,123, 3.14
         
def main():
    print_hello(12, 11)
    print_hello(7, "python")

    re, re1, _ = print_hello(3, 2) # TypeError: print_hello() takes 1 positional argument but 2 were given

    print(re, re1, _)
    print(*re)

if __name__ == "__main__":
        main()
