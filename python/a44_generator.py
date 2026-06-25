def test():
    print("A함수가 호출됨.")
    yield "re"
    print("B함수가 호출됨.")
    yield "re"
    print("C함수가 호출됨.")
    yield "re"

def main():                 #제너레이터 사용
    ge = test()             #함수의 실행이 매번 다른 결과를 요구할때
    print(ge)               #일련의과정 -> 연속 수행
    #print(ge.__next__())
    #print(next(ge))
    #print(next(ge))
    for re in ge:
        print(re)

if __name__ == "__main__":
    main()