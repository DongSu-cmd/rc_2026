def print_n_times(n, *args, abc="abc", defg="defg", **keyargs):
        for i in range(n):
                print(args)
        print(abc, defg)
        print(type(keyargs), keyargs)
        for k, v in keyargs.items():
               print(k, v)
        

def general_f(*args, **keyargs):            #래핑함수
       pass

def main():

    print_n_times(3, "sin", "dong", "su", "is", "nice")
    print_n_times(3, "test", defg = "dong", abc = "su")
    general_f(1, 2, 4, k="key")


if __name__ == "__main__":
        main()
        #인자=argument #매개변수  =>싹다 변수