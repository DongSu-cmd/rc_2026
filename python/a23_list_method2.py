import datetime


def main():
        ptime = datetime.datetime.now()
        list_a = [0, 1, 2, 3, 4, 5, 6]
        list_b = ["a", "b", "c", "d", "e", "f", ptime]
        del list_a[0]
        del list_b[2]
        del list_b[5]
        print(list_a)
        print(list_b)
        del list_a # 이후 사용불가
        #print(list_a)
        print(list_b.pop())
        print(list_b)
        
        if "a" in list_b: 
         list_b.remove("a")
         print(list_b)

if __name__ == "__main__":
        main()
#가비지컬렉터: 메모리 관리-동적할당 데이터 처분
