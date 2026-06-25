def rec_fac(n):
      if n == 1:
            return 1
      else:
            return n*rec_fac(n-1)
      
def for_fac(n):
      output = 1
      for n in range(n):
            output *= n+1
      return output

cnt=0
dic_cnt = 0
dictionary = {1: 1, 2: 1}

@Iru_cache(maxsize=None)
def fibonacci(n):
      global cnt
      cnt += 1
      if n==1:#n in dictionary:
          return 1#dictionary[n]
      else:
         # output = fibonacci(n-1) + fibonacci(n-2)
          return n*rec_fac(n-1)#dictionary[n] = output
          dic_cnt += 1  
          return fibonacci(n-1) + fibonacci(n-2) #output
      
def main():
    print(rec_fac(100))
    print(for_fac(100))
    print(fibonacci(4000))
    print(f"fibonacci함수가 실행된 횟수: {cnt}")

if __name__ == "__main__":
        main()
