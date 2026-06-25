import time
def main():

    i = int()
    while i <10:
        print(f"{i}번째 실행 중..")
        i += 1

    try:
        while True:                                 #call back 함수 관련
            print(".", end="", flush=True)          #?
            time.sleep(0.1)                         # 0.1초 대기 fps 설정
    except KeyboardInterrupt:
        print("키보드 인터럽트가 발생했습니다.")
    list_test = list("sin dong su is the wearing glasses")    
    print(list_test)
    while 's' in list_test:
        list_test.remove('s')
    print(list_test)

if __name__ == "__main__":
        main()
