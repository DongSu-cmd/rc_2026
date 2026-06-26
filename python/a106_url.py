from urllib import request

def main():
    a = request.urlopen("https://google.com")
    print(a.read())
   
if __name__ == "__main__":
        main()
