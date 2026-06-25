import time

def main():
    print(time.time())
    print(time.asctime())
    print(time.clock_gettime_ns(1))

    ctime = time.time()                 #prev time
    cnt = int()
    while time.time() < 5 + ctime: #5초 동안 반복
        cnt += 1
        print(f"이 컴퓨터는 5초 동안 {cnt:,d} 카운트가 실행되었다.")


if __name__ == "__main__":
        main()
