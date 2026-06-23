def main():
        
        print(range(10))
        print(range(1,10,0))
        a = range(10)
        print(list(a))
        print(range(5,3,10))
        a = []
        for i in range(0,100,2):
                a.append(i+1)
        print(a)

        list_b = ["a", "b", "c", "d", "e", "f"]
        for els in list_b:
                print(els+"원소", a)

        list_c = ["에이", "비", "씨"]
        for i in range(3):
                print(list_b[i], list_c[i])
        for b, c in zip(list_b, list_c):
                print(b, c)

if __name__=="__main__":
        main()
