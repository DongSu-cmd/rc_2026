def main():
        print(10==100)
        print(10!=100)
        print(10<100)
        print(10<=100)
        print(type(True))

        print(not True)
        print(not False)
        print(True and True)
        print(True and False)
        print(False and False)
        print(True or True)
        print(True or False)
        print(False or False)

        a = int(input("100보다 큰 수를 입력하세요: "))
        
        if a > 100:#콜론과 인벤테이션
                print("a가 100보다 큽니다.")
                print("프로그램을 종료합니다.")

if __name__=="__main__":
        main()