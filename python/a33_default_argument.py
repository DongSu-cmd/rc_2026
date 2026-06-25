def print_n_time(value, n=2, v=3, g=5, *sum):           #디폴트 파람
        sum_ = 0
        for i in range(n):
                print(value)                            #position, default, 가변인자 #가변인자 없으면 keyword인자 or default인자
        for i in sum: 
               sum_ += i
        return sum_
        
def main():
    print(print_n_time("안녕하세요!", 10, 123, 54123, 123))

if __name__ == "__main__":
        main()