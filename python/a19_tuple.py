def main():
    tu = tuple()
    print(tu, type(tu))
    tu_1 = 1, 2                       #원소 추가 제거 변경이 안됨 - tuple 단점
    print(tu_1, type(tu_1))

    a =10                             #tu기능
    b =20
    tmp = a
    a = b
    b = tmp
    print(a, b)

    a, b = b, a


if __name__ == "__main__":
        main()
                                    #tuple > list - 안정적 데이터 전달