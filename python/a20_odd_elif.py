def main():
    number = int(input("Enter a number: "))
    
    #if number % 2 == 0:
   #     print(f"{number} is even.")
   # elif number % 2 != 0:
   #     print(f"{number} is odd.")
   # else:
    #    print("Invalid input.")

    print("홀수" if number % 2 != 0 else "짝수", "입니다.")

if __name__ == "__main__":
    main()