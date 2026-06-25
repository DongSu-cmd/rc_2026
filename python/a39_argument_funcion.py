def call(func):
      for _ in range(10):
            func()

def hello():
      print("hello")

                            #pass 오류방지 한줄
def main():                 #함수도 클래스 객체
    temp_f = hello
    print(type(hello))
    call(temp_f)
if __name__ == "__main__":
        main()
